import os
import sys

# Get command-line arguments
sample_list_file = sys.argv[1]
locus = sys.argv[2]
input_dir = sys.argv[3]
output_dir = sys.argv[4] + "/L" + locus

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open sample list file and read sample names
with open(sample_list_file, 'r') as f:
    for line in f:
        # Split line on underscore and get first part
        sample_name = line.strip().split("_")[0]

        # Copy FASTQ files for specified locus from input directory to output directory
        os.system("cp {}/{}/locus{}.R1.fastq.gz {}/{}_{}.R1.fastq.gz".format(input_dir, sample_name, locus, output_dir, sample_name, locus))
        os.system("cp {}/{}/locus{}.R2.fastq.gz {}/{}_{}.R2.fastq.gz".format(input_dir, sample_name, locus, output_dir, sample_name, locus))

path= input_dir + "/Log_copy.txt"
with open(path, 'a') as file:
    file.write("Copy ok" + '\n')
