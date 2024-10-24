#!/usr/bin/perl -w

$table=$ARGV[0];
$fasta=$ARGV[1];
$lista_individui=$ARGV[2];
$cutoff=$ARGV[3];

$fileTableFilt=$ARGV[0];
$fileTableFilt=~s/\.txt/\.filtered\.txt/;
open(FILTT,">$fileTableFilt");

$fileTableComp=$ARGV[0];
$fileTableComp=~s/\.txt/\.full\.txt/;
open(COMP,">$fileTableComp");


## Reading the Haplotype matrix table
open(F,$table)||die "Cannot open file $table\n" ;
$count=0;
while($r=<F>){
    chomp$r;
    next if $r=~/Exported/;
    $r=~s/\"//g;
    @t=split(/\t/,$r);
    $ncol=$#t;
    for($i=0; $i<=$#t; $i++){
	if($count==0){
	    $t[$i]=~s/_\d+//;
	    $IndPos{$t[$i]}=$i;
	}
	$matrix[$count][$i]=$t[$i];
	#print " >>>> $matrix[$count][$i]\n";
    }
    $count++;
}
$ncol=$#t;
$nrow=$count-1;


# First check that all samples are present, otherwise add the missing samples.


open(I,$lista_individui)||die "Cannot open $lista_individui\n" ;
while($r=<I>){
    chomp$r;
    @t=split(/_/,$r);
    $t[0]=~s/Ind//;
    push(@ALLIND,$t[0]);
}
@ALLIND=sort{$a<=>$b}(@ALLIND);
for($a=0;$a<=$#ALLIND; $a++){
    $ALLIND[$a]="Ind".$ALLIND[$a];
}


for($row=1; $row<=$nrow; $row++){
    $newmatrix[$row][0]=$matrix[$row][0];
}
$newmatrix[0][0]=$matrix[0][0];
$col=0;
for($a=0; $a<=$#ALLIND; $a++){
    $col++;
    $newmatrix[0][$col]=$ALLIND[$a];
    if($IndPos{$ALLIND[$a]}){
	for($row=1; $row<=$nrow; $row++){
	    $newmatrix[$row][$col]=$matrix[$row][$IndPos{$ALLIND[$a]}];
	}
    }
    else{
	for($row=1; $row<=$nrow; $row++){
            $newmatrix[$row][$col]=0;
        }
    }
}
$ncol=$col;
@matrix=@newmatrix;


#print "NCOL: $ncol $#ALLIND\n";


print COMP "$matrix[0][0]";
for($col=1; $col<=$ncol; $col++){
    print COMP "\t$matrix[0][$col]";
}
print COMP  "\n";

for($row=1; $row<=$nrow; $row++){
    print COMP "$matrix[$row][0]";
    for($col=1; $col<=$ncol; $col++){
	print COMP  "\t".$matrix[$row][$col];
    }
    print COMP "\n";
}




for($col=1; $col<=$ncol; $col++){
    for($row=1; $row<=$nrow; $row++){
	#print "--- $matrix[$row][0]  $matrix[$row][$col]\n";
	$vals{$matrix[$row][0]}=$matrix[$row][$col]
    }
    print STDERR ">Summary for $matrix[0][$col]\n";
    %keep=&Filter(%vals);
    $OK=0;
    for($row=1; $row<=$nrow; $row++){
	if($matrix[$row][$col]>0){
	    if(!$keep{$matrix[$row][0]}){
		print STDERR "Setting to 0 Haplotype $matrix[$row][0] : $matrix[$row][$col]\n";
		$matrix[$row][$col]=0;
		#$OK=1;
	    }
	    else{
		print STDERR "Keeping Haplo $matrix[$row][0] : $matrix[$row][$col]\n";
	    }
	    $OK=1;
	}
    }
    if($OK==0){
	print STDERR "No haplotypes founds becouse of all the reads were filtered\n";
    }
    print STDERR "\n";
}

print FILTT "$matrix[0][0]";
for($col=1; $col<=$ncol; $col++){
    print FILTT "\t$matrix[0][$col]";
}
print FILTT "\n";

for($row=1; $row<=$nrow; $row++){
    $somma=0;
    $str="";
    for($col=1; $col<=$ncol; $col++){
	$somma+=$matrix[$row][$col];
	$str.="\t".$matrix[$row][$col]
    }
    if($somma>0){
	print FILTT "$matrix[$row][0]$str\n";
    }
    else{
	$HaploToDelete{$matrix[$row][0]}="ok";
    }
}


$fileKeep=$fasta;
$fileKeep=~s/\.fasta/\.keep\.fasta/;

$fileFilt=$ARGV[1];
$fileFilt=~s/\.fasta/\.filtered\.fasta/;

open(KEEP,">$fileKeep");
open(FILT,">$fileFilt");

open(S,$ARGV[1])||die;
while($r=<S>){
    chomp$r;
    if($r=~/^>/){
	$r=~s/>//;
	$id=$r;
	next;
    }
    $seq{$id}.=$r;
}

print STDERR "HaploSeq:\n";
foreach $k(keys(%seq)){
    if($HaploToDelete{$k}){
	print STDERR "$k\tRemoved\n";
	print FILT ">$k\n$seq{$k}\n";
    }
    else{
	print KEEP ">$k\n$seq{$k}\n";
	print STDERR "$k\tKept\n";
    }
}






sub Filter(){
    my(%hash)=@_;
    my($somma)=0;
    my(%keep);
    #$somma=0;
    #foreach my $k (sort { $hash{$b} <=> $hash{$a} } keys %hash) {
	#$somma+=$hash{$k};
    #}
    #$cutoff=0.8;
    #$somma=0;
    foreach my $k (sort { $hash{$b} <=> $hash{$a} } keys %hash) {
	#print "$k  $hash{$k}\n";
	if($hash{$k}>0){
	    $somma+=$hash{$k};
	    #print "$somma\t$cutoff\n";
	    if($somma<$cutoff){
		$keep{$k}=$hash{$k};
	    }
	    if($somma>=$cutoff){
		$keep{$k}=$hash{$k};
		last;
	    }
	}
    }
    return %keep;
    #foreach $l (keys(%keep)){
#	print "$l\t$keep{$l}\n";
#    }
	
}

