def read_fasta(filename):
    with open(filename, 'r') as f:
        # Read header
        header = f.readline().strip()
        # Read sequence 
        sequence = f.readline().strip()

    return header, sequence

def find_start_codons(sequence):
        matches = re.finditer('ATG', sequence)
        codon_positions = []
        for match in matches:
            codon_positions.append(match.start())

        return codon_positions

def find_stop_codon(sequence):
    matches = re.finditer('(TAA|TAG|TGA)', sequence)
    # Choose first match that provides ORF length divisible by 3
    for match in matches:
        if match.end() % 3 == 0:
            return match.end()
    # If no stop codon found
    return None

def find_longest_orf(sequence):
    # Ensure all uppercase
    sequence = sequence.upper()

    # Find positions of all start codons
    start_codons = find_start_codons(sequence)

    # List of stop codon positions
    stop_codons = []
    # List of ORFs - format for each entry is [length, start position, stop position]
    orfs = []

    # Loop through start codon positions
    for start in start_codons:
        # Find relative position of end of first stop codon
        stop = find_stop_codon(sequence[start:])

        if stop:
            # Absolute position of stop codon
            stop_position = start + stop

            # If already in list of stop codons then a longer ORF contains the stop codon
            if stop not in stop_codons:
                stop_codons.append(stop)
                orfs.append([stop, start, stop_position])

    # Sort orfs
    orfs = sorted(orfs, reverse=True)

    # Get longest orf
    longest_orf_start = orfs[0][1]
    longest_orf_stop = orfs[0][2]
    longest_orf = sequence[longest_orf_start:longest_orf_stop]

    return longest_orf