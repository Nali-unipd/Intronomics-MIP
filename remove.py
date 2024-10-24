import sys
import os
import re
import shutil


# Get the arguments
dir = sys.argv[1]
in_file = sys.argv[2]
out=sys.argv[3]

# Open the input file
with open(in_file, 'r') as f:
    # Read the file line by line
    for r in f:
        # Remove the newline character from the line
        r = r.strip()
        # Split the line into an array using the tab character as a delimiter
        t = r.split('\t')
        # Extract the number that appears after an underscore character
        locus = re.search(r'_(\d+)', t[0]).group(1)
        # Create the removed directory
        removed_dir = f"{dir}/L{locus}/merged/removed"
        # Check if the removed directory exists
        if not os.path.isdir(removed_dir):
            # Create the removed directory if it does not exist
            os.makedirs(removed_dir)
        else:
            directory_path = '/percorso/della/cartella'
            shutil.rmtree(removed_dir)
            os.makedirs(removed_dir)

        # Create the fastq file path
        fastq = f"{dir}/L{locus}/merged/{t[0]}.merged.fastq.gz"

        # Check if the last element of the array is "FUSED"
        #if t[-1] == "FUSED":
            # Move the fastq file to the removed directory
            #try:
             #   shutil.move(fastq, removed_dir)
            #except:
             #   pass
            #continue

        # Check if the second element of the array is less than ... (10)
        if int(t[1]) < 10:
            # Move the fastq file to the removed directory
            shutil.move(fastq, removed_dir)
            continue

path=out+"/Log_remove.txt"
with open(path, 'a') as file:
    file.write("remove ok" + '\n')