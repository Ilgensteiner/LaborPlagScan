import os

from laborPlagScan.DataModels.file import File
from laborPlagScan.filter import Filter


class Student:
    def __init__(self, name, extractedFolders):
        self.name = name
        self.folderPath = os.path.join(extractedFolders, name)
        self.files = []  # Initialisiert eine leere Liste für File-Objekte
        self.zeilenGes_ungefiltert = 0  # Initialisiert die Gesamtzahl der Zeilen auf 0
        self.zeilenGes_gefiltert = 0  # Initialisiert die Gesamtzahl der gefilterten Zeilen auf 0
        self.aiDetection = False

        self.find_java_files()
        self.getZeilenGes()

    def find_java_files(self):
        """Returns a list with all java files in the given folder and its subfolders,
        while ignoring folders in the ignore_folders list and ignoring case."""
        ignore_folders = ["__MACOSX"]
        ignore_files = Filter.getIgnoreFiles()

        # Konvertiere die Liste der zu ignorierenden Ordner in Kleinbuchstaben
        ignore_folders = [folder.lower() for folder in ignore_folders]

        for root, dirs, files in os.walk(self.folderPath):
            for file in files:
                if file.lower() in ignore_files:
                    continue
                if file.lower().endswith(".java"):
                    if not any(folder in root.lower().split(os.sep) for folder in ignore_folders):
                        java_file = File(file, os.path.join(root, file))
                        self.files.append(java_file)
                        if java_file.aiDetection:
                            self.aiDetection = True

        # Sortiere die Dateien nach ihrem Namen
        self.files.sort(key=lambda x: x.name)

    def getZeilenGes(self):
        """Returns the total number of lines of all files in the folder."""
        for file in self.files:
            self.zeilenGes_ungefiltert += file.lineCount_ungefiltert
            self.zeilenGes_gefiltert += file.lineCount_gefiltert

