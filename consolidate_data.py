import pandas as pd
import os
import glob

# Define the path to the data directory
data_dir = 'data'
output_file = os.path.join(data_dir, 'consolidated.csv')

# Find all .xls files in the data directory
xls_files = glob.glob(os.path.join(data_dir, '*.xls'))

# Create a list to hold the dataframes
all_data = []

# Loop through the files and read them into a pandas dataframe
for f in xls_files:
    print(f"Reading {f}...")
    df = pd.read_excel(f)
    all_data.append(df)

# Concatenate all the dataframes into one
consolidated_df = pd.concat(all_data, ignore_index=True)

# Save the consolidated dataframe to a csv file
consolidated_df.to_csv(output_file, index=False)

print(f"\nSuccessfully consolidated {len(xls_files)} files into {output_file}")
print(f"Total rows in consolidated file: {len(consolidated_df)}") 