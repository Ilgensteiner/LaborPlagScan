import json
import os
import zipfile
import tkinter as tk
from tkinter import filedialog

import mainGUI


def extract_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        folder_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_path = os.path.join(os.path.dirname(zip_path), folder_name)
        zip_file.extractall(path=extract_path)
    return extract_path


def unpackZipFiles(folder_path: str, gui: mainGUI):
    # 1. Liste aller Dateien im Ordner
    files = os.listdir(folder_path)
    zipfile_found = False

    # 1.1. Einstellen der Progressbar
    gui.set_progressbar_start(len(files))

    # 2. Schleife für alle Dateien im Ordner
    for file in files:
        gui.update_progressbar_value(1)
        # 3. Prüfen, ob Datei eine ZIP-Datei ist
        if not file.endswith('.zip'):
            continue

        zipfile_found = True

        # 4. Entpacken der ZIP-Datei
        file_path = os.path.join(folder_path, file)
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            extract_path = os.path.join(folder_path, "extracted", file.replace(".zip", ""))
            zip_file.extractall(path=extract_path)

    # 5. Wenn keine ZIP-Datei gefunden wurde, nach & in Unterordnern suchen
    if not zipfile_found:
        subfolders = os.listdir(folder_path)
        for subfolder in subfolders:
            subfolder_path = os.path.join(folder_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue
            extract_path = unpackZipFiles(subfolder_path, gui)
            return extract_path

    return os.path.dirname(extract_path)


def get_last_modified_file():
    folder_path = 'result'
    if not os.path.exists(folder_path):
        return None
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        return None
    last_modified_file = max(files, key=os.path.getmtime)
    last_modified_file = os.path.basename(last_modified_file).split(".")[0]
    return last_modified_file


def save_auswertung_to_file(d: dict, path="result/", filename="last_result"):
    """Saves the auswertung dictionary to a json-file"""
    if path is None:
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory()
        root.destroy()

    filename = filename.split('.')[0] + '.json'
    path = os.path.join(path, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(d, f)


def load_auswertung_from_file(filename: str) -> dict:
    # Erstelle den Pfad zur Datei im Ordner "result"
    filepath = f"result/{filename}.json"

    # Öffne die Datei und lese das dict aus
    with open(filepath, "r") as file:
        data = json.load(file)

    # Gib das dict zurück
    return data


def read_file(filepath, lines=None):
    # TODO: Vieleicht noch paar Zeilen drunter und drüber mit ausgeben (+ Markieren wann eig. Start und Ende ist)
    with open(filepath, 'r') as file:
        content = file.readlines()
        if lines:
            start, end = lines
            content = content[start-1:end]
        return ''.join(content)
