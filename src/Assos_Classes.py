import json
import re
import sys
import os

def read_intervals_from_file(file_path):
    with open(file_path, 'r') as file:
        line = file.readline()
        start_index = line.find('(')
        line = line[start_index:]
        intervals = []
        for interval in line.split():
            numbers = [float(num) for num in re.findall(r'-?\d+\.?\d*', interval)]
            intervals.append(tuple(numbers))
    return intervals

def assign_angle_class(angle_value, intervals):
    if angle_value is None:
        return 0
    for i, interval in enumerate(intervals):
        if interval[0] < angle_value <= interval[1]:
            return i + 1
    return 0

# Chemin du fichier de sortie
output_file_path = sys.argv[3]
input_file=sys.argv[1]
interval_path=sys.argv[2]
# Charger les données depuis le fichier JSON
with open(input_file, 'r') as json_file:
    data = json.load(json_file)

# Charger les intervalles depuis le fichier texte
intervals = read_intervals_from_file(interval_path)

# Ouvrir le fichier de sortie en mode écriture
with open(output_file_path, 'w') as output_file:
    # Rediriger la sortie vers le fichier
    for rp_key, rp_data in data.items():
        print(rp_key)
        if "angles" in rp_data and "theta" in rp_data["angles"]:
            angles_theta = rp_data["angles"]["theta"]
            nucleotides = rp_data.get("sequence", "")
            
            for angle, nucleotide in zip(angles_theta, nucleotides):
                angle_value = float(angle) if angle != "NA" else None
                angle_class = assign_angle_class(angle_value, intervals)
                output_line = f"{rp_key} - Nucléotide: {nucleotide}, Angle Theta: {angle_value}, Classe: {angle_class}\n"
                output_file.write(output_line)
