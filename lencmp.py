import glob
from statistics import mean, stdev
from scipy import stats
import sys
import re

print('\t'.join( ('genome', 'exdef', 'eother', 'indef', 'iother',
	'exdef_mean', 'exdef_stdev', 'eother_mean', 'eother_stdev',
	'indef_mean', 'indef_stdev', 'iother_mean', 'iother_stdev',
	'exdef_pvalue', 'indef_pvalue')))

for path in glob.glob(f'{sys.argv[1]}/*'):
	m = re.search('(\w\.\w+)\.txt', path)
	name = m.group(1)

	exdef = []
	indef = []
	eother = []
	iother = []
	
	with open(path) as fp:
		for line in fp:
			f = line.split()
			elen = int(f[3]) - int(f[2])
			ilen = int(f[5]) - int(f[4])
			if   ilen > 5000: exdef.append(elen) # exon def
			else:             eother.append(elen)
			
			if elen > 2000: indef.append(ilen)
			else:           iother.append(ilen)
	
	if len(exdef) == 0: continue
	if len(indef) == 0: continue
	
	pe = stats.ttest_ind(exdef, eother).pvalue
	pi = stats.ttest_ind(indef, iother).pvalue
	
	print(name, len(exdef), len(eother), len(indef), len(iother),
		mean(exdef), stdev(exdef),
		mean(eother), stdev(eother), mean(indef), stdev(indef),
		mean(iother), stdev(iother), pe, pi, sep='\t')
