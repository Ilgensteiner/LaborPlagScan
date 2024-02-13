import ast
import os

import file


class Student:
    def __init__(self, name, extractedFolders):
        self.name = name
        self.folderPath = os.path.join(extractedFolders, name)
        self.files = []  # Initialisiert eine leere Liste für File-Objekte
        self.zeilenGes = 0  # Initialisiert die Gesamtzahl der Zeilen auf 0

        self.find_java_files()
        self.getZeilenGes()

    def find_java_files(self):
        """Returns a list with all java files in the given folder and its subfolders,
        while ignoring folders in the ignore_folders list and ignoring case."""
        ignore_folders = ["__MACOSX"]
        ignore_files = []

        # TODO: Austauschen durch Filter-Klasse
        # sammle Files die ignoriert werden sollen
        with open('./filter.txt', 'r') as f:
            filter_list = ast.literal_eval(f.read())

        for filter_str in filter_list:
            if isinstance(filter_str, dict):
                settings_dict = filter_str
                continue

            readed_filter = filter_str.split(":")
            if readed_filter[0] == "Regex":
                continue
            elif readed_filter[0] == "File":
                ignore_files.append(readed_filter[1].strip().lower())
            else:
                continue

        # Konvertiere die Liste der zu ignorierenden Ordner in Kleinbuchstaben
        ignore_folders = [folder.lower() for folder in ignore_folders]

        for root, dirs, files in os.walk(self.folderPath):
            for file in files:
                if file.lower() in ignore_files:
                    continue
                if file.lower().endswith(".java"):
                    if not any(folder in root.lower().split(os.sep) for folder in ignore_folders):
                        self.files.append(File(file, os.path.join(root, file)))

    def getZeilenGes(self):
        """Returns the total number of lines of all files in the folder."""
        for file in self.files:
            self.zeilenGes += file.lineCount

