
my @file = `find genomes/*/*.gz`;
chomp @file;
foreach my $file (@file) {
	my ($name) = $file =~ /(\w\.\w+)\.gz/;
	print STDERR "working on $file\n";
	my $out = "triples/$name.txt";
	if (-s $out < 100) {
		system("python3 procgenome.py $file > triples/$name.txt") == 0 or die;
	} else {
		print STDERR "$out already exists, skipping\n";
	}
	system("python3 graphgenome.py $out $name") == 0 or die;
}