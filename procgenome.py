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
"""
exon_len = []
intr_len = []
"""

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

"""

		exon_len.append(e1e-e1b+1)
		if e2e < e1b: 
			intr_len.append(e1b-e2e+1)
		else: 
			intr_len.append(ie-ib+1)
		if (ib > ie): 
			print(gid, tid, e1b, e1e, ib, ie, e2b, e2e)
			# sys.exit('ERROR: negative strand length')

print(intr_len)

def mean(list): 
	total = 0
	for v in list: 
		total += list[v]
	return total/len(list)


print(mean(intr_len), len(intr_len))
print(mean(exon_len), len(exon_len))


rel_list = []
def rel_len(list):
	small = 100 
	for i in list:
		if i <= small: 
			rel_list.append(list[i+1])
	return rel_list
rel_len(exon_len)

<<<<<<< HEAD
print(mean(rel_list), len(rel_list))
			
			
=======
print()
print(f'Mean of intron lengths: {mean(intr_len):.3f}')
print(f'Mean of exon lengths:   {mean(exon_len):.3f}')
print()
print(f'{rel_len(exon_len)}')

"""
>>>>>>> 9ef4013998014ccc7ccc1b6f9737493181f34417
