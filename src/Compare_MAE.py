import shutil
import os
import pandas as pd

diff_file=["Test","Train"]
fichiers_source = os.listdir("data/output)

def complete_file(all_file, fichiers, outfile):
    file1 = pd.read_csv(all_file[0], sep=":", header=None)
    file2 = pd.read_csv(all_file[1], sep=":", header=None)
    res_1 = 0
    res_2 = 0
    with open(outfile, "a") as output_add:
        for index1, line1 in file1.iterrows():
            for index2, line2 in file2.iterrows():
                if line1[0] == line2[0]:
                    if line1[2] > line2[2]:
                        output_add.write(line1[0] + " : \t" + str(line1[2]) + "\t" + str(line2[2]) + "\t" +str(abs(line1[2] - line2[2])) + "\t" + fichiers[0] + "\n")
                        res_1 += 1
                    else:
                        output_add.write(line1[0] + " : \t" + str(line1[2]) + "\t" + str(line2[2]) +"\t" + str(abs(line1[2] - line2[2])) + "\t" + fichiers[1] + "\n")
                        res_2 += 1
        if res_1 > res_2:
            output_add.write("Le meilleur modèle est le modèle " + fichiers[0])
        else:
            output_add.write("Le meilleur modèle est le modèle " + fichiers[1])

for deb in diff_file:
    outfile = "/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/Comparaison_" + deb + ".txt"
    print(deb)
    all_file = []
    fichiers = []
    for fichier in fichiers_source:
        if fichier.startswith("MAE_DSSR_" + deb) and os.path.join("/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/", fichier) not in all_file:
            all_file.append(os.path.join("/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/", fichier))
            fichiers.append(str(fichier))

    with open(outfile, "w") as output:
        output.write("Sequence \t MAE : " + fichiers[0] + "\t MAE : " + fichiers[1] + "\t Difference \t Meilleur model \n")

    complete_file(all_file, fichiers, outfile)
