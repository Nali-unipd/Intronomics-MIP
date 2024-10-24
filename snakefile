configfile: "config.yaml"
rule all:
	input:
		expand("{dirout}/log_final.txt", dirout = config['working_dir']),



rule split:
	input:
		dirout = expand("{dirout}", dirout=config['working_dir']),
		ind_list = expand("{indlist}", indlist=config['ind_list.txt']),
		adapters = expand("{adapters}", adapters=config['adapters.txt'])

	output:"{dirout}/Log.txt"
	params:
		rpath = expand("{rpath}", rpath=config['reads_path']),
		dirout = expand("{dirout}", dirout=config['working_dir']),
		adp1 = expand("{adp1}", adp1=config['reverse_adapter']),
		adp2 = expand("{adp1}", adp1=config['rev_comp_rev_adapter']),
		adp3 = expand("{adp1}", adp1=config['forward_adapter']),
		adp4 = expand("{adp1}", adp1=config['rev_comp_fow_adapter'])
	threads: config['Th_num']
	shell:
		"python3.8 split.py {input.ind_list} {input.adapters} {params.rpath} {params.dirout} {params.adp1} {params.adp2} {params.adp3} {params.adp4}"

rule rename:
	input:
		"{dirout}/Log.txt",
		dirout = expand("{dirout}", dirout=config['working_dir'])
	output: "{dirout}/Log_rename.txt"
	shell:
		"python3.8 rename.py {wildcards.dirout}"

rule Newlist:
	input:
		"{dirout}/Log_rename.txt",
		dirout = expand("{dirout}", dirout=config['working_dir'])
	output: "{dirout}/Newlist.txt"
	shell:
		"python3.8 Newlist.py {wildcards.dirout}"
rule copy:
	input:
		"{dirout}/Newlist.txt",
		ind_list = "{dirout}/Newlist.txt",
		dirout = expand("{dirout}", dirout=config['working_dir'])
	output:"{dirout}/Log_copy.txt"
	params:
		number = config['Nloci'],
		xlocus = "{dirout}/Xlocus"
	shell:
		     """
        for i in $(seq 1 {params.number}); do
            python3.8 Copy.py {input.ind_list} $i {wildcards.dirout} {params.xlocus}
        done
        """

rule merge:
	input:
		"{dirout}/Log_copy.txt",
		dirout = expand("{dirout}", dirout=config['working_dir']),
		adapters = expand("{adapters}", adapters=config['adapters.txt'])
	output: "{dirout}/MergedStatistics.txt"
	params:
		xlocus = "{dirout}/Xlocus",
		pathFl=expand("{pathFl}", pathFl=config['flash2_path']),
		pathbb=expand("{pathbb}", pathbb=config['fuse.sh_path'])
	shell:
		"python3.8 merge.py {input.adapters} {params.xlocus}/ {wildcards.dirout} {params.pathFl} {params.pathbb}"

rule remove:
	input:
		dirout = expand("{dirout}", dirout=config['working_dir']),
		file = "{dirout}/MergedStatistics.txt"
	output: "{dirout}/Log_remove.txt"
	params:
		xlocus = "{dirout}/Xlocus"
	shell:
		"python3.8 remove.py {params.xlocus} {input.file} {wildcards.dirout}"

rule seekdeep:
	input:
		"{dirout}/Log_remove.txt",
		dirout = expand("{dirout}", dirout=config['working_dir']),
		adapters = expand("{adapters}", adapters=config['adapters.txt'])
	params:
		path = expand("{path}", path=config['seekdeep_path']),
		xlocus = "{dirout}/Xlocus"
	output: "{dirout}/Log_SeekDeep.txt"
	shell:
		"python3.8 SeekDeep_par.py {input.adapters} {params.xlocus}/ {params.path} {wildcards.dirout}"

rule create:
	input:
		"{dirout}/Log_SeekDeep.txt",
		dirout = expand("{dirout}", dirout=config['working_dir']),
		ind_list = "{dirout}/Newlist.txt",
		adapters = expand("{adapters}", adapters=config['adapters.txt'])
	params:
		xlocus = "{dirout}/Xlocus",
		Sum = expand("{Sum}", Sum=config['cumulativeSum'])
	output: "{dirout}/Xlocus/Total_table.txt", "{dirout}/Xlocus/Filtered_table.txt"
	shell:
		"python3.8 create.py {input.adapters} {input.ind_list} {params.xlocus}/ {params.Sum}"

rule genepop:
	input:
		"{dirout}/Xlocus/Total_table.txt", "{dirout}/Xlocus/Filtered_table.txt",
		dirout = expand("{dirout}", dirout=config['working_dir']),
	params:
		number = config['Nloci'],
		table = "{dirout}/Xlocus/Filtered_table.txt"
	output: "{dirout}/Log_genepop.txt"
	shell:
		"python3.8 To_genepop.py {params.table} {params.number} {wildcards.dirout}/"


rule Merge_genepop:
	input:
		"{dirout}/Log_genepop.txt",
		dirout = expand("{dirout}", dirout=config['working_dir'])
	params:
		Perc = config['Perc'],
	output: "{dirout}/outputPop.txt"
	shell:
		"python3.8 totpop.py {wildcards.dirout} {params.Perc}"

rule Fasta:
    input:
        "{dirout}/outputPop.txt",
        dirout = config['working_dir']
    output:
        "{dirout}/log_final.txt"
    params:
        number = config['Nloci'],
        Sum = config['cumulativeSum']
    shell:
        """
        mkdir -p {wildcards.dirout}/FASTA;
        for i in $(seq 1 {params.number}); do
            if [ -f {wildcards.dirout}/Xlocus/L$i/merged/Results{params.Sum}/PopSeqs.keep.fasta ]; then
                mv {wildcards.dirout}/Xlocus/L$i/merged/Results{params.Sum}/PopSeqs.keep.fasta {wildcards.dirout}/Xlocus/L$i/merged/Results{params.Sum}/PopSeqs.keep_L$i.fasta;
            fi
        done
        for i in $(seq 1 {params.number}); do
            if [ -f {wildcards.dirout}/Xlocus/L$i/merged/Results{params.Sum}/PopSeqs.keep_L$i.fasta ]; then		
                cp  {wildcards.dirout}/Xlocus/L$i/merged/Results{params.Sum}/PopSeqs.keep_L$i.fasta {wildcards.dirout}/FASTA/;
            fi				
        done
		
		echo "complete!" > {wildcards.dirout}/log_final.txt
        """
