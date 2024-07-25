import argparse
import gzip
import statistics
import sys
import matplotlib.pyplot as plt
import numpy as np

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
	
x = np.array(dataset['Intron'])
y = np.array(dataset['Exon1'])
plt.scatter(x, y, s=1, color = 'red')


x = np.array(dataset['Intron'])
y = np.array(dataset['Exon2'])
plt.scatter(x, y, s=1, color = 'blue')


plt.title(f'{arg.genome}', fontsize = 18)

# plt.show()
#Display the plot
plt.savefig(f'graphs/scatter_plots_png/without_labels/{arg.genome}_scatterplt.png')