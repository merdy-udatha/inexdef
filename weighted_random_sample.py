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
			counts[kmer] += 1 /len(seq)
			total += 1/len(seq)
	probs = {}
	for kmer, n in counts.items():
		probs[kmer] = n / total
	
	return probs

eseqs = readseqs('ce.idef.fasta')
iseqs = readseqs('ce.edef.fasta')

kdiff = {}

for i in range(100):
	set1 = []
	set2 = []
	nseqs = 200
	
	for i in range(nseqs):
		s1 = random.choice(eseqs)
		s2 = random.choice(iseqs)
		if random.random() < 0.5:
			set1.append(s1)
			set2.append(s2)
		else:
			set1.append(s2)
			set2.append(s1)
	k1s = kmers(set1, 5)
	k2s = kmers(set2, 5)
	
	for kmer in k1s:
		if kmer not in k2s: continue
		if kmer not in kdiff: kdiff[kmer] = []
		kdiff[kmer].append(math.log2(k1s[kmer]/k2s[kmer]))

observed = {}
with open('ce.kmerdiff.txt') as fp:
	for line in fp:
		kmer, diff = line.split()
		observed[kmer] = float(diff)


for kmer in kdiff:
	m = statistics.mean(kdiff[kmer])
	s = statistics.stdev(kdiff[kmer])
	d = abs(observed[kmer] - m) / s
	print(kmer, m, s, observed[kmer], d, sep='\t')

