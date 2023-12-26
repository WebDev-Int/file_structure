import os
import tkinter as tk
from tkinter import filedialog

def generate_structure():
    folder_path = selected_folder.get()
    if not folder_path:
        return  # No folder selected

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

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
                if os.path.isdir(new_path) and not excluded_folders.get(item, False):
                    format_directory(new_path, indent + "│   ")

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        format_directory(folder_path)

        # Display the generated structure in the text area
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, structure_text)

    else:
        print(f"Folder '{folder_name}' not found.")

def select_folder():
    folder_path = filedialog.askdirectory()
    selected_folder.set(folder_path)
    pre_scan()

def toggle_include(folder):
    excluded_folders[folder] = not excluded_folders.get(folder, False)
    generate_structure()

def pre_scan():
    folder_path = selected_folder.get()
    global excluded_folders

    excluded_folders = {}

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for item in dirs:
                if item not in excluded_folders:
                    excluded_folders[item] = False

        clear_checkboxes()
        for item in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, item)):
                checkbox_vars[item] = tk.BooleanVar()
                checkbox_vars[item].set(not excluded_folders.get(item, False))
                checkboxes[item] = tk.Checkbutton(main_root, text=f"{item} {'(Excluded)' if excluded_folders.get(item, False) else '(Included)'}", variable=checkbox_vars[item], command=lambda f=item: toggle_include(f))
                checkboxes[item].pack()

def clear_checkboxes():
    for checkbox in checkboxes.values():
        checkbox.pack_forget()
        checkbox.destroy()
    checkboxes.clear()
    checkbox_vars.clear()

# Create the main window
main_root = tk.Tk()
main_root.title("Folder Structure Generator")

# Variable to store selected folder path
selected_folder = tk.StringVar()

# Button to select folder
select_button = tk.Button(main_root, text="Select Folder", command=select_folder)
select_button.pack()

# Text area to display generated structure and preview
text_area = tk.Text(main_root, wrap="word", width=50, height=40)
text_area.pack()

# Create checkboxes for root folders
checkboxes = {}
checkbox_vars = {}

# Initialize folder structure on startup
pre_scan()

excluded_folders = {}

def generate_structure_file():
    preview_text = text_area.get('1.0', tk.END)
    # Write to a file based on the content in the text area
    with open("generated_structure.txt", 'w') as file:
        file.write(preview_text)

generate_button = tk.Button(main_root, text="Generate File", command=generate_structure_file)
generate_button.pack()

main_root.mainloop()
