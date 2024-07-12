import argparse
import gzip
import sys

filename = sys.argv[1]
if filename.endswith('.gz'): fp = gzip.open(filename, 'rt')
else:                        fp = open(filename)

d = {}

header = next(fp)
for line in fp:
	gid, tid, chrom, beg, end = line.split()
	if gid not in d: d[gid] = {}
	if tid not in d[gid]: d[gid][tid] = []
	d[gid][tid].append((int(beg), int(end)))

for gid in d:
	print(gid)
	for tid in d[gid]:
		exons = d[gid][tid]
		if len(exons) == 1: continue # no intron
		print(gid, tid, len(exons))