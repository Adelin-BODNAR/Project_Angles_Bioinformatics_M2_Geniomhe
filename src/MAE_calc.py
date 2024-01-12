import json
import sys
import os

fichier1=sys.argv[1] 
fichier2=sys.argv[2]             
def extraire_classes(data):
    with open(data, "r") as file_1:
        classes = {}
        for lines in file_1:
            elements = lines.split()
            if len(elements) >= 9:
                sequence = elements[0]
                classe = int(elements[8])
                if sequence not in classes:
                    classes[sequence] = []
                classes[sequence].append(classe)
        return classes


classes_fichier1 = extraire_classes(fichier1)
classes_fichier2 = extraire_classes(fichier2)


for sequence in set(classes_fichier1.keys()) & set(classes_fichier2.keys()):
    classes_sequence_fichier1 = classes_fichier1[sequence]
    classes_sequence_fichier2 = classes_fichier2[sequence]
    
    total_MAE = 0  
    
    for class_fichier1, class_fichier2 in zip(classes_sequence_fichier1, classes_sequence_fichier2):
        Di = abs(class_fichier1 - class_fichier2)
        MAE = min(Di, 15 - Di)
        total_MAE += MAE  

    average_MAE = total_MAE / len(classes_sequence_fichier1)  

    with open("data/output/MAE_DSSR_Test__SPOT.txt", 'a') as res_file:
        res_file.write(f"{sequence} :\tMAE : {average_MAE}\n")
