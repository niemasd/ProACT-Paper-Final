#!/usr/bin/env python3
'''
For each individual, compute the number of people infected by the individual's neighbors
'''
from gzip import open as gopen
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--individuals', required=False, type=str, default='stdin', help="Individuals (one per line)")
parser.add_argument('-c', '--contacts', required=True, type=str, help="Contact Network (FAVITES format)")
parser.add_argument('-tn', '--transmissions', required=True, type=str, help="Transmission Network (FAVITES format)")
parser.add_argument('-t', '--from_time', required=True, type=float, help="From Time")
parser.add_argument('-tt', '--to_time', required=False, type=float, default=float('inf'), help="To Time")
args = parser.parse_args()
assert args.to_time > args.from_time, "To Time must be larger than From Time"
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
if args.transmissions.endswith('.gz'):
    args.transmissions = gopen(args.transmissions).read().strip().decode().splitlines()
else:
    args.transmissions = open(args.transmissions).read().strip().splitlines()

# load FAVITES transmission network
trans = []; nodes = set()
for line in args.transmissions:
    if isinstance(line,bytes):
        l = line.decode().strip()
    else:
        l = line.strip()
    try:
        u,v,t = l.split(); t = float(t)
    except:
        raise RuntimeError("Invalid transmission network")
    if u not in nodes:
        nodes.add(u)
    if v not in nodes:
        nodes.add(v)
    trans.append((u,v,t))

# load user's individuals
user_individuals = list()
for line in args.individuals:
    if isinstance(line,bytes):
        l = line.decode().strip()
    else:
        l = line.strip()
    assert l in nodes, "Individual not in transmission network: %s"%l
    user_individuals.append(l)
user_individuals_set = set(user_individuals)

# compute neighbors of each individual
neighbors = dict()
for l in args.contacts:
    if len(l.strip()) == 0 or l[0] == '#':
        continue
    parts = l.strip().split('\t')
    if len(parts) == 3 and parts[0].strip() == 'NODE':
        if parts[1] not in neighbors:
            neighbors[parts[1]] = set()
    elif len(parts) == 5 and parts[0].strip() == 'EDGE':
        dummy,u,v,attributes,directionality = parts # HIV, so assume all are undirected
        if u not in neighbors:
            neighbors[u] = set()
        if v not in neighbors:
            neighbors[v] = set()
        if u in user_individuals_set:
            neighbors[v].add(u)
        if v in user_individuals_set:
            neighbors[u].add(v)
    else:
        raise RuntimeError("Invalid contact network")

# compute total number infected by neighbors
num_infected_by_neighbors = {u:0 for u in user_individuals}
for u,v,t in trans:
    if t >= args.from_time and t <= args.to_time and u in num_infected_by_neighbors:
        for neighbor in neighbors[u]:
            if neighbor in user_individuals_set:
                num_infected_by_neighbors[neighbor] += 1
for u in user_individuals:
    print("%s\t%d" % (u,num_infected_by_neighbors[u]))
