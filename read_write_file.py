# Define file paths
source_file = "input.txt"
destination_file = "output.txt"

try:
    # Open and read the source file
    with open(source_file, "r", encoding="utf-8") as infile:
        content = infile.read()

        # Open and overwrite the destination file
    with open(destination_file, "w", encoding="utf-8") as outfile:
        outfile.write(content)

    print("File successfully copied in Python!")
except FileNotFoundError:
    print(f"Error: The file {source_file} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
