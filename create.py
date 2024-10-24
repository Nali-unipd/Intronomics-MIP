import os
import sys
import glob
import shutil
import gzip
import subprocess
# Read the command-line arguments
adapter_file = sys.argv[1]
ind = sys.argv[2]
input_dir = sys.argv[3]
cutoff = sys.argv[4]

with open(adapter_file, 'r') as f:
    for line in f:
        # Split the line into columns
        columns = line.strip().split()
        # Get the first column
        l = columns[0]
        DIR =f"{input_dir}L{l}/merged/SeekDeep/CLUSTER/processClusters"
        rdir = f"{input_dir}L{l}/merged/Results"+str(cutoff)
        os.makedirs(rdir, exist_ok=True)
        try:
            shutil.copy(f"{DIR}/hapIdTable.tab.txt.gz", rdir,)
            with gzip.open(f"{rdir}/hapIdTable.tab.txt.gz", 'rb') as f_in, open(f"{rdir}/hapIdTable.tab.txt", 'wb') as f_out:
                f_out.write(f_in.read())
            shutil.copy(f"{DIR}/population/PopSeqs.fastq.gz", rdir,)
            with gzip.open(f"{rdir}/PopSeqs.fastq.gz", 'rb') as f_in, open(f"{rdir}/PopSeqs.fastq", 'wb') as f_out:
                f_out.write(f_in.read())

            with open(f"{rdir}/PopSeqs.fastq") as f:
                with open(f"{rdir}/PopSeqs.fasta", 'w') as out:
                    for i, line in enumerate(f, start=1):
                        if line.startswith("@PopUID"):
                            out.write(line.replace("@", ">", 1).split("_")[0] + "\n")
                        elif i % 4 !=0 and not line.startswith("+"):
                            out.write(line)
        except Exception as e:
            # exception handling code here
            pass



        result=subprocess.run(['./filter_Haplo_table.pl', f"{rdir}/hapIdTable.tab.txt", f"{rdir}/PopSeqs.fasta", ind, cutoff], stderr=subprocess.PIPE)
        with open(f"{rdir}/Filtering.log", "w") as f:
            f.write(result.stderr.decode())
                    
        result=subprocess.run(['./FracToNumer_matrix.pl', f"{DIR}/selectedClustersInfo.tab.txt.gz", f"{rdir}/hapIdTable.tab.full.txt"], stdout=subprocess.PIPE)
        with open(f"{rdir}/hapIdTable.tab.count.full.txt", "w") as f:
            f.write(result.stdout.decode())

        result=subprocess.run(['./FracToNumer_matrix.pl', f"{DIR}/selectedClustersInfo.tab.txt.gz", f"{rdir}/hapIdTable.tab.filtered.txt"], stdout=subprocess.PIPE)
        with open(f"{rdir}/hapIdTable.tab.count.filtered.txt", "w") as f:
            f.write(result.stdout.decode()) 

        result = subprocess.run(['./concatenate_tables.pl', adapter_file, "hapIdTable.tab.count.full.txt", input_dir, cutoff  ], stdout=subprocess.PIPE)
        with open(f"{input_dir}/"+"Total_table"+".txt", "w") as f:
            f.write(result.stdout.decode())

        result=subprocess.run(['./concatenate_tables.pl', adapter_file, "hapIdTable.tab.count.filtered.txt", input_dir, cutoff  ], stdout=subprocess.PIPE)
        with open(f"{input_dir}/Filtered_table"+".txt", "w") as f:
            f.write(result.stdout.decode()) 
      
          

                 