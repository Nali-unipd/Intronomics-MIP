import os
import sys
import multiprocessing

dirIn = sys.argv[3]
dirOut = sys.argv[4]
adp1=sys.argv[5]
adp2=sys.argv[6]
adp3=sys.argv[7]
adp4=sys.argv[8]
# Read list of sample names and store them in a list
sample_names = []
with open(sys.argv[1]) as f:
  for line in f:
    t = line.strip().split("_")
    sample_names.append((t[0], line.strip()))

# Define a function to invert and complement a DNA sequence
def InvComp(sequence):
  inv_comp = ""
  for base in sequence[::-1]:
    if base == "A":
      inv_comp += "T"
    elif base == "C":
      inv_comp += "G"
    elif base == "G":
      inv_comp += "C"
    elif base == "T":
      inv_comp += "A"
  return inv_comp


def process_sample(locus, t, sample_names, dirIn, dirOut, adp1, adp2, adp3, adp4, InvComp):
    primer5 = t[3]
    primer3 = t[6]
    primer5Inv = InvComp(primer5)
    primer3Inv = InvComp(primer3)

    for ind, sample in enumerate(sample_names):
        ind_id, sample_name = sample

        # Creazione della directory se non esiste
        sample_dir = os.path.join(dirOut, ind_id)
        if not os.path.exists(sample_dir):
            os.makedirs(sample_dir)

        f1out = os.path.join(sample_dir, f"locus{locus}.R1.fastq.gz")
        f2out = os.path.join(sample_dir, f"locus{locus}.R2.fastq.gz")
        f1In = os.path.join(dirIn, f"{sample_name}_L001_R1_001.fastq.gz")
        f2In = os.path.join(dirIn, f"{sample_name}_L001_R2_001.fastq.gz")
        log = os.path.join(sample_dir, f"locus{locus}")


        cmd = (
            f"cutadapt --interleaved {f1In} {f2In} | "
            f"cutadapt -n 5 --minimum-length 100 --overlap 15 -j 8 -q 15 -g {primer5} -G {primer3} "
            f"--discard-untrimmed --pair-filter=any --action=trim --interleaved - 2> {log}.s1.log | "
            f"cutadapt --minimum-length 100 -n 5 -j 8 --interleaved "
            f"-A {primer5Inv} -a {primer3Inv} -a {adp3} -A {adp2} -g {adp1} -G {adp4} - 2> {log}.s2.log | "
            f"cutadapt -n 5 -j 8 --interleaved "
            f"-A {adp3} -a {adp2} -G {adp1} -g {adp4} "
            f"-A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT "
            f"--discard-trimmed --pair-filter=any - 2> {log}.s3.log | "
            f"cutadapt -j 8 --interleaved -o {f1out} -p {f2out} -"
        )


        print(cmd)
        os.system(cmd)

def process_locus_parallel(line, sample_names, dirIn, dirOut, adp1, adp2, adp3, adp4, InvComp):
    line = line.strip()
    t = line.split("\t")
    locus = t[0]
    print(f"Processing locus {locus}")

    process_sample(locus, t, sample_names, dirIn, dirOut, adp1, adp2, adp3, adp4, InvComp)

if __name__ == "__main__":
    # Parametri multiprocess
    num_processes = 8  # Puoi regolare il numero di processi
    pool = multiprocessing.Pool(processes=num_processes)

    # Apertura del file e lettura
    with open(sys.argv[2]) as f:
        lines = f.readlines()

    num = len(lines)  # Loci è il numero di righe nel file

    
    results = [
        pool.apply_async(process_locus_parallel, (line, sample_names, dirIn, dirOut, adp1, adp2, adp3, adp4, InvComp))
        for line in lines
    ]


    pool.close()
    pool.join()

path=dirOut + "/Log.txt"
with open(path, 'a') as file:
    file.write("split ok" + '\n')