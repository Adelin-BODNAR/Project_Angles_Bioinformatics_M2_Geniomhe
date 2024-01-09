import json
path_file=["/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/m2_geniomhe_rna_project/data/SPOT-RNA-1D/test.json",
"/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/Test_DSSR_theta.json",
"/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/m2_geniomhe_rna_project/data/SPOT-RNA-1D/training.json",
"/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/Train_DSSR_theta.json"]
nom=["SPOT","SPOT","OUR_MODEL","OUR_MODEL"]
nomT=["Test","Train","Test","Train"]
count=0
def write_res(MAE,cle) : 
    global count
    with open ("/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/MAE_DSSR_"+nom[count]+"_"+nomT[count]+".txt",'a' ) as res_file :
        res_file.write(str(cle)+" : \nMAE : "+str(MAE)+"\n")

def calcul_MAE (value1,value2) : 
    angle_pred=0
    angle_true=0
    for i in range(min(len(value1)-1,len(value2)-1)) : 
        angle_pred+=1
        if value1[i]==value2[i] : 
            angle_true+=1
    MAE=abs(angle_pred-angle_true)
    return(MAE)
        
for path in range(0,len(path_file)-1,2) : 
    with open(path_file[path],"r") as file_1 :
        with open(path_file[path+1],"r") as file_2 : 
            data_json_1= json.load(file_1)
            data_json_2=json.load(file_2)
            for cle1, valeur1 in data_json_1.items():
                for cle2,valeur2 in data_json_2.items():
                    if (cle1==cle2) : 
                            MAE=calcul_MAE(valeur1['angles']['theta'],valeur2['angles']['theta']) 
                            write_res(MAE,cle1)
    count+=1