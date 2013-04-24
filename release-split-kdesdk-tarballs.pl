use strict;
use warnings;

my @packages = ('cervisia', 'dolphin-plugins', 'kapptemplate', 'kcachegrind', 'kdesdk-kioslaves', 'kdesdk-strigi-analyzers', 'kdesdk-thumbnailers', 'kompare', 'lokalize', 'okteta', 'poxml', 'umbrello', 'amor', 'kteatime', 'ktux');

my $version = '4.10.2';

open my $rev_n_hashes, "C:\\Users\\patrick\\Downloads\\revisions_and_hashes-4.10.2.txt";
my @revisions = <$rev_n_hashes>;
#my @revisions = $rev_n_hashes;
#for my $line ($rev_n_hashes) {
#    print ">".$line."\n";
#};

#my @revisions = qw( bla blub );
#print @revisions;

for my $package (@packages) {
    my $cmd;
    print $package."\n";
    my ($line) = grep { chomp; /$package/; } (@revisions);
    $line =~ s/^[^ ]* ([0-9a-f]*).*$/$1/;
    $cmd = "cd $package && git archive --prefix=$package-$version/ $line | xz > ../$package-$version.tar.xz && cd ..";
#    $cmd = "cd $package && git fetch && cd ..";
    system($cmd);
};

close $rev_n_hashes;
