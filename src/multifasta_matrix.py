import numpy as np
import os
import pandas as pd

def read_fasta(file_path):
    """
    Read a FASTA file and return the header and sequence as strings.
    """
    with open(file_path, 'r') as file:
        header = file.readline().strip()


        sequence = ''.join(line.strip() for line in file.readlines())

    return header, sequence

def normalize_fasta_sequence(sequence):
    """
    Normalize a FASTA sequence, ensuring it contains only the bases A, U, G, C.
    """
    return ''.join(base.upper() for base in sequence if base.upper() in "AUGC")

def one_hot_encoding(sequence):
    """
    Perform one-hot encoding of an RNA sequence.
    """
    sequence_length = len(sequence)
    one_hot_matrix = np.zeros((sequence_length, 4), dtype=int)

    for i, nucleotide in enumerate(sequence):
        if nucleotide in "AUGC":
            one_hot_matrix[i, "AUGC".index(nucleotide)] = 1

    return one_hot_matrix

def process_fasta_files(fasta_files):
    """
    Process multiple FASTA files.
    """
    sequences = []
    headers = []

    for fasta_file in fasta_files:
        header, sequence = read_fasta(fasta_file)
        normalized_sequence = normalize_fasta_sequence(sequence)
        sequences.append(normalized_sequence)
        headers.append(header)


    max_sequence_length = max(len(sequence) for sequence in sequences)


    one_hot_matrices = []

    for sequence in sequences:
        one_hot_matrix = one_hot_encoding(sequence)
        padding_length = max_sequence_length - len(sequence)
        padding_matrix = np.zeros((padding_length, 4), dtype=int)
        one_hot_matrix = np.vstack([one_hot_matrix, padding_matrix])
        one_hot_matrices.append(one_hot_matrix)

    return headers, one_hot_matrices

def main():

    fasta_folder_path = 'data/TestSet_seq_Fasta'


    fasta_files = [os.path.join(fasta_folder_path, file) for file in os.listdir(fasta_folder_path) if file.endswith('.fasta')]

    try:
        headers, one_hot_matrices = process_fasta_files(fasta_files)

 
        output_folder = 'data/Test_matrices'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

     
        for i, (header, matrix) in enumerate(zip(headers, one_hot_matrices)):
            columns = [f'nucleotide_{j}' for j in range(1, matrix.shape[1] + 1)]
            df = pd.DataFrame(matrix, columns=columns)

            output_csv_path = os.path.join(output_folder, f'{header}_Matrix.csv')
            df.to_csv(output_csv_path, index=False)

            print(f"CSV file for sequence {i + 1} with header '{header}' saved to: {output_csv_path}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
