#!/usr/bin/env python3
"""Check a removal list against the image's manifest DB.
Usage: lint_removals.py manifests.json libs_features.txt remove.tsv [--upto N]
Errors: a removed package is not in the image; a kept package needs a required shared library whose
file belongs to a removed package. Warnings: a kept component is guarded by a permission only a removed
package declares while a kept package requests it. Prints the HOME candidates left after removal."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python -I drops the script dir
from romlib import canon, load_removals


def lint(M, libs_text, removals):
    """Returns (lines, error_count). `removals` is a set of package names."""
    R = set(removals)
    libs = {m.group(1): m.group(2) for l in libs_text.splitlines()
            for m in [re.search(r'library name="([^"]+)" *file="([^"]+)"', l)] if m}
    out, err = [], 0
    for p in sorted(R - set(M)):
        out.append(f'ERROR not in image: {p}')
        err += 1
    owner_of = {canon(e['file']): p for p, es in M.items() for e in es}
    declared = {}
    for p, es in M.items():
        for e in es:
            for pr in e['decl_perm']:
                declared.setdefault(pr, set()).add(p)
    for p, es in sorted(M.items()):
        if p in R:
            continue
        for e in es:
            for lib, req in e['uses_lib']:
                f = libs.get(lib, '')
                o = owner_of.get(canon(f)) if f.endswith('.apk') else None
                if req != '0x0' and o in R:
                    out.append(f'ERROR {p} requires library {lib} from removed {o}')
                    err += 1
            for c in e['components']:
                pr = c[3]
                if pr and pr in declared and declared[pr] <= R:
                    callers = sorted(q for q, qs in M.items()
                                     if q not in R and q != p and any(pr in x['uses_perm'] for x in qs))
                    if callers:
                        out.append(f'WARN {p}/{c[1]} guarded by {pr} (declared only by removed '
                                   f'{sorted(declared[pr])}); kept callers lose access: {callers}')
    home = sorted(p for p, es in M.items() if p not in R and any(e['home'] for e in es))
    out.append(f'HOME candidates after removal: {home}')
    out.append(f'{len(R)} removed, {err} errors')
    return out, err


def main(argv):
    if len(argv) < 4:
        sys.exit(__doc__)
    upto = argv[argv.index('--upto') + 1] if '--upto' in argv else '999'
    M = json.load(open(argv[1]))
    pkgs = {p for p, _, _ in load_removals(argv[3], upto)}
    lines, err = lint(M, open(argv[2]).read(), pkgs)
    print('\n'.join(lines))
    return 1 if err else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
