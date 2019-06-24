#!/usr/bin/env python3
from gzip import open as gopen
from sys import argv
if len(argv) != 5:
    print("USAGE: %s <clustering_file> <diag_file> <from_time> <to_time>"%argv[0]); exit()
FROM_TIME = float(argv[3]); TO_TIME = float(argv[4])
assert FROM_TIME < TO_TIME, "from_time must be less than to_time"
if argv[2].endswith('.gz'):
    diag_lines = gopen(argv[2]).read().decode().strip().splitlines()
else:
    diag_lines = open(argv[2]).read().strip().splitlines()
diag = {l.split('\t')[0].strip().split('|')[1]:float(l.split('\t')[1]) for l in diag_lines}
if argv[1].endswith('.gz'):
    clus_lines = [l.strip().split('\t') for l in gopen(argv[1]).read().decode().strip().splitlines()]
else:
    clus_lines = [l.strip().split('\t') for l in open(argv[1])]
from_size = dict(); to_size = dict(); clusters = set()
for u,clus in clus_lines:
    c = int(clus); clusters.add(c)
    for t,d in [(FROM_TIME,from_size), (TO_TIME,to_size)]:
        if diag[u] <= t:
            if c in d:
                d[c] += 1
            else:
                d[c] = 1
print('Cluster\tGrowthRate')
for c in sorted(clusters):
    if c in from_size:
        n1 = from_size[c]
    else:
        n1 = 0
    if c in to_size:
        n2 = to_size[c]
    else:
        n2 = 0
    if n2 == 0: # n1 must also be 0 (clusters can only grow)
        g = 0
    else:
        g = (n2-n1)/(n2**0.5)
    print('%d\t%f' % (c,g))
