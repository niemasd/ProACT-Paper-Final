#!/usr/bin/env python3
from gzip import open as gopen
from sys import argv,stdin
from treeswift import read_tree_newick
if len(argv) != 3:
    print("USAGE: %s <tree_file> <labels_file>"%argv[0]); exit(1)
tree = read_tree_newick(argv[1])
if argv[2] == '-':
    people = {l.strip() for l in stdin}
elif argv[2].lower().endswith('.gz'):
    people = {l.strip() for l in gopen(argv[2]).read().decode().splitlines()}
else:
    people = {l.strip() for l in open(argv[2]).read().splitlines()}
labels = [label for label in tree.labels(internal=False) if label in people or label.split('|')[1] in people]
print(tree.extract_tree_with(labels))
