import tkinter as tk
from tkinter import filedialog
import zipfile
import os


def extract_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        folder_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_path = os.path.join(os.path.dirname(zip_path), folder_name)
        zip_file.extractall(path=extract_path)
    return extract_path


def find_common_files(filenames, line_threshold):
    file_contents = {}
    common_files = {}
    for filename in filenames:
        with open(filename, 'r') as file:
            try:
                lines = file.readlines()
            except UnicodeDecodeError:
                continue
            for line in lines:
                if line not in file_contents:
                    file_contents[line] = [filename]
                else:
                    file_contents[line].append(filename)
            for content, file_list in file_contents.items():
                if len(file_list) >= line_threshold:
                    common_files[content] = file_list
    return common_files


if __name__ == '__main__':
    def select_zip():
        filepath = filedialog.askopenfilename(title="ZIP auswählen")
        if filepath:
            zip_selection.config(text=filepath)


    def start_plagscan():
        zip_path = zip_selection.cget("text")
        if zip_path:
            zip_folder_path = extract_zip(zip_path)
            zip_filenames = []
            for foldername, subfolders, filenames in os.walk(zip_folder_path):
                for filename in filenames:
                    if filename.endswith('.zip'):
                        zip_filenames.append(os.path.join(foldername, filename))
            all_filenames = zip_filenames.copy()
            all_filenames.append(zip_path)
            common_files = find_common_files(all_filenames, 10)  # Change line_threshold as needed
            with open('common_files.txt', 'w') as outfile:
                for content, file_list in common_files.items():
                    outfile.write("Content: " + content + "\n")
                    for filename in file_list:
                        outfile.write("File: " + filename + "\n")
                    outfile.write("\n")
            no_file_selected.config(text="Übereinstimmungen wurden in common_files.txt gespeichert.")
        else:
            no_file_selected.config(text="Bitte wählen Sie eine ZIP-Datei aus.")


    root = tk.Tk()
    root.title("PlagScan GUI")

    zip_button = tk.Button(root, text="ZIP auswählen", command=select_zip)
    zip_button.pack()

    zip_selection = tk.Label(root, text="")
    zip_selection.pack()

    start_button = tk.Button(root, text="PlagScan starten", command=start_plagscan)
    start_button.pack()

    no_file_selected = tk.Label(root, text="")
    no_file_selected.pack()

    root.mainloop()