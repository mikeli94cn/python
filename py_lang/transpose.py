import pandas as pd

# 1. File paths
input_file = 'output.xlsx'  # Replace with your input file name
output_file = 'transposed_output.xlsx'  # Name of the new file to be created

# 2. Read the Excel file (header=None keeps the first row as regular data)
df = pd.read_excel(input_file, header=None)

# 3. Transpose the table (swaps rows to columns and columns to rows)
transposed_df = df.T

# 4. Save the flipped table to a new Excel file without extra row/column labels
transposed_df.to_excel(output_file, index=False, header=False)

print(f'Successfully transposed {input_file} to {output_file}!')
