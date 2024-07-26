import argparse
import gzip
import statistics
import sys
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Graphing program')
parser.add_argument('triples', help='triples file')
parser.add_argument('genome', help='name of genome')
parser.add_argument('--cutoff', type=float, default=30,
	help='z-score cutoff [%(default)f]')
arg = parser.parse_args()

e1lens = []
e2lens = []
ilens = []
with open(arg.triples) as fp:
	for line in fp:
		gid, tid, e1b, e1e, ib, ie, e2b, e2e = line.split()
		e1lens.append(int(e1e) - int(e1b) + 1)
		e2lens.append(int(e2e) - int(e2b) + 1)
		ilens.append(int(ie) - int(ib) + 1)

# filtered data = 3 groups: short exon next to long intron, long exon, don't care dataset = {
dataset = {
	'shortex_longin': [],
	'longex': [],
	'dontcare': [],
}

emean = statistics.mean(e1lens)
estd  = statistics.stdev(e1lens)
imean = statistics.mean(ilens)
istd  = statistics.stdev(ilens)

small_cutoff = 1
big_cutoff = 15
for e1, e2, il in zip(e1lens, e2lens, ilens):
	z1 = abs(e1 - emean) / estd
	z2 = abs(e2 - emean) / estd
	z3 = abs(il - imean) / istd
	if z1 > big_cutoff:
		dataset['longex'].append(e1)
	elif z2 > big_cutoff: 
		dataset['longex'].append(e2)
	elif z1 < small_cutoff and z3 > big_cutoff:
		dataset['shortex_longin'].append(il)
	elif z2 < small_cutoff and z3 > big_cutoff:
		dataset['shortex_longin'].append(il)
	else: dataset['dontcare'].append(e1)
	
print(dataset['longex'])
print(dataset['shortex_longin'])

