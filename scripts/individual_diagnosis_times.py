#!/usr/bin/env python3
from gzip import open as gopen
from sys import argv,stdin
if len(argv) != 3:
    print("USAGE: %s <individuals> <full_diagnosis_times>"%argv[0]); exit(1)
if argv[1].lower().endswith('.gz'):
    people = [l.strip() for l in gopen(argv[1]).read().decode().strip().splitlines()]
else:
    people = [l.strip() for l in open(argv[1])]
if argv[2].lower().endswith('.gz'):
    diag_lines = [l.strip().split('\t') for l in gopen(argv[2]).read().decode().strip().splitlines()]
else:
    diag_lines = [l.strip().split('\t') for l in open(argv[2])]
diag = dict()
for l in diag_lines:
    if '|' in l[0]:
        diag[l[0].split('|')[1].strip()] = float(l[1])
    else:
        diag[l[0].strip()] = float(l[1])
for u_orig in people:
    if '|' in u_orig:
        u = u_orig.split('|')[1].strip()
    else:
        u = u_orig.strip()
    print('%s\t%f' % (u,diag[u]))
