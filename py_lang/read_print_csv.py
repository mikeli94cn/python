import csv

file_path = "data.csv"

try:
    with open(file_path, mode="r", encoding="utf-8") as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        # Loop through each row and print it to the console
        for row in csv_reader:
            # row is a list of strings: ['Value1', 'Value2', ...]
            print(" | ".join(row))

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
