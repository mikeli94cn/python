import csv
import tkinter as tk
from tkinter import scrolledtext

# 1. Read the CSV File content
file_path = "data.csv"
formatted_content = ""

try:
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Join cells with standard tab characters for visual alignment
            formatted_content += " \t|\t ".join(row) + "\n"
except FileNotFoundError:
    formatted_content = f"Error: The file '{file_path}' was not found."

    # 2. Create the built-in Tkinter Window
window = tk.Tk()
window.title("Tkinter CSV Viewer")
window.geometry("500x400")

# Add a native scrollable text area component
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
text_area.insert(tk.INSERT, formatted_content)

# Make the text area fill the entire window frame
text_area.pack(expand=True, fill="both")

# Prevent users from editing the CSV output text
text_area.configure(state="disabled")

# Run the window display main event loop
window.mainloop()
