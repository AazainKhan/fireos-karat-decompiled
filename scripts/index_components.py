#!/usr/bin/env python3
"""Flatten the manifest DB into agent-friendly TSVs.

Usage: index_components.py <manifests.json> <out_dir>

Writes:
  packages.tsv    package, apk path, sharedUserId, home, persistent, #components, #declared perms
  components.tsv  package, type, component, exported, guard permission
  actions.tsv     package, intent action or category it handles
  providers.tsv   package, content provider authority
  permissions.tsv package, declared permission, protection level
"""
import json
import sys
from pathlib import Path


def main() -> None:
    db = json.load(open(sys.argv[1]))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    files = {n: open(out / f"{n}.tsv", "w") for n in ("packages", "components", "actions", "providers", "permissions")}
    files["packages"].write("package\tapk\tsharedUserId\thome\tpersistent\tcomponents\tdeclared_perms\n")
    files["components"].write("package\ttype\tcomponent\texported\tpermission\n")
    files["actions"].write("package\taction\n")
    files["providers"].write("package\tauthority\n")
    files["permissions"].write("package\tpermission\tprotectionLevel\n")
    for pkg in sorted(db):
        for e in db[pkg]:
            comps = e.get("components") or []
            decl = e.get("decl_perm") or {}
            files["packages"].write("\t".join([pkg, e.get("file", ""), e.get("sharedUserId") or "",
                                               str(bool(e.get("home"))).lower(), str(bool(e.get("persistent"))).lower(),
                                               str(len(comps)), str(len(decl))]) + "\n")
            for c in comps:
                ctype, name, exp, perm = (list(c) + [None] * 4)[:4]
                files["components"].write("\t".join([pkg, ctype or "", name or "",
                                                     "yes" if exp == "exp" else "no", perm or ""]) + "\n")
            for a in sorted(set(e.get("actions") or [])):
                files["actions"].write(f"{pkg}\t{a}\n")
            for a in sorted(set(e.get("authorities") or [])):
                files["providers"].write(f"{pkg}\t{a}\n")
            for p, lvl in sorted(decl.items()):
                files["permissions"].write(f"{pkg}\t{p}\t{lvl or ''}\n")
    for f in files.values():
        f.close()
    print(f"{len(db)} packages indexed")


if __name__ == "__main__":
    main()
