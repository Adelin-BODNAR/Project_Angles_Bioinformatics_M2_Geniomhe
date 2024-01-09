import json
import sys
import os

path = sys.argv[1]
output = sys.argv[2]


def write_output(data_json) : 
    res_json={}
    for cle, valeur in data_json.items():
        sequence = valeur['sequence']
        theta_angle = valeur['angles']['theta']

    # Enregistrer les informations dans la nouvelle structure
        res_json[cle] = {
            'sequence': sequence,
            'angles' :{
            'theta': theta_angle
            }
            }
    with open(output, 'w') as fichier_sortie:
        json.dump(res_json, fichier_sortie, indent=2)


with open(path,"r") as file_json :
    data_json= json.load(file_json)
    write_output(data_json)