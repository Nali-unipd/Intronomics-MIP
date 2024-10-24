#!/usr/bin/perl -w


open(F,$ARGV[0])||die; # file loci list
$tableType=$ARGV[1];
$DIR=$ARGV[2];
$cutoff=$ARGV[3];

$init=0;
while($r=<F>){
    chomp$r;
    @t=split(/\t/,$r);
    $locus=$t[0];
    $input=$DIR."/L$locus/merged/Results$cutoff/$tableType";
    if(-e $input){
	open(T,$input)||die "can not find file $input";
	while($l=<T>){
	    chomp$l;
	    if($init==0){
		print "$l\n";
		$init=1;
		next;
	    }
	    next if($l=~/^#/);
	    print "L".$locus."_".$l."\n";
	}
    }
    else{
	print STDERR "Locus $locus \n";
    }
}
