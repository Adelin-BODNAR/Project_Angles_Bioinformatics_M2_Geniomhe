#!/bin/bash

#sudo apt install python3
pip install json

mkdir data/TestSet_A
mkdir data/TrainingSet_A

#Cree un fichier avec uniquement les chaines A
dossier_entree="data/TestSet"
dossier_sortie="data/TestSet_A"
for fichier in "$dossier_entree"/*.pdb
do
  nom_fichier=$(basename "$fichier")
  cat <(head -n 3 "$fichier") <(awk '{if ($5 == "A" || $5 == "") print}' "$fichier") > "$dossier_sortie/${nom_fichier%.pdb}.pdb"
done

dossier_entree="data/TrainingSet"
dossier_sortie="data/TrainingSet_A"
for fichier in "$dossier_entree"/*.pdb
do
  nom_fichier=$(basename "$fichier")
  cat <(head -n 3 "$fichier") <(awk '{if ($5 == "A" || $5 == "") print}' "$fichier") > "$dossier_sortie/${nom_fichier%.pdb}.pdb"
done


#Cree les fichiers json pour DSSR
make -C dssr/src
pip install -r requirements.txt

mkdir data/output

python3 -m src.dssr_wrapper --input_path=data/TestSet_A --output_path=data/output/Test_DSSR.json

python3 -m src.dssr_wrapper --input_path=data/TrainingSet --output_path=data/output/Train_DSSR.json


#Extrait uniquement les angles theta des fichiers precedent
python3 src/extract_theta.py data/output/Test_DSSR.json data/output/Test_DSSR_theta.json

python3 src/extract_theta.py data/output/Train_DSSR.json data/output/Train_DSSR_theta.json

python3 src/extract_theta.py data/SPOT-RNA-1D/test.json data/output/Test_SPOT_theta.json

python3 src/extract_theta.py data/output/training.json data/output/Train_SPOT_theta.json

#Distribution et classe de theta

Rscript src/distrib_theta.R data/output/Train_DSSR_theta.json Distribution_train_theta_DSSR.pdf train_set data/output/Train_classes.txt

Rscript src/distrib_theta.R data/output/Test_DSSR_theta.json Distribution_test_theta_DSSR.pdf test_set data/output/Test_classes.txt
#Associe les nu de chaque sequence a des classes 
python3 src/Assos_Classes.py data/output/Train_DSSR_theta.json data/output/Train_classes.txt data/output/Train_DSSR_theta.txt
python3 src/Assos_Classes.py data/output/Test_DSSR_theta.json data/output/Test_classes.txt data/output/Test_DSSR_theta.txt

python3 src/Assos_Classes.py data/output/Train_DSSR_theta.json data/output/Train_classes.txt data/output/Train_SPOT_theta.txt
python3 src/Assos_Classes.py data/output/Test_DSSR_theta.json data/output/Test_classes.txt data/output/Test_SPOT_theta.txt

#sudo apt-get install pdftk   

pdftk data/output/Distribution_test_theta_DSSR.pdf data/output/Distribution_train_theta_DSSR.pdf cat output data/output/Distribution_test_train_theta_DSSR.pdf

rm -f data/output/Distribution_test_theta_DSSR.pdf
rm -f data/output/Distribution_train_theta_DSSR.pdf
#Creation des fasta _file
python3 src/Extract_seq_pdb_fasta.py data/TestSet_A data/TestSet_seq_Fasta TestSet_seq_Fasta
python3 src/Extract_seq_pdb_fasta.py data/TrainingSet_A data/TestSet_seq_Fasta TrainingSet_seq_Fasta

# Sequence in Fasta file Transformation into a matrix
python3 src/FastaSeq_to_matrix.py data/TrainingSet_seq_Fasta
python3 src/FastaSeq_to_matrix.py data/TestSet_seq_Fasta

python3 src/multifasta_matrix.py data/output/TrainingSet_seq_Fasta data/Training_matrices
python3 src/multifasta_matrix.py data/output/TestSet_seq_Fasta data/Test_matrices

#Concatenation matrices 
python3 src/Concatenation_Matrices.py data/Test_matrices data/output/AllTest_Matrices.csv
python3 src/Concatenation_Matrices.py data/Training_matrices data/output/AllTraining_Matrices.csv
#Extrait les labels
output_file_classes="data/output/Train_uniq_classe.txt"
output_file_ids="data/output/Train_ordered_ids.txt"

# Ajout de l'entête "label" dans le fichier de sortie des classes
echo "label" > "$output_file_classes"

while IFS=, read -r full_id classe rest; do
    id=$(echo "$full_id" | awk '{print $1}')
    classe=$(echo "$rest" | awk '{print $NF}')  # Récupère le dernier champ de la ligne

    csv_file="/data/output/Training_matrices/>${id}_Matrix.csv"

    if [ -f "$csv_file" ]; then
        echo "$classe" >> "$output_file_classes"
        echo "$id" >> "$output_file_ids"
    fi
done < data/output/train_classes.txt


output_file_classes="data/output/Test_uniq_classe.txt"
output_file_ids="data/output/Test_ordered_ids.txt"

# Ajout de l'entête "label" dans le fichier de sortie des classes
echo "label" > "$output_file_classes"

while IFS=, read -r full_id classe rest; do
    id=$(echo "$full_id" | awk '{print $1}')
    classe=$(echo "$rest" | awk '{print $NF}')  # Récupère le dernier champ de la ligne

    csv_file="/data/output/Test_matrices/>${id}_Matrix.csv"

    if [ -f "$csv_file" ]; then
        echo "$classe" >> "$output_file_classes"
        echo "$id" >> "$output_file_ids"
    fi
done < data/output/test_classes.txt
#associe les labels aux matrices
python3 src/label_matrix.py data/output/AllTest_Matrices.csv data/output/Test_uniq_classe.txt data/output/AllTest_Matrices_with_labels.csv Labels_all_matrices_test.csv
python3 src/label_matrix.py d/data/output/Training_matrices/ data/output/Train_uniq_classe.txt data/output/AllTraining_Matrices_with_labels.csv Labels_all_matrices_train.csv

#MLP
python3 src/model_mlp.py data/output/ALLTraining_Matrices.csv data/output/Labels_all_matrices_train.csv data/output/AllTraining_Matrices.csv data/output/Labels_all_matrices_test.csv

#Calcule le MAE pour le model SPOT
python3 src/MAE_calc.py data/output/Train_SPOT_theta.txt data/output/Train_DSSR_theta.txt data/output/MAE_DSSR_Train__SPOT.txt
python3 src/MAE_calc.py data/output/Test_SPOT_theta.txt data/output/Test_DSSR_theta.txt data/output/data/output/MAE_DSSR_Test__SPOT.txt


awk 'BEGIN { sum=0; count=0; } { sum+=$5; count++; lines[count]=$0; } END { if(count>0) { lines[1]="Moyenne : " sum/count; for(i=1;i<=count;i++) print lines[i]; } }' data/output/MAE_DSSR_Train__SPOT.txt > temp && mv temp data/output/MAE_DSSR_Train__SPOT.txt
awk 'BEGIN { sum=0; count=0; } { sum+=$5; count++; lines[count]=$0; } END { if(count>0) { lines[1]="Moyenne : " sum/count; for(i=1;i<=count;i++) print lines[i]; } }' data/output/MAE_DSSR_Test__SPOT.txt > temp && mv temp data/output/MAE_DSSR_Train__SPOT.txt

