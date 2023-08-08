#!/usr/bin/perl

use strict;
use warnings;

my %seqs;
$/ = "\n>"; # read fasta by sequence, not by lines

while (<>) {
    s/>//g;
    my ($seq_id, @seq) = split (/\n/, $_);
    my $seq = uc(join "", @seq); # rebuild sequence as a single string
    my $len = length $seq;
    my $numA = $seq =~ tr/A//; # removing A's from sequence returns total counts
    my $numC = $seq =~ tr/C//;
    my $numG = $seq =~ tr/G//;
    my $numT = $seq =~ tr/T//;
    my $numN = $seq =~ tr/N//;
    print "$seq_id $len $numN\n";
}


# run example 
perl masked_stats.pl top10_uniq_plant_contigs_id1e5_short_header.fa.masked > top10_uniq_plant_contigs_id1e5_short_header.fa.masked.stats

perl masked_stats.pl no_hit_masked_all.fasta > no_hit_masked_all.fasta.stats
