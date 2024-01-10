#!/bin/bash

#sudo apt install python3
pip install json

make -C dssr/src
pip install -r requirements.txt

mkdir data/output

mkdir data/TestSet_A
mkdir data/TrainingSet_A
#Cree un fichier avec uniquement les chaines A
dossier_entree="data/TestSet"
dossier_sortie="data/TestSet_A"
for fichier in "$dossier_entree"/*.pdb
do
  nom_fichier=$(basename "$fichier")
  cat <(head -n 3 "$fichier") <(awk '$5 == "A" {print}' "$fichier") > "$dossier_sortie/${nom_fichier%.pdb}_filtre.pdb"
done

dossier_entree="data/TrainingSet"
dossier_sortie="data/Training_A"
for fichier in "$dossier_entree"/*.pdb
do
  nom_fichier=$(basename "$fichier")
  cat <(head -n 3 "$fichier") <(awk '$5 == "A" {print}' "$fichier") > "$dossier_sortie/${nom_fichier%.pdb}_filtre.pdb"
done

#Cree les fichiers json pour DSSR
python -m src.dssr_wrapper --input_path=data/TestSet_A --output_path=data/output/Test_DSSR.json

python -m src.dssr_wrapper --input_path=/data/TrainingSet_A --output_path=data/output/Train_DSSR.json


#Extrait uniquement les angles theta des fichiers precedent
python3 src/extract_theta.py data/output/Test_DSSR.json data/output/Test_DSSR_theta.json

python3 src/extract_theta.py data/output/Train_DSSR.json data/output/Train_DSSR_theta.json

#Distribution et classe de theta

Rscript src/distrib_theta.R data/output/Train_DSSR_theta.json Distribution_train_theta_DSSR.pdf train_set

Rscript src/distrib_theta.R data/output/Test_DSSR_theta.json Distribution_test_theta_DSSR.pdf test_set

sudo apt-get install pdftk   

pdftk data/output/Distribution_test_theta_DSSR.pdf data/output/Distribution_train_theta_DSSR.pdf cat output data/output/Distribution_test_train_theta_DSSR.pdf

rm -f data/output/Distribution_test_theta_DSSR.pdf
rm -f data/output/Distribution_train_theta_DSSR.pdf

# Sequence in Fasta file Transformation into a matrix
python3 multifasta_matrix.py

#Calcule le MAE pour le model SPOT et notre model 
python3 src/MAE_calc.py data/SPOT-RNA-1D/test.json data/output/test_our_model.json data/SPOT-RNA-1D/training.json data/output/train_our_model.json SPOT OUR_MODEL Test Train data/output/Test_DSSR_theta.json data/output/Train_DSSR_theta.json

#Compare les MAE
python3 src/Compare_MAE.py
