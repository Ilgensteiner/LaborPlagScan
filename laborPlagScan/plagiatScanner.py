import os
import threading
from tkinter import messagebox
import math

import laborPlagScan.fileEditor as FileEditor
import laborPlagScan.Gui.mainGUI as mainGUI
from laborPlagScan.DataModels.plagiat import Plagiat
from laborPlagScan.DataModels.plagiatPaare import PlagiatPaare
from laborPlagScan.DataModels.student import Student
from laborPlagScan.filter import Filter

java_syntax_words = {"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue",
                     "default", "double", "do", "else", "enum", "extends", "final", "finally", "float", "for", "goto",
                     "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package",
                     "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch",
                     "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while", "true",
                     "false", "null", "String", "System", "out", "println", "print", "Scanner", "nextInt", "nextLine",
                     "new", "File", "exists", "length", "length()", "charAt", "substring", "equals", "equalsIgnoreCase",
                     "next", "hasNext", "hasNextLine", "hasNextInt", "hasNextDouble", "hasNextBoolean", "hasNextByte",
                     "hasNextFloat", "hasNextLong", "hasNextShort", "hasNextBigDecimal", "hasNextBigInteger",
                     "hasNextBigInteger", "hasNextBigDecimal", "hasNextBigInteger", "Main", "main", "args", "array",
                     "temp", "Exception", "printStackTrace", "getMessage", "abstrakt", "@override", "@Override",
                     "Override", "toString", "equals", "hashCode", "clone", "compareTo", "finalize", "getClass",
                     "IllegalArgumentException"}

java_syntax_chars = {"{", "}", "(", ")", "[", "]", ";", "=", ":", ",", "+", "-", "*", "%", "++", "--", "==", "!=", ">",
                     "<", ">=", "<=", "&&", "||", "!", "&", "|", "^", "~", "<<", ">>", ">>>", "+=", "-=", "*=", "/=",
                     "%=", "&=", "|=", "^=", "<<=", ">>=", ">>>=", "?"}


def start_plagscan(selected_path, Gui: mainGUI):
    """Starts the PlagiatScanner, which compares all files in the students folder with each other"""
    # read filter.txt
    Filter.readFilter()

    if selected_path == "":
        messagebox.showerror("Fehler", "Keine ZIP-Datei ausgewählt!")
        return
    elif selected_path.endswith(".zip"):
        mainGUI.GUI.set_info_text("ZIP-Datei wird entpackt...")
        selected_path = FileEditor.extract_zip(selected_path)
        mainGUI.GUI.set_info_text("ZIP-Datei entpackt")

    mainGUI.GUI.set_info_text("Files werden entpackt...")
    try:
        students_folder = FileEditor.unpackZipFiles(selected_path)
    except UnboundLocalError:
        mainGUI.GUI.set_info_text("")
        messagebox.showerror("Fehler", "ZIP-Dateien der Einzellabore nicht gefunden!")
        return
    mainGUI.GUI.set_info_text("Files entpackt")
    mainGUI.GUI.set_info_text("PlagiatScanner wird gestartet...")
    plagscan(students_folder)
    mainGUI.GUI.remove_progressbar()
    Gui.create_open_result_button(None)
    mainGUI.GUI.set_info_text("PlagiatScanner abgeschlossen")


def get_plagcode_from_filelist(file_as_list: list, plag_result: list) -> str:
    """Returns the plagiat code from a file as a string"""
    plag_code = ""
    for line in file_as_list:
        if line[0] >= plag_result[0] or line[0] <= plag_result[1]:
            plag_code += line[1]
        if line[0] > plag_result[1]:
            break

    # for i in range(plag_result[0], plag_result[1] + 1):
    #     plag_code += file_as_list[i][1]
    return plag_code


