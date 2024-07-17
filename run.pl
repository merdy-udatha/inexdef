
my @file = `find genomes/*/*.gz`;
chomp @file;
foreach my $file (@file) {
	my @out = `python3 procgenome.py $file`;
	print "$file: ", scalar(@out), "\n";
}