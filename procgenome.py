import argparse
import gzip
import sys

def lohi(exons):
	lo = exons[0][0]
	hi = exons[0][1]
	for beg, end in exons:
		if beg < lo: lo = beg
		if end > hi: hi = end
	return lo, hi



# open file
filename = sys.argv[1]
if filename.endswith('.gz'): fp = gzip.open(filename, 'rt')
else:                        fp = open(filename)
header = next(fp)

# gather data into gene->tx->exons
d = {}
for line in fp:
	gid, tid, chrom, beg, end = line.split()
	if gid not in d: d[gid] = {}
	if tid not in d[gid]: d[gid][tid] = []
	d[gid][tid].append((int(beg), int(end)))

# reorganize data
for gid in d:
	#print(gid)
	for tid in d[gid]:
		exons = d[gid][tid]
		if len(exons) == 1: continue # no intron
		beg, end = lohi(exons)
		size = end - beg + 1
		print(gid, tid, len(exons), size, beg, end)

# no double-counts, use first?
# probably already sorted given the order
# 3 columns exon.len intron.len exon.len
