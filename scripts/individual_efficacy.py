#!/usr/bin/env python3
from gzip import open as gopen
from sys import argv
if len(argv) != 4:
    print("USAGE: %s <people_list> <transmission_network> <time>"%argv[0]); exit()
END = float(argv[3])
if argv[2].endswith('.gz'):
    trans = [l.split('\t') for l in gopen(argv[2]).read().decode().strip().splitlines()]
else:
    trans = [l.split('\t') for l in open(argv[2]).read().strip().splitlines()]
if argv[1].endswith('.gz'):
    people = [l.strip() for l in gopen(argv[1]).read().decode().strip().splitlines()]
else:
    people = [l.strip() for l in open(argv[1])]
if '|' in people[0]:
    people = [u.split('|')[1] for u in people]
num_trans = {u:0 for u in people}
for u,v,t in trans:
    if u in num_trans and float(t) > END:
        num_trans[u] += 1
try:
    for u in people:
        print('%s\t%d' % (u,num_trans[u]))
except BrokenPipeError:
    exit()
