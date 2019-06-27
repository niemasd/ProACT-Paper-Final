#!/usr/bin/env python3
from gzip import open as gopen
from sys import argv
if len(argv) != 6:
    print("USAGE: %s <clustering_file> <growth_file> <diagnosis> <from_time> <to_time>"%argv[0]); exit()
FROM_TIME = float(argv[4]); TO_TIME = float(argv[5])
if argv[2].endswith('.gz'):
    growth_lines = [l.strip().split('\t') for l in gopen(argv[2]).read().decode().strip().splitlines()]
else:
    growth_lines = [l.strip().split('\t') for l in open(argv[2])]
growth = {int(l[0]):float(l[1]) for l in growth_lines if not l[1].startswith('Growth')}
if argv[1].endswith('.gz'):
    clus_lines = [l.strip().split('\t') for l in gopen(argv[1]).read().decode().strip().splitlines()]
else:
    clus_lines = [l.strip().split('\t') for l in open(argv[1])]
if argv[3].endswith('.gz'):
    diag_lines = gopen(argv[3]).read().decode().strip().splitlines()
else:
    diag_lines = open(argv[3]).read().strip().splitlines()
diag = {l.split('\t')[0].strip().split('|')[1]:float(l.split('\t')[1]) for l in diag_lines}
people = [u for u in diag if diag[u] <= TO_TIME]
p2c = dict()
for u,clus in clus_lines:
    p2c[u] = int(clus)
for u in people:
    if u not in p2c:
        p2c[u] = len(p2c); assert p2c[u] not in growth
        if FROM_TIME < diag[u] <= TO_TIME:
            growth[p2c[u]] = 1
        else:
            growth[p2c[u]] = 0
print('\n'.join(sorted(people, key=lambda x:growth[p2c[x]], reverse=True)))
