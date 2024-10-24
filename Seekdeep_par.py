import os
import sys
import glob
import subprocess
import multiprocessing
import argparse

def genotyping(l, filenames, input_dir, path):
    for file in glob.glob(f"{input_dir}/L{l}/merged/*.gz"):
        base_name = os.path.basename(file).split(".")[0]
        filenames.append(base_name)

    # Writing filenames to lista file
    lista_file = f"{input_dir}L{l}/merged/lista"
    with open(lista_file, "w") as f:
        for filename in filenames:
            f.write(filename + "\n")

    # Running SeekDeep_par for each file in lista
    try:
        with open(lista_file, "r") as in_file:
            for line in in_file:
                i = line.strip()  # Strip the newline character
                print(f"Processing file: {i}")
                subprocess.run([f"{path}/bin/SeekDeep", "qluster",
                                "--fastqgz", f"{input_dir}L{l}/merged/{i}.merged.fastq.gz",
                                "--overWriteDir", "--parFreqs", "1.5", "--illumina",
                                "-dout", f"{input_dir}L{l}/merged/SeekDeep/CLUSTER/{i}/MID1"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running qluster for {i}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # Running processClusters
    try:
        os.chdir(f"{input_dir}L{l}/merged/SeekDeep/CLUSTER/")
        subprocess.run([f"{path}/bin/SeekDeep", "processClusters", 
                        "--fastqgz", "output.fastq.gz", "--illumina", 
                        "--noErrors", "--sampleMinTotalReadCutOff", "30", 
                        "--overWriteDir", "-dout", "processClusters"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running processClusters: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def process_locus(line, input_dir, path):
    # Get the first column (locus number)
    l = line.strip().split()[0]
    filenames = []
    genotyping(l, filenames, input_dir, path)

if __name__ == "__main__":
    # Argument Parsing
    parser = argparse.ArgumentParser(description='Run SeekDeep genotyping pipeline.')
    parser.add_argument('adapter_file', type=str, help='Path to adapter file')
    parser.add_argument('input_dir', type=str, help='Input directory')
    parser.add_argument('path', type=str, help='Path to SeekDeep_par executable')
    parser.add_argument('out', type=str, help='Output directory for logs')
    
    args = parser.parse_args()
    
    # Multiprocessing setup
    num_processes = 8  # Adjust based on system capabilities
    pool = multiprocessing.Pool(processes=num_processes)
    
    # Reading loci from the adapter file
    with open(args.adapter_file) as f:
        lines = f.readlines()

    # Processing each locus with multiprocessing
    results = [
        pool.apply_async(process_locus, (line, args.input_dir, args.path))
        for line in lines
    ]
    
    pool.close()
    pool.join()

    # Logging
    log_path = os.path.join(args.out, "Log_SeekDeep.txt")
    with open(log_path, 'a') as log_file:
        log_file.write("SeekDeep processing completed successfully.\n")
