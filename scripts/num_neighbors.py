#!/usr/bin/env python3
'''
For each individual, compute the number of the neighbors the individual has (in the contact network)
'''
from gzip import open as gopen
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--individuals', required=False, type=str, default='stdin', help="Individuals (one per line)")
parser.add_argument('-c', '--contacts', required=True, type=str, help="Contact Network (FAVITES format)")
args = parser.parse_args()
if args.individuals == 'stdin':
    from sys import stdin; args.individuals = stdin.read().strip().splitlines()
elif args.individuals.endswith('.gz'):
    args.individuals = gopen(args.individuals).read().strip().decode().splitlines()
else:
    args.individuals = open(args.individuals).read().strip().splitlines()
if args.contacts.endswith('.gz'):
    args.contacts = gopen(args.contacts).read().strip().decode().splitlines()
else:
    args.contacts = open(args.contacts).read().strip().splitlines()

# compute number of neighbors per individual
num_neighbors = dict()
for l in args.contacts:
    if len(l.strip()) == 0 or l[0] == '#':
        continue
    parts = l.strip().split('\t')
    if len(parts) == 3 and parts[0].strip() == 'NODE':
        num_neighbors[parts[1].strip()] = 0
    elif len(parts) == 5 and parts[0].strip() == 'EDGE':
        u,v = [x.strip() for x in parts[1:3]]
        num_neighbors[u] += 1; num_neighbors[v] += 1
    else:
        raise RuntimeError("Invalid contact network")

# load user's individuals
user_individuals = list()
for line in args.individuals:
    if isinstance(line,bytes):
        l = line.decode().strip()
    else:
        l = line.strip()
    assert l in num_neighbors, "Individual not in contact network: %s"%l
    user_individuals.append(l)

# output number of neighbos for each individual
for u in user_individuals:
    print("%s\t%d" % (u,num_neighbors[u]))
