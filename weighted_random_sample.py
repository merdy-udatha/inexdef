import math
import random
import statistics

def readseqs(path):
	seqs = []
	with open(path) as fp:
		for seq in fp:
			if seq.startswith('>'): continue
			seq = seq.upper()
			seqs.append(seq)
	return seqs

def kmers(seqs, k):
	counts = {}
	total = 0
	for seq in seqs:
		for i in range(len(seq) - k):
			kmer = seq[i:i+k]
			if kmer not in counts: counts[kmer] = 0
			counts[kmer] += 1/len(seq)
			total += 1/len(seq)
	probs = {}
	for kmer, n in counts.items():
		probs[kmer] = n / total
	
	return probs

seqs = readseqs('default.edef.fasta')
seqs.extend('default.idef.fasta')

kdiff = {}

for i in range(100):
	set1 = {}
	set2 = {}
	nseqs = 200
	
	while len(set1.keys()) < nseqs:
		s1 = random.choice(seqs)
		s2 = random.choice(seqs)
		if s1 == s2: continue
		if s1 in set1: continue
		if s1 in set2: continue
		if s2 in set1: continue
		if s2 in set2: continue
		set1[s1] = True
		set2[s2] = True
	
	seqs1 = list(set1.keys())
	seqs2 = list(set2.keys())
	
	k1s = kmers(seqs1, 5)
	k2s = kmers(seqs2, 5)
	
	for kmer in k1s:
		if kmer not in k2s: continue
		if kmer not in kdiff: kdiff[kmer] = []
		kdiff[kmer].append(math.log2(k1s[kmer]/k2s[kmer]))

for kmer in kdiff:
	print(kmer, statistics.mean(kdiff[kmer]), statistics.stdev(kdiff[kmer]))
