import argparse
import gzip
import statistics
import sys
import matplotlib.pyplot as plt
import numpy as np
import random 


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

# filtered data
dataset = {
	'Exon1': [],
	'Exon2': [],
	'Intron': [],
}

emean = statistics.mean(e1lens)
estd  = statistics.stdev(e1lens)
imean = statistics.mean(ilens)
istd  = statistics.stdev(ilens)

skipped = 0
for e1, e2, il in zip(e1lens, e2lens, ilens):
	z1 = abs(e1 - emean) / estd
	z2 = abs(e2 - emean) / estd
	z3 = abs(il - imean) / istd
	if z1 > arg.cutoff or z2 > arg.cutoff or z3 > arg.cutoff:
		skipped += 1
		continue
	dataset['Exon1'].append(e1)
	dataset['Exon2'].append(e2)
	dataset['Intron'].append(il)

		
set1 = {}
set2 = {}	
while len(set1.keys()) <  len(dataset['Intron']):
	s1 = random.choice(dataset['Intron'])
	s2 = random.choice(dataset['Exon1'])
	if s1 in set1: continue
	if s2 in set2: continue
	set1[s1] = True
	set2[s2] = True
	x = s1 
	y = s2
	plt.scatter(x, y, s=1, color = 'black')


"""
x = np.array(dataset['Intron'])
y = np.array(dataset['Exon2'])
plt.scatter(x, y, s=1, color = 'blue')
"""
plt.xlabel("Intron Length (bp)")
plt.ylabel("Exon Length (bp)")
plt.title(f'{arg.genome}', fontsize = 18)

# plt.show()
# Display the plot
plt.savefig(f'graphs/scatter_plots/randomdict/{arg.genome}_scatterplt.png')

"""

randintron = []
randexon = []
for i in range(len(dataset['Intron'])):  
		ri = random.choice(dataset['Intron'])
		re = random.choice(dataset['Exon1'])
		if ri not in randintron: 
			randintron.append(random.choice(dataset['Intron']))
			x = ri
		if re not in randexon: 
			randexon.append(random.choice(dataset['Exon1']))
			y = re 
		else: continue 
"""