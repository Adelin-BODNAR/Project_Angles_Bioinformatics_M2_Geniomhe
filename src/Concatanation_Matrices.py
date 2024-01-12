import os
import pandas as pd

# Set the path to the folder containing the CSV files
folder_path = 'Test_matrices'

# Initialize an empty DataFrame to store the concatenated matrices
concatenated_df = pd.DataFrame()

# Iterate through each CSV file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # Read the CSV file into a DataFrame
        matrix_df = pd.read_csv(os.path.join(folder_path, file_name), index_col=0)

        # Concatenate the matrices vertically (along rows)
        concatenated_df = pd.concat([concatenated_df, matrix_df])

# Write the concatenated DataFrame to a new CSV file
concatenated_df.to_csv('AllTest_Matrices.csv')
