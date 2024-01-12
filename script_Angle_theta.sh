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

# Sequence in Fasta file Transformation into a matrix
python3 multifasta_matrix.py

#Calcule le MAE pour le model SPOT
python3 src/MAE_calc.py data/SPOT-RNA-1D/Test_SPOT_theta.txt data/output/Test_SPOT_theta.txt
data/SPOT-RNA-1D/training.json
#Compare les MAE
python3 src/Compare_MAE.py
