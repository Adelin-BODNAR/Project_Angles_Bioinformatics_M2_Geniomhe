import numpy as np
import os
import pandas as pd

def read_fasta(file_path):
    """
    Read a FASTA file and return the header and sequence as strings.
    """
    with open(file_path, 'r') as file:
        # Skip the first line (header)
        header = file.readline().strip()

        # Read the rest of the file and join lines into a single string
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

    # Read sequences and headers from FASTA files
    for fasta_file in fasta_files:
        header, sequence = read_fasta(fasta_file)
        normalized_sequence = normalize_fasta_sequence(sequence)
        sequences.append(normalized_sequence)
        headers.append(header)

    # Find the maximum length among all sequences
    max_sequence_length = max(len(sequence) for sequence in sequences)

    # Initialize the list of one-hot matrices
    one_hot_matrices = []

    # Perform one-hot encoding and fill the matrices
    for sequence in sequences:
        one_hot_matrix = one_hot_encoding(sequence)
        # Add zeros to the end to align the matrices
        padding_length = max_sequence_length - len(sequence)
        padding_matrix = np.zeros((padding_length, 4), dtype=int)
        one_hot_matrix = np.vstack([one_hot_matrix, padding_matrix])
        one_hot_matrices.append(one_hot_matrix)

    return headers, one_hot_matrices

def main():
    # Specify the path to the folder containing input FASTA files
    fasta_folder_path = 'TestSet_seq_Fasta'

    # List of FASTA files in the folder
    fasta_files = [os.path.join(fasta_folder_path, file) for file in os.listdir(fasta_folder_path) if file.endswith('.fasta')]

    try:
        # Process FASTA files
        headers, one_hot_matrices = process_fasta_files(fasta_files)

        # Create a folder to save CSV files
        output_folder = 'Test_matrices'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save each matrix in a separate CSV file with the corresponding header
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
