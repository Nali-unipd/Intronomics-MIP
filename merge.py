import os
import sys

# Get command-line arguments
loci_file = sys.argv[1]
input_dir = sys.argv[2]
out=sys.argv[3]
pathFl=sys.argv[4]
pathbb=sys.argv[5]


# Open file to write commands to
with open("Merged_Command.sh", 'w') as cmd_file:
    # Open loci file and read loci
	with open(loci_file, 'r') as f:
		for line in f:
            # Split line on tab character and get locus and sample names
			fields = line.strip().split("\t")
			locus = fields[0]
            

			# Set input and output directories
			dir_in = input_dir + "/L" + locus
			out_dir = dir_in + "/merged"

			# Create output directory if it doesn't exist
			if not os.path.exists(out_dir):
				os.makedirs(out_dir)
			try:
				files = os.listdir(dir_in)
			except OSError:
				print("Cannot open {}".format(dir_in))
				sys.exit(1)

			seq = {}
			fastq_files = [f for f in files if f.endswith('.fastq.gz')]

			for f in fastq_files:
				fields = f.split(".")
				sample_name = fields[0]
				seq[sample_name] = "ok"

            # Process each sample
			for sample in seq.keys():
                # Set input and output filenames
				in_1 = dir_in + "/" + sample + ".R1.fastq.gz"
				in_2 = dir_in + "/" + sample + ".R2.fastq.gz"
				out_file = out_dir + "/" + sample + ".merged.fastq.gz"
				log_file = out_dir + "/" + sample + ".LOG"

                # Attempt to merge FASTQ files with flash2
				cmd = f"{pathFl}flash2 -t 1 --to-stdout -z --interleaved-output --max-overlap 300 {in_1} {in_2} > {out_file} 2> {log_file}"
				os.system(cmd)
				cmd_file.write(cmd + "\n")

                # Parse log file to get total and combined number of pairs of reads
				total_pairs = 0
				combined_pairs = 0
				percent_combined = 0
				if os.path.exists(log_file):
					with open(log_file, 'r') as log:
						for log_line in log:
							if "Total pairs:" in log_line:
								total_pairs = int(log_line.strip().split()[-1])
							elif "Combined pairs:" in log_line:
								combined_pairs = int(log_line.strip().split()[-1])
							elif "Percent combined:" in log_line:
								percent_combined = log_line.strip().split()[-1]
								percentage = percent_combined.strip('%')
								percent_combined = float(percentage)


                # Print information about merging process to STDERR
				path=out + "/MergedStatistics.txt"
				with open(path, 'a') as file:
					if total_pairs == 0:
						file.write(("{}\t"+str(total_pairs)+"\t"+str(combined_pairs)+"\t"+str(percent_combined)+"\tNo Sequences\r").format(sample))

                # If merge fails, use fuse.sh to merge FASTQ files
					elif percent_combined <= 20:
						cmd = f"{pathbb}fuse.sh in1={in_1} in2={in_2} pad=10 out={out_file} fusepairs overwrite=TRUE 2> {log_file}"
						os.system(cmd)
						cmd_file.write(cmd + "\n")
						file.write(("{}\t"+str(total_pairs)+"\t"+str(combined_pairs)+"\t"+str(percent_combined)+"\tFUSED\r").format(sample))
					else: 
						file.write(("{}\t"+str(total_pairs)+"\t"+str(combined_pairs)+"\t"+str(percent_combined)+"\tMERGED\r").format(sample))
#file.write(("{}\t"+str(total_pairs)+"\t"+str(combined_pairs)+"\t"+str(percent_combined)+"\tMERGED").format(sample), file=sys.stderr)
