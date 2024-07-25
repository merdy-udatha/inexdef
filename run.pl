
my @file = `find genomes/*/*.gz`;
chomp @file;
foreach my $file (@file) {
	my ($name) = $file =~ /(\w\.\w+)\.gz/;
	print STDERR "working on $file\n";
	my $out1 = "triples/$name.txt";
	if (-s $out1 < 100) {
		system("python3 procgenome.py $file > triples/$name.txt") == 0 or die;
	} else {
		print STDERR "$out1 already exists, skipping\n";
	}
	my $out2 = "graphs/scatter_plots/randomdict/$name\_scatterplt.png";
	if (-s $out2 < 100) {
		system("python3 randomscatter.py triples/$name.txt $name $out2") == 0 or die;
	} else {
		print STDERR "$out2 already exists, skipping\n";
	}
}
	