import numpy as np
import pandas as pd

# 1. File paths and settings
input_file = 'input.xlsx'  # Replace with your input file name
output_file = 'output.xlsx'  # Name of the new file to be created
rows_per_column = 9  # Number of cells per column

# 2. Read the Excel file (header=None ensures the very first row isn't treated as a title)
df = pd.read_excel(input_file, header=None)

# 3. Extract the single column into a 1D list/array and remove any trailing blank cells
data = df.iloc[:, 0].dropna().to_numpy()

# 4. Pad the end with empty values (None) if the total count isn't a multiple of 9
remainder = len(data) % rows_per_column
if remainder != 0:
  padding_needed = rows_per_column - remainder
  data = np.append(data, [None] * padding_needed)

# 5. Reshape the data into 9 rows, filling column-by-column ('F' stands for Fortran/column-major order)
reshaped_data = data.reshape((rows_per_column, -1), order='F')

# 6. Convert back to a DataFrame and save to a new Excel file without row/column headers
output_df = pd.DataFrame(reshaped_data)
output_df.to_excel(output_file, index=False, header=False)

print(f'Successfully converted {input_file} to {output_file}!')
