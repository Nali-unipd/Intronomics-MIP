#!/usr/bin/perl -w


$selectedClustersInfo=$ARGV[0];
$table=$ARGV[1];

open(F, "gunzip -c $selectedClustersInfo |");
while($r=<F>){
    chomp$r;
    @t=split(/\t/,$r);
    $t[0]=~s/\_\d+//;
    $key=$t[0]."-".$t[2];
    $Nreads{$key}=$t[25];
}


open(F,$table)||die "Cannot open file $table\n" ;
while($r=<F>){
    chomp$r;
    if ($r=~/#/){
	print "$r\n";
	@header=split(/\t/,$r);
	next;
    }
    @t=split(/\t/,$r);
    print "$t[0]";
    for($col=1;$col<=$#t;$col++){
	$key=$header[$col]."-".$t[0];
	if($t[$col]!=0){
	    print "\t$Nreads{$key}";
	}
	else{
	    print "\t0";
	}
    }
    print "\n";
}
