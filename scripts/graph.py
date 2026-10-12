#!/usr/bin/env python3
"""Dependency graph from the manifest DB. Usage: graph.py manifests.json libs_features.txt graph.json
deps[pkg][provider] = reasons: 'perm:<name>' (provider declares it; undeclared names belong to 'android'),
'lib-req:<lib>' (required shared library; provider is the owning package or 'JAR:<file>'), 'meta' (manifest names it).
rev is the inverse, suid maps sharedUserId -> packages, info has per-package facts."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python -I drops the script dir
from romlib import canon


def build(M, libs_text):
    libs = {m.group(1): m.group(2) for l in libs_text.splitlines()
            for m in [re.search(r'library name="([^"]+)" *file="([^"]+)"', l)] if m}
    declared = {}
    for p, es in M.items():
        for e in es:
            for pr in e['decl_perm']:
                declared.setdefault(pr, set()).add(p)
    files = {canon(e['file']): p for p, es in M.items() for e in es}
    deps, rev, suid, info = {}, {}, {}, {}

    def add(p, q, why):
        if p != q:
            deps.setdefault(p, {}).setdefault(q, [])
            if why not in deps[p][q]:
                deps[p][q].append(why)

    for p, es in M.items():
        for e in es:
            for pr in e['uses_perm']:
                owners = set(declared.get(pr, ())) or ({'android'} if pr.startswith('android.') else set())
                for q in sorted(owners):
                    add(p, q, 'perm:' + pr)
            for lib, req in e['uses_lib']:
                f = libs.get(lib)
                if f and req != '0x0':
                    q = files.get(canon(f)) if f.endswith('.apk') else None
                    add(p, q or 'JAR:' + f.rsplit('/', 1)[-1], 'lib-req:' + lib)
            for t in e['targets']:
                if t in M:
                    add(p, t, 'meta')
            if e['sharedUserId']:
                suid.setdefault(e['sharedUserId'], []).append(p)
        info[p] = {'file': es[0]['file'], 'suid': es[0]['sharedUserId'], 'home': any(e['home'] for e in es),
                   'persistent': any(e['persistent'] for e in es),
                   'auth': list(dict.fromkeys(a for e in es for a in e['authorities'])),
                   'exp': sum(1 for e in es for c in e['components'] if c[2])}
    for p, d in deps.items():
        for q in d:
            rev.setdefault(q, []).append(p)
    for q in rev:
        rev[q].sort()
    for d in deps.values():
        for q in d:
            d[q].sort(key=lambda r: (r != 'meta', r))
    return {'deps': deps, 'rev': rev, 'suid': suid, 'info': info}


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    g = build(json.load(open(sys.argv[1])), open(sys.argv[2]).read())
    json.dump(g, open(sys.argv[3], 'w'), indent=1)
    print(len(g['deps']), 'packages with dependencies')
