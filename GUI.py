import tkinter as tk
from tkinter import filedialog, messagebox

import FileEditor
import PlagiatScanner


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
        selected_path = zip_selection.cget("text")
        if selected_path == "":
            info_textline.config(text="Keine ZIP-Datei/Ordner ausgewählt!")
            return
        elif selected_path.endswith(".zip"):
            info_textline.config(text="ZIP-Datei wird entpackt...")
            selected_path = FileEditor.extract_zip(selected_path)
            info_textline.config(text="ZIP-Datei entpackt")

        info_textline.config(text="Files werden entpackt...")
        try:
            students_folder = FileEditor.unpackZipFiles(selected_path)
        except UnboundLocalError:
            info_textline.config(text="")
            messagebox.showerror("Fehler", "ZIP-Dateien der Einzellabore nicht gefunden!")
            return
        info_textline.config(text="Files entpackt")
        info_textline.config(text="PlagiatScanner wird gestartet...")
        PlagiatScanner.plagscan(students_folder)

    root = tk.Tk()
    root.title("PlagScan GUI")

    zip_button = tk.Button(root, text="ZIP auswählen", command=select_zip)
    zip_button.pack()

    zip_selection = tk.Label(root, text="")
    zip_selection.pack()

    start_button = tk.Button(root, text="PlagScan starten", command=start_plagscan)
    start_button.pack()

    info_textline = tk.Label(root, text="")
    info_textline.pack()

    root.mainloop()