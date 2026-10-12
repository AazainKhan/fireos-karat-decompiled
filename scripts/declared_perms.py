#!/usr/bin/env python3
"""Sorted names of every permission declared by a package in the image.
Usage: declared_perms.py <manifests.json> > config/declared-permissions.txt
privapp_xml.py --declared-from reads that list to drop names this Android 11 image does not know."""
import json, sys
M = json.load(open(sys.argv[1]))
print('\n'.join(sorted({pr for es in M.values() for e in es for pr in e['decl_perm']})))
