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
	if tid not in d[gid]: d[gid][tid] = {}
	d[gid][tid][(int(beg), int(end))] = True

# reorganize data
# keep only the first transcript in the group
# report the coordinates of exon1-intron-exon2
for gid in d:
	tid = list(d[gid].keys())[0]
	exons = list(d[gid][tid].keys())
	exons.sort(key=lambda tup: tup[0])
	
	if len(exons) == 1: continue # no intron
	if exons[0][0] > exons[1][0]: exons = list(reversed(exons)) # neg strand
	
	for i in range(len(exons) -1):
		e1b, e1e = exons[i]
		e2b, e2e = exons[i+1]
		ib = e1e+1
		ie = e2b-1
		if (ib > ie): sys.exit('ERROR: negative strand length')			
		print(f'{gid}\t{tid}\t{e1b}\t{e1e}\t{ib}\t{ie}\t{e2b}\t{e2e}')