def compare_files(file1_lines: list, file2_lines: list) -> list:
    """Compares two files and returns the lines of code that are the same in both files"""

    start_datei1 = 0
    start_datei2 = 0
    plag_list = []

    i = 0
    while i < len(file1_lines):
        count = 0
        for j in range(len(file2_lines)):
            if file1_lines[i][1] == file2_lines[j][1]:
                if count == 0:
                    start_datei1 = file1_lines[i][0]
                    start_datei2 = file2_lines[j][0]
                count += 1
                i += 1
                # Wenn Abstand zwischen den Zeilen größer als 15, dann kein zusammenhängendes Plagiat
                if i >= len(file1_lines) or file1_lines[i][0] - file1_lines[i-1][0] >= 15:
                    if count >= 5:
                        plag_list.append([start_datei1, file1_lines[i - 1][0], start_datei2, file2_lines[j][0]])
                    break
            else:
                if count >= 5:
                    plag_list.append([start_datei1, file1_lines[i][0], start_datei2, file2_lines[j][0]])
                count = 0
        i += 1
    return plag_list


def create_stats(plagiat_list: PlagiatPaare) -> list:
    """Creates a list with the stats for the given dictionary
        :return [Anz Plagiate, Anz Studenten, Plagiate pro Student, Plagiate pro Studenten Paar]"""
    # Zählen wie oft ein Student plagiiert, hat
    plagiatabschitte = 0
    for plagiat in plagiat_list:
        plagiatabschitte += len(plagiat.plagiate)

    return [plagiatabschitte, len(plagiat_list)]


def plagscan(students_folder: str):
    """Scans all files in the given folder for plagiarism"""
    # 1. Sammeln aller Java-Dateien für jeden Studenten
    student_folders_list = os.listdir(students_folder)
    mainGUI.GUI.set_progressbar_start(len(student_folders_list))
    mainGUI.GUI.set_info_text("Files werden gesammelt...")
    student_dict = {}

    studenten = []
    for student_folder in student_folders_list:
        studenten.append(Student(student_folder, students_folder))
        mainGUI.GUI.update_progressbar_value(1)

    # Wenn keine Studenten bzw Java-Dateien gefunden wurden, dann abbrechen
    if len(studenten) == 0:
        mainGUI.display_msgbox("Keine Studenten gefunden", "Es wurden keine Studenten gefunden. Bitte überprüfen Sie die ZIP-Datei.")
        return

    # 3. Schleife für alle Kombinationen von Studenten
    plagiat_list = []
    aiDetected_stud_list = []
    mainGUI.GUI.set_progressbar_start((math.pow(len(student_folders_list), 2) / 2))
    mainGUI.GUI.set_info_text("Files werden verglichen...")
    for i, student1 in enumerate(studenten):
        if student1.aiDetection:
            aiDetected_stud_list.append(student1)

        for student2 in list(studenten)[i + 1:]:
            PlagiatPaar = PlagiatPaare(student1, student2)
            for file1 in student1.files:
                for file2 in student2.files:
                    plagiat = compare_files(file1.linesAufbereitet, file2.linesAufbereitet)
                    if len(plagiat) == 0:
                        continue
                    else:
                        newPlagiat = Plagiat(file1, file2, plagiat)
                        PlagiatPaar.addPlagiat(newPlagiat)
            PlagiatPaar.countPlagiatZeilenGes()
            PlagiatPaar.calcPlagiatAnteil()
            if PlagiatPaar.plagiatAnteil > Filter.getPlagiatAlert():
                plagiat_list.append(PlagiatPaar)
            mainGUI.GUI.update_progressbar_value(1)

    # 4. Stats erstellen
    stats_list = create_stats(plagiat_list)
    stats_text = "PlagScan abgeschlossen!\n\nAnzahl Plagiate: " + str(stats_list[0]) + \
                 "\nAnzahl Studenten mit Plagiat: " + str(stats_list[1])
    threading.Thread(target=mainGUI.display_msgbox, args=("PlagScan", stats_text)).start()

    # 5. Ergebnis Sturktur erstellen und sortieren
    plagiat_list_sorted = sorted(plagiat_list, key=lambda paar: paar.plagiatAnteil, reverse=True)

    # 6. Ergebnis speichern
    FileEditor.save_auswertung_to_file([plagiat_list_sorted, aiDetected_stud_list])
