import argparse
from grimoire.genome import Reader
import sys

def write_fasta(filename, inex, seqs):
	with open(f'{filename}.{inex}.fasta', 'w') as fp:
		for i, seq in enumerate(seqs):
			fp.write(f'>{inex}.{i}\n{seq}\n')

parser = argparse.ArgumentParser(description='Select short/long seqs')
parser.add_argument('fasta', help='number of features to generate')
parser.add_argument('gff', help='number of features to generate')
parser.add_argument('out', help='output name')
parser.add_argument('--exondef-emax', type=int, default=500,
	help='number of chromosomes [%(default)i]')
parser.add_argument('--exondef-imin', type=int, default=5000,
	help='number of chromosomes [%(default)i]')
parser.add_argument('--introndef-emin', type=int, default=2000,
	help='number of chromosomes [%(default)i]')
parser.add_argument('--introndef-imax', type=int, default=1000,
	help='number of chromosomes [%(default)i]')
arg = parser.parse_args()


edef_seq = []
idef_seq = []

for chrom in Reader(fasta=arg.fasta, gff=arg.gff):
	genes = chrom.ftable.build_genes()
	for gene in genes:
		if len( gene.transcripts()) == 0: continue
		tx = gene.transcripts()[0]
		for exon, intron in zip(tx.exons, tx.introns):
			if exon.length < arg.exondef_emax and intron.length > arg.exondef_imin:
				edef_seq.append(exon.seq_str())
			if exon.length > arg.introndef_emin and intron.length < arg.introndef_imax:
				idef_seq.append(exon.seq_str())

write_fasta(arg.out, 'edef', edef_seq)
write_fasta(arg.out, 'idef', idef_seq)

