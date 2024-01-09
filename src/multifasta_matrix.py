import numpy as np
import os

def read_fasta(file_path):
    """
    Lit un fichier FASTA et renvoie la séquence en tant que chaîne de caractères.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Vérifier si la séquence est déjà au bon format (contient '>')
    if lines[0].startswith('>'):
        # Concaténer toutes les lignes après la première ligne qui contient le nom de la séquence
        sequence = ''.join(line.strip() for line in lines[1:])
    else:
        # La séquence n'est pas au format FASTA, utiliser la ligne telle quelle
        sequence = lines[0].strip()

    return sequence

def normalize_fasta_sequence(sequence):
    """
    Normalise une séquence FASTA en s'assurant qu'elle ne contient que les bases A, U, G, C.
    """
    return ''.join(base for base in sequence if base in "AUGC")

def one_hot_encoding(sequence):
    """
    Effectue le one-hot encoding d'une séquence d'ARN.
    """
    sequence_length = len(sequence)
    one_hot_matrix = np.zeros((sequence_length, 4), dtype=int)

    for i, nucleotide in enumerate(sequence):
        if nucleotide in "AUGC":
            one_hot_matrix[i, "AUGC".index(nucleotide)] = 1

    return one_hot_matrix

def process_fasta_files(fasta_files):
    """
    Traite plusieurs fichiers FASTA.
    """
    sequences = []

    # Lire les séquences à partir des fichiers FASTA et les normaliser
    for fasta_file in fasta_files:
        sequence = read_fasta(fasta_file)
        normalized_sequence = normalize_fasta_sequence(sequence)
        sequences.append(normalized_sequence)

    # Trouver la longueur maximale parmi toutes les séquences
    max_sequence_length = max(len(sequence) for sequence in sequences)

    # Initialiser la liste des matrices one-hot
    one_hot_matrices = []

    # Effectuer le one-hot encoding et remplir les matrices
    for sequence in sequences:
        one_hot_matrix = one_hot_encoding(sequence)
        # Ajouter des zéros à la fin pour aligner les matrices
        padding_length = max_sequence_length - len(sequence)
        padding_matrix = np.zeros((padding_length, 4), dtype=int)
        one_hot_matrix = np.vstack([one_hot_matrix, padding_matrix])
        one_hot_matrices.append(one_hot_matrix)

    return one_hot_matrices

def main():
    # Spécifiez le chemin du dossier contenant les fichiers FASTA en entrée
    fasta_folder_path = '/Users/macbook/Downloads/RNA_bioinfo'

    # Liste des fichiers FASTA dans le dossier
    fasta_files = [os.path.join(fasta_folder_path, file) for file in os.listdir(fasta_folder_path) if file.endswith('.fasta')]

    try:
        # Traiter les fichiers FASTA
        one_hot_matrices = process_fasta_files(fasta_files)

        # Afficher les matrices résultantes
        for i, matrix in enumerate(one_hot_matrices):
            print(f"Matrice one-hot pour la séquence {i + 1}:\n", matrix)
            print()

    except ValueError as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()
