import json
path_files=[sys.argv[1],    
sys.argv[2],                

sys.argv[3],   
sys.argv[4]]

DSSR_path=[sys.argv[9],sys.argv[10]]

nom=[sys.argv[5],sys.argv[6]]
nomT=[sys.argv[7],sys.argv[8]]
count=0
def write_res(MAE,cle) : 
    global count
    with open ("/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/MAE_DSSR_"+nom[count]+"_"+nomT[count]+".txt",'a' ) as res_file :
        res_file.write(str(cle)+" : \tMAE : "+str(MAE)+"\n")

def calcul_MAE (value1,value2) : 
    angle_pred=0
    angle_true=0
    for i in range(min(len(value1)-1,len(value2)-1)) : 
        angle_pred+=1
        if value1[i]==value2[i] : 
            angle_true+=1
    MAE=abs(angle_pred-angle_true)
    return(MAE)
def prep_val(file1,file2) : 
    for cle1, valeur1 in file1.items():
        for cle2,valeur2 in file2.items():
            if (cle1==cle2) : 
                MAE=calcul_MAE(valeur1['angles']['theta'],valeur2['angles']['theta']) 
                write_res(MAE,cle1)
                
for name in nom : 
    for end in nomT  :
        outfile.append(end+"_"+name+".txt")

for file in range(len(path_files)):
    if file < len(path_files) / 2:
        file1 = pd.read_json(path_files[file])
        file2 = pd.read_json(DSSR_path[0])
        prep_val(file1, file2)
    else:
        file1 = pd.read_json(path_files[file])
        file2 = pd.read_json(DSSR_path[1])
        prep_val(file1, file2)
    count+=1
