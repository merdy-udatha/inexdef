import argparse
import gzip
import sys

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
# keep only the first transcript in the group
# report the coordinates of exon1-intron-exon2
exon_len = []
intr_len = [] 
for gid in d:
	tid = list(d[gid].keys())[0]
	exons = d[gid][tid]
	if len(exons) == 1: continue # no intron
	if exons[0][0] > exons[1][0]: exons = list(reversed(exons)) # neg strand
	
	for i in range(len(exons) -1):
		e1b, e1e = exons[i]
		e2b, e2e = exons[i+1]
		ib = e1e+1
		ie = e2b-1
		exon_len.append(e1e-e1b+1)
		intr_len.append(ie-ib+1)
		print(gid, tid, e1b, e1e, ib, ie, e2b, e2e)
		if (ib > ie): sys.exit('ERROR: negative strand length')
print(intr_len)

def mean(list):
	total_sum = 0 
	for i in list: 
		total_sum += list[i]
	return total_sum/len(list)
print()
print(f'Mean of intron lengths: {mean(intr_len):.3f}')
print(f'Mean of exon lengths:   {mean(exon_len):.3f}')
