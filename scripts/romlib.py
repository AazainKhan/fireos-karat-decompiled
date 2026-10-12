"""Shared helpers for the removal tools: batch ids, removal lists, canonical image paths."""
import re


def batch_key(b):
    """'1a' -> (1, 'a'); '2' -> (2, ''). Batch ids are a number plus an optional letter."""
    m = re.fullmatch(r'(\d+)([a-z]?)', b)
    if not m:
        raise ValueError(f'bad batch id: {b!r}')
    return int(m.group(1)), m.group(2)


def batch_included(batch, upto):
    """True if `batch` is covered by --upto `upto`. `--upto 2` covers 1a, 1b, 2; `--upto 1a` covers only 1a."""
    bn, bs = batch_key(batch)
    un, us = batch_key(upto)
    if bn != un:
        return bn < un
    return us == '' or bs <= us


def load_removals(path, upto='999'):
    """Returns [(package, batch, reason)] for batches <= upto, in file order."""
    out = []
    for line in open(path):
        if line.startswith('#') or not line.strip():
            continue
        p, b, *rest = line.rstrip('\n').split('\t')
        if batch_included(b, upto):
            out.append((p, b, rest[0] if rest else ''))
    return out


def canon(path):
    """Canonical form of an APK path so manifests.json ('system/system/system_ext/...') and
    libs_features.txt ('/system_ext/...' or '/system/system_ext/...') compare equal."""
    p = path.strip().lstrip('/')
    while p.startswith('system/'):
        p = p[len('system/'):]
    return p


def package_dirs(entries):
    """Directories (relative to the extraction root, e.g. 'system/system/system_ext/priv-app/X')
    that hold a package's APKs."""
    return sorted({e['file'].rsplit('/', 1)[0] for e in entries})
