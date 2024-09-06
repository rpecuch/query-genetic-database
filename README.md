# Query Genetic Database
# Author: Rita Pecuch 

The goal of this script is to output the nucleotide and amino acid sequences of a given human gene and identify all species with homologous genes.

Inputs: 
- MC1R: name of gene
- utils.py: Python file containing utility functions needed by the script

Output files: 
- MC1R.fasta: contains nucleotide and amino acid sequences of inputted gene
- mc1r_homology_list.txt: contains the name of each species with homologous gene to inputted gene

Execution:

1) Copy over the following files into the directory that you would like to run the script:
- utils.py
- query_database.py

2) Execute the following command: python3 query_database.py -gene MC1R -utils utils.py