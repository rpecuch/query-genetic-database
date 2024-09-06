# Execution: python3 query_database.py -gene MC1R -utils utils.py

# Import needed libraries
import argparse
from Bio.Seq import Seq
import re
import requests

if __name__ == "__main__":
    # Read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-gene", help="Name of gene to query")
    parser.add_argument("-utils", help="Python file with utility functions")
    args=parser.parse_args()

    # Import utility functions
    exec(open(args.utils).read())

    # Get Entrez gene ID
    endpoint = f'http://mygene.info/v3/query?q={args.gene}&species=human'
    gene_info = requests.get(endpoint).json()
    gene_id = gene_info["hits"][0]["_id"]

    # Get ensembl ID
    endpoint = f'http://mygene.info/v3/gene/{gene_id}'
    gene_annotation = requests.get(endpoint).json()
    ensembl_id = gene_annotation['ensembl']['gene']

    # Get nucleotide sequence
    endpoint = f'https://rest.ensembl.org/sequence/id/{ensembl_id}'
    # headers={ "Content-Type" : "text/x-fasta"}
    headers={ "Content-Type" : "text/plain"}
    sequence = requests.get(endpoint, headers=headers).text

    # Write sequence to FASTA
    with open(f'{args.gene}.fasta', 'w') as f:
        # Write header
        f.write(f'>{ensembl_id}')
        f.write('\n')
        # Write sequence
        f.write(sequence)

    # Read sequence from FASTA file
    header, sequence = read_fasta(f'{args.gene}.fasta')

    # Find longest ORF
    longest_orf = find_longest_orf(sequence)

    # Convert nucleotide sequence to amino acid sequence
    seq_to_translate = Seq(longest_orf) 
    # Transcription
    rna_seq = seq_to_translate.transcribe()
    # Translation, do not print * for stop codon
    aa_seq = str(rna_seq.translate(to_stop=True))
    
    # Add amino acid sequence to FASTA file
    with open(f'{args.gene}.fasta', 'a') as f:
        # Write header
        f.write('\n')
        f.write(f'>{longest_orf}')
        # Write sequence
        f.write('\n')
        f.write(aa_seq)

    # Find homology info
    endpoint = f'https://rest.ensembl.org/homology/id/human/{ensembl_id}'
    headers={ "Content-Type" : "application/json"}
    response = requests.get(endpoint, headers=headers).json()
    homology_data = response['data'][0]['homologies']
    
    # Write species to txt file
    gene_lowercase = args.gene.lower()
    with open(f'{gene_lowercase}_homology_list.txt', 'w') as f:
        species = []
        for entry in homology_data:
            # Add only unique species
            if entry['target']['species'] not in species:
                species.append(entry['target']['species'])
                f.write(entry['target']['species'])
                f.write('\n')