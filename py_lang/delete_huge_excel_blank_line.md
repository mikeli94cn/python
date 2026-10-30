Here is the Python script optimized for processing very large Excel files.
                                   
For a file with a million rows, loading the entire dataset into memory using standard libraries can cause your system to run out of RAM. To handle this efficiently, this script uses openpyxl in read-only and write-only modes, which streams the data line by line and keeps memory usage extremely low.

```python
import openpyxl

def remove_null_orders(input_file, output_file, target_column_name):
    print("Opening input file (Read-Only Mode)...")
    wb_in = openpyxl.load_workbook(input_file, read_only=True, data_only=True)
    sheet_in = wb_in.active

    print("Creating output file (Write-Only Mode)...")
    wb_out = openpyxl.Workbook(write_only=True)
    sheet_out = wb_out.create_sheet()

    # Read the header row to find the target column index
    row_iter = sheet_in.iter_rows(values_only=True)
    try:
        header_row = next(row_iter)
    except StopIteration:
        print("The file is empty.")
        return

    try:
        # Excel column indices are 0-based in this iterator
        target_col_idx = header_row.index(target_column_name)
    except ValueError:
        print(f"Error: Column '{target_column_name}' not found in the header.")
        return

    # Write the header to the new file
    sheet_out.append(header_row)

    print("Processing rows... This may take a couple of minutes for 1 million rows.")
    processed_count = 0
    deleted_count = 0

    for row in row_iter:
        processed_count += 1
        
        # Check if the specific column is None (null) or a string like '#N/A'
        val = row[target_col_idx]
        if val is None or str(val).strip().upper() == '#N/A':
            deleted_count += 1
            continue  # Skip writing this row
            
        sheet_out.append(row)

        # Optional progress counter
        if processed_count % 100000 == 0:
            print(f"  Processed {processed_count} rows...")

    print("Saving the new file...")
    wb_out.save(output_file)
    
    print("Done!")
    print(f"Total rows evaluated: {processed_count}")
    print(f"Rows removed (null or #N/A): {deleted_count}")
    print(f"Rows remaining: {processed_count - deleted_count}")

# --- Configuration ---
INPUT_EXCEL = "your_huge_file.xlsx"
OUTPUT_EXCEL = "cleaned_file.xlsx"
COLUMN_TO_CHECK = "call_online_order_id_new"

if __name__ == "__main__":
    remove_null_orders(INPUT_EXCEL, OUTPUT_EXCEL, COLUMN_TO_CHECK)
```

Why this approach works best for 1,000,000+ rows:

*  Memory Efficient: By utilizing read_only=True and write_only=True, the script never loads all 1 million rows into your RAM at once. It streams them sequentially, preventing your computer from crashing.
*  Handles Multiple "Null" Types: The script safely checks for native Excel None values as well as literal #N/A text errors.
*  Non-Destructive: It creates a brand-new file (cleaned_file.xlsx) instead of modifying your original file, keeping your original data completely safe.

Alternative (Fastest Alternative if you have enough RAM)

If your computer has a lot of RAM (e.g., 16GB+ available) and you want maximum speed, you can use the Pandas Library:
```python
import pandas as pd

# Load, drop nulls, and save
df = pd.read_excel('your_huge_file.xlsx')
df = df.dropna(subset=['call_online_order_id_new'])
df.to_excel('cleaned_file.xlsx', index=False)
```
Note: While Pandas is faster, it attempts to load the entire 1 million row sheet into memory at once, which frequently triggers MemoryError crashes on larger Excel sheets.
If you run into issues, let me know:
*  Approximately how much RAM your computer has
*  If your file contains multiple sheets or just one
*  If you encounter any specific error messages when running it
