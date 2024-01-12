import csv
import pandas as pd
csv_file_path = sys.agrv[1]
txt_file_path =sys.agrv[2]
output_csv_path = sys.agrv[3]
output_labls = sys.agrv[4]
with open(csv_file_path, 'r') as csv_file, open(txt_file_path, 'r') as txt_file, open(output_csv_path, 'w', newline='') as output_csv:
    csv_reader = csv.reader(csv_file, delimiter=',')  # Assurez-vous d'utiliser le délimiteur approprié
    csv_writer = csv.writer(output_csv, delimiter=',')
    
    for row in csv_reader:
        if row != ['0', '0', '0', '0']:
            line = txt_file.readline()
            line_value = line.strip() if line else '0'
            csv_writer.writerow(row + [line_value])
        else:

            csv_writer.writerow(row + ['0'])
            continue

df = pd.read_csv(output_csv_path, delimiter=',')

last_column = df.iloc[:, -1]

df_output = pd.DataFrame({df.columns[-1]: last_column})

df_output.to_csv(output_labls , index=False)
 
