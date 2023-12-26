import os
import tkinter as tk
from tkinter import filedialog

def generate_structure():
    folder_path = selected_folder.get()
    if not folder_path:
        return  # No folder selected

    # Get folder name
    folder_name = os.path.basename(folder_path)
    structure_text = f"{folder_name}/\n"

    # Function to format the directory structure recursively
    def format_directory(dir_path, indent=""):
        nonlocal structure_text
        for item in os.listdir(dir_path):
            if not item.startswith('.') and not item.startswith('__'):
                structure_text += f"{indent}├── {item}\n"
                new_path = os.path.join(dir_path, item)
                if os.path.isdir(new_path):
                    format_directory(new_path, indent + "│   ")
    
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        format_directory(folder_path)

        # Write file structure to a text file
        file_name = f"{folder_name}_structure.txt"
        with open(file_name, 'w') as file:
            file.write(structure_text)

        # Create a window to display the generated structure
        structure_window = tk.Tk()
        structure_window.title(f"Folder Structure for '{folder_name}'")

        text_area = tk.Text(structure_window, wrap="word", width=50, height=20)
        text_area.insert(tk.END, structure_text)
        text_area.pack(fill="both", expand=True)

        structure_window.mainloop()
    else:
        print(f"Folder '{folder_name}' not found.")

def select_folder():
    folder_path = filedialog.askdirectory()
    selected_folder.set(folder_path)

# Create the main window
root = tk.Tk()
root.title("Folder Structure Generator")

# Variable to store selected folder path
selected_folder = tk.StringVar()

# Button to select folder
select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack()

# Button to generate structure
generate_button = tk.Button(root, text="Generate Structure", command=generate_structure)
generate_button.pack()

root.mainloop()
