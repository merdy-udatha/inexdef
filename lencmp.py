from statistics import mean, stdev
import scipy
import sys

exdef = []
indef = []
eother = []
iother = []

with open(sys.argv[1]) as fp:
	for line in fp:
		f = line.split()
		elen = int(f[3]) - int(f[2])
		ilen = int(f[5]) - int(f[4])
		if   ilen > 5000: exdef.append(elen) # exon def
		else:             eother.append(elen)
		
		if elen > 2000: indef.append(ilen)
		else:           iother.append(ilen)
		
	
print(len(exdef), mean(exdef), stdev(exdef), len(eother), mean(eother), stdev(eother))
#print(mean(indef), stdev(indef), mean(iother), stdev(iother))

from scipy import stats
result = stats.ttest_ind(exdef, eother)
print(result.pvalue)

print(len(indef), mean(indef), stdev(indef), len(iother), mean(iother), stdev(iother))
#print(mean(indef), 
result = stats.ttest_ind(indef, iother)
print(result.pvalue)