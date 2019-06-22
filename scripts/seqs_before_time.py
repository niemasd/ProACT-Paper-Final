#!/usr/bin/env python3
from gzip import open as gopen
from sys import argv
if len(argv) != 4:
    print("USAGE: %s <seqs> <sample_times> <time>"%argv[0]); exit()
END = float(argv[3])
if argv[2].endswith('.gz'):
    diag_lines = gopen(argv[2]).read().decode().strip().splitlines()
else:
    diag_lines = open(argv[2]).read().strip().splitlines()
diag = {l.split('\t')[0].strip():float(l.split('\t')[1]) for l in diag_lines}
if argv[1].endswith('.gz'):
    seq_lines = gopen(argv[1]).read().decode().strip().splitlines()
else:
    seq_lines = open(argv[1]).read().strip().splitlines()
for i in range(0, len(seq_lines), 2):
    if diag[seq_lines[i][1:]] <= END:
        print(seq_lines[i]); print(seq_lines[i+1])
