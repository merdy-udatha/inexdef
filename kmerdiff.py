import argparse
import math

def kmers(path, k):
	counts = {}
	total = 0
	with open(path) as fp:
		for seq in fp:
			if seq.startswith('>'): continue
			seq = seq.upper()
			for i in range(len(seq) - k):
				kmer = seq[i:i+k]
				if kmer not in counts: counts[kmer] = 0
				counts[kmer] += 1
				total += 1
	probs = {}
	for kmer, n in counts.items():
		probs[kmer] = n / total
	
	return probs
				

parser = argparse.ArgumentParser(description='K-mer distance computer')
parser.add_argument('file1', help='sequences raw format')
parser.add_argument('file2', help='sequences raw format')
parser.add_argument('-k', '--kmer', type=int, default=5,
	help='kmer size [ %(default)i ]')
arg = parser.parse_args()

k1s = kmers(arg.file1, arg.kmer)
k2s = kmers(arg.file2, arg.kmer)

for kmer in k1s:
	if kmer not in k2s: continue
	print(kmer, math.log2(k1s[kmer]/k2s[kmer]))