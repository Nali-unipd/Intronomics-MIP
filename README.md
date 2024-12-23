### Author: Annalisa Scapolatiello  
**Email:** annalisa.scapolatiello@studenti.unipd.it  


# **Intronomics-MIP Pipeline**

## **Description**
The Intronomics-MIP pipeline is designed to analyze multi-locus targeted sequencing data. It automates the haplotype generation process, providing a robust and scalable approach for analyzing genetic diversity.

## **Index**
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)

## **Requirements**
- Snakemake v7.32.4
- Cutadapt v2.8
- FLASH v2.2.00
- SeekDeep v3.0.1

## **Installation**

bash install_dep.sh

---

## **Usage**

Place your input files in the specified directory. The pipeline requires:
FASTQ file with raw readings.
A YAML configuration file to specify project parameters (e.g. file paths, library names, and filtering parameters).

Start the pipeline with Snakemake:
snakemake --cores 8

The main outputs will be generated in the directory specified in config.yaml

-FASTA files for each locus

-Haplotype Coverage Table

-Haplotype Genepop format table


## **Example**

Preparing Files Download the sample data and configuration file provided in the repository:

git clone https://github.com/Nali-unipd/Intronomics-MIP.git

cd Intronomics-MIP

Execution Start the pipeline using the example configuration file:

 snakemake --cores 4 --configfile config_example.yaml




### Feel free to modify any part as needed! If you need more help or additional sections, just let me know.
