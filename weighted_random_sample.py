import argparse
import gzip
import math
import random
import statistics

def readseqs(path):
	seqs = []
	if path.endswith('.gz'): fp = gzip.open(path, 'rt')
	else: fp = open(path)
	for seq in fp:
		if seq.startswith('>'): continue
		seq = seq.upper()
		seqs.append(seq)
	fp.close()
	return seqs

def kmers(seqs, k):
	counts = {}
	total = 0
	for seq in seqs:
		for i in range(len(seq) - k):
			kmer = seq[i:i+k]
			if kmer not in counts: counts[kmer] = 0
			counts[kmer] += 1 /len(seq)
			total += 1/len(seq)
	probs = {}
	for kmer, n in counts.items():
		probs[kmer] = n / total
	
	return probs

parser = argparse.ArgumentParser(description='weighted random thing')
parser.add_argument('edef', help='file of edef seqs')
parser.add_argument('idef', help='file of idef seqs')
parser.add_argument('--k', type=int, default=5)
parser.add_argument('--iterations', type=int, default=100)
arg = parser.parse_args()


eseqs = readseqs(arg.edef)
iseqs = readseqs(arg.idef)

kdiff = {}

for i in range(arg.iterations):
	set1 = []
	set2 = []
	nseqs = min(len(eseqs), len(iseqs))
	
	for i in range(nseqs):
		s1 = random.choice(eseqs)
		s2 = random.choice(iseqs)
		if random.random() < 0.5:
			set1.append(s1)
			set2.append(s2)
		else:
			set1.append(s2)
			set2.append(s1)
	k1s = kmers(set1, arg.k)
	k2s = kmers(set2, arg.k)
	
	for kmer in k1s:
		if kmer not in k2s: continue
		if kmer not in kdiff: kdiff[kmer] = []
		kdiff[kmer].append(math.log2(k1s[kmer]/k2s[kmer]))

k1s = kmers(eseqs, arg.k)
k2s = kmers(iseqs, arg.k)
observed = {}
for kmer in k1s:
	if kmer not in k2s: continue
	observed[kmer] = math.log2(k1s[kmer]/k2s[kmer])

for kmer in kdiff:
	m = statistics.mean(kdiff[kmer])
	s = statistics.stdev(kdiff[kmer])
	d = abs(observed[kmer] - m) / s
	print(kmer, m, s, observed[kmer], d, math.log2(k1s[kmer]/k2s[kmer]), sep='\t')

