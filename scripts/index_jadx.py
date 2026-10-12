#!/usr/bin/env python3
"""Turn jadx output into declaration-level TSV indexes (no method bodies).

Usage: index_jadx.py <decompiled_root> <out_dir>

<decompiled_root>/<package>/sources/** is jadx output for one APK. For each package writes:
  <out_dir>/<package>.classes.tsv  kind, class, extends, implements
  <out_dir>/<package>.members.tsv  class, kind (method/field), declaration
  <out_dir>/<package>.strings.tsv  class, constant (intent actions, extras, URIs, settings keys)
Only signatures and integration-relevant string constants are kept. Code bodies are dropped.
"""
import re
import sys
from pathlib import Path

PKG = re.compile(r"^package\s+([\w.]+);")
TYPE = re.compile(r"^\s*(?:(?:public|protected|private|abstract|static|final|sealed)\s+)*"
                  r"(class|interface|enum|@interface|record)\s+(\w+)"
                  r"(?:<[^{]*?>)?(?:\s+extends\s+([\w.<>, ]+?))?(?:\s+implements\s+([\w.<>, ]+?))?\s*\{")
METHOD = re.compile(r"^\s*(?:(?:public|protected|private|static|final|abstract|synchronized|native|default)\s+)+"
                    r"[\w.<>\[\], ?]+\s+\w+\s*\([^)]*\)\s*(?:throws [\w., ]+)?\s*[{;]")
CTOR = re.compile(r"^\s*(?:public|protected|private)\s+\w+\s*\([^)]*\)\s*(?:throws [\w., ]+)?\s*\{")
FIELD = re.compile(r"^\s*(?:(?:public|protected|private|static|final|volatile|transient)\s+)+"
                   r"[\w.<>\[\], ?]+\s+\w+\s*(?:=\s*[^;]*)?;")
# String constants that matter for integration: intent actions/categories/extras, content URIs,
# component names, settings keys and system properties.
STRING = re.compile(r'"((?:android|com|amazon|content|ro|persist|sys|vendor)[\w.:/\-]{6,200})"')


# Bundled third-party libraries: public elsewhere and noise for Fire OS questions.
THIRD_PARTY = re.compile(r"^(androidx|android/support|kotlin|kotlinx|javax|dagger|okhttp3|okio|retrofit2|io/reactivex"
                         r"|org/(apache|json|jetbrains|intellij|reactivestreams|slf4j|chromium)"
                         r"|com/(google|bumptech|squareup|fasterxml|facebook|airbnb|jakewharton))/")


def clean(s: str) -> str:
    s = s.strip().rstrip("{").strip()
    return re.sub(r"\s+", " ", s)


def index_package(pkg_dir: Path, out_dir: Path) -> tuple[int, int, int]:
    classes, members, strings = set(), set(), set()
    src = pkg_dir / "sources"
    for jf in sorted(src.rglob("*.java")):
        if THIRD_PARTY.match(jf.relative_to(src).as_posix()):
            continue
        text = jf.read_text(errors="replace")
        pkg = ""
        stack: list[tuple[str, int]] = []
        depth = 0
        for line in text.splitlines():
            if not pkg:
                m = PKG.match(line)
                if m:
                    pkg = m.group(1)
            t = TYPE.match(line)
            if t:
                kind, name, ext, impl = t.groups()
                outer = stack[-1][0] if stack else (pkg + "." if pkg else "")
                fq = f"{outer}${name}" if stack else f"{outer}{name}"
                classes.add((kind, fq, (ext or "").strip(), re.sub(r"\s+", "", impl or "")))
                stack.append((fq, depth))
            elif stack and depth == stack[-1][1] + 1:
                owner = stack[-1][0]
                if METHOD.match(line) or CTOR.match(line):
                    members.add((owner, "method", clean(line)))
                elif FIELD.match(line):
                    # Drop initializer values: they can hold embedded keys or other secrets.
                    # Integration constants are captured separately in strings.tsv.
                    decl = clean(line.split("=", 1)[0]).rstrip(";").strip() + ";"
                    members.add((owner, "field", decl))
            if stack:
                for s in STRING.findall(line):
                    strings.add((stack[-1][0], s))
            depth += line.count("{") - line.count("}")
            while stack and depth <= stack[-1][1]:
                stack.pop()
    name = pkg_dir.name
    for suffix, header, rows in (("classes", "kind\tclass\textends\timplements", classes),
                                 ("members", "class\tkind\tdeclaration", members),
                                 ("strings", "class\tconstant", strings)):
        with open(out_dir / f"{name}.{suffix}.tsv", "w") as f:
            f.write(header + "\n")
            for r in sorted(rows):
                f.write("\t".join(r) + "\n")
    return len(classes), len(members), len(strings)


def main() -> None:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for pkg_dir in sorted(p for p in root.iterdir() if (p / "sources").is_dir()):
        c, m, s = index_package(pkg_dir, out)
        print(f"{pkg_dir.name}\t{c} classes\t{m} members\t{s} strings")


if __name__ == "__main__":
    main()
