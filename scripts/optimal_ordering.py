#!/usr/bin/env python3
from gzip import open as gopen
from sys import argv
if len(argv) != 5:
    print("USAGE: %s <sequence_file> <transmission_network> <sample_times> <time>"%argv[0]); exit()
END = float(argv[4])
if argv[3].endswith('.gz'):
    diag_lines = gopen(argv[3]).read().decode().strip().splitlines()
else:
    diag_lines = open(argv[3]).read().strip().splitlines()
diag = {l.split('\t')[0].strip():float(l.split('\t')[1]) for l in diag_lines}
if argv[2].endswith('.gz'):
    trans = [l.split('\t') for l in gopen(argv[2]).read().decode().strip().splitlines()]
else:
    trans = [l.split('\t') for l in open(argv[2]).read().strip().splitlines()]
if argv[1].endswith('.gz'):
    people = [l.split('\t')[0][1:] for l in gopen(argv[1]).read().decode().strip().splitlines() if l[0] == '>']
else:
    people = [l.split('\t')[0][1:] for l in open(argv[1]) if l[0] == '>']
num_trans = {u.split('|')[1]:0 for u in people if diag[u] <= END}
for u,v,t in trans:
    if u in num_trans and float(t) > END:
        num_trans[u] += 1
print('\n'.join(sorted(num_trans.keys(), key=lambda x: num_trans[x], reverse=True)))
