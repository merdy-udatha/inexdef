
import matplotlib.pyplot as plt
import numpy as np
import sys

# expects filepath and genome as sys.argv[1] and sys.argv[2]
genome = sys.argv[2]

e1lens = []
e2lens = []
ilens = []
with open(sys.argv[1]) as fp:
	for line in fp:
		gid, tid, e1b, e1e, ib, ie, e2b, e2e = line.split()
		e1lens.append(int(e1e) - int(e1b) + 1)
		e2lens.append(int(e2e) - int(e2b) + 1)
		ilens.append(int(ie) - int(ib) + 1)
	
dataset = {
	'Exon1': e1lens,
	'Exon2': e2lens,
	'Intron': ilens,
}

for name, data in dataset.items():

	# Plotting a basic histogram
	plt.hist(data, bins=100, color='skyblue', edgecolor='black')
	
	# Adding labels and title
	plt.xlabel(f'{name} length (bp)')
	plt.ylabel('Frequency')
	plt.title(f'{name} Length in {genome}')

	# Display the plot
	plt.show()
	# plt.savefig(f'graphs/{genome}:{name}.pdf')
