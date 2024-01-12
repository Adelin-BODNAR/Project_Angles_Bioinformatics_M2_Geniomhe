from Bio import PDB
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqIO import write
import os 
import sys
def extract_rna_sequence(pdb_file):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('structure', pdb_file)

    rna_sequence = ""
    for model in structure:
        for chain in model:
            for residue in chain:
                if PDB.is_aa(residue):
                    try:
                        rna_sequence += PDB.Polypeptide.three_to_one(residue.get_resname())
                    except KeyError:
                        # Ignorer les résidus inconnus lors de la conversion
                        pass
                elif residue.id[0] == " ":
                    rna_sequence += residue.get_resname()

    return Seq(rna_sequence)


def create_fasta_files(input_folder, output_folder, error_folder):
    output_folder.mkdir(exist_ok=True)  # Create the output folder if it doesn't exist
    error_folder.mkdir(exist_ok=True)  # Create the error folder if it doesn't exist

    for pdb_file in input_folder.glob('*.pdb'):
        try:
            sequence = extract_rna_sequence(str(pdb_file))
            record_id = pdb_file.stem  # Use the filename without extension as the record ID
            record = SeqRecord(sequence, id=record_id, description="")

            output_file = output_folder / f"{record_id}.fasta"
            with open(output_file, 'w') as fasta_out:
                write(record, fasta_out, 'fasta')
        except RuntimeError as e:
            print(f"RuntimeError processing {pdb_file}: {e}")
            # Move the problematic PDB file to the error folder
            error_file = error_folder / pdb_file.name
            os.rename(pdb_file, error_file)
            continue  # Pass to the next file
        except Exception as e:
            print(f"Error processing {pdb_file}: {e.__class__.__name__} - {e}")
            continue  # Pass to the next file

if __name__ == "__main__":
    import pathlib

    input_folder_path = sys.argv[1]
    output_folder_path = sys.argv[2]
    error_folder_path = 'data/PDB_Files_error'

    input_folder = pathlib.Path(input_folder_path)
    output_folder = pathlib.Path(output_folder_path)
    error_folder = pathlib.Path(error_folder_path)

    create_fasta_files(input_folder, output_folder, error_folder)
