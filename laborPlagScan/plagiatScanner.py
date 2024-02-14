import ast
import os
import threading
from tkinter import messagebox
import math
import re

import laborPlagScan.fileEditor as FileEditor
import laborPlagScan.Gui.mainGUI as mainGUI
import laborPlagScan.basicConfig as basicConfig
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


def start_plagscan(selected_path, mainGui: mainGUI):
    """Starts the PlagiatScanner, which compares all files in the students folder with each other"""
    # read filter.txt
    Filter.readFilter()

    if selected_path == "":
        messagebox.showerror("Fehler", "Keine ZIP-Datei ausgewählt!")
        return
    elif selected_path.endswith(".zip"):
        mainGUI.GUI.info_textline.config(text="ZIP-Datei wird entpackt...")
        selected_path = FileEditor.extract_zip(selected_path)
        mainGUI.GUI.info_textline.config(text="ZIP-Datei entpackt")

    mainGUI.GUI.info_textline.config(text="Files werden entpackt...")
    try:
        students_folder = FileEditor.unpackZipFiles(selected_path)
    except UnboundLocalError:
        mainGUI.GUI.info_textline.config(text="")
        messagebox.showerror("Fehler", "ZIP-Dateien der Einzellabore nicht gefunden!")
        return
    mainGUI.GUI.info_textline.config(text="Files entpackt")
    mainGUI.GUI.info_textline.config(text="PlagiatScanner wird gestartet...")
    plagscan(students_folder)
    mainGUI.GUI.remove_progressbar()
    mainGui.create_open_result_button(None)
    mainGUI.GUI.info_textline.config(text="PlagiatScanner abgeschlossen")


# def file_to_list(filepath: str) -> list:
#     """Converts a file to a list of lines, each line is a list with the line number and the line itself"""
#     with open(filepath, 'r') as file:
#         try:
#             lines = file.readlines()
#         except UnicodeDecodeError as e:
#             basicConfig.handle_exception(type(e), e, None, "Mindestens eine Datei konnte nicht gelesen werden!", "File: " + filepath + " konnte nicht gelesen werden!")
#             return []
#
#     new_lines = []
#     i = 0
#     for line in lines:
#         if line.count(";") > 1:
#             lineSplits = line.count(";") - 1
#             multi_line = line.replace(";", ";SplitHERE", lineSplits).split("SplitHERE")
#             for j in multi_line:
#                 line_list = [i, j]
#                 new_lines.append(line_list)
#                 i += 1
#             continue
#         line_list = [i, line]
#         new_lines.append(line_list)
#         i += 1
#
#     return new_lines


# def replace_words_in_file(file_list: list, word_list: set, java_operator_set: set) -> list:
#     """Replaces all variables in a file with a placeholder and deletes all comments, and blank lines"""
#     new_lines = []
#     commentblock = False
#     for line in file_list:
#         new_line = line[:]
#         if '/**' in new_line[1]:
#             commentblock = True
#             continue
#         elif '*/' in new_line[1]:
#             commentblock = False
#             continue
#         elif commentblock:
#             continue
#         else:
#             if '//' in new_line[1]:
#                 new_line[1] = new_line[1].split('//')[0] + '\n'
#
#         # Entfernen von "{" und "}" in der Zeile da diese an verschiedenen Stellen gesetzt sein können
#         new_line[1] = new_line[1].replace('{', '').replace('}', '')
#
#         # Erntferenen von Leeren Zeilen
#         if new_line[1].strip() == "":
#             continue
#
#         if re.search(r'System\.out\.println\("?\s*(?:\\n|\\t)*\s*"?\);', new_line[1]):
#             continue
#
#         words = re.findall(r'\b\w+\b', new_line[1])
#         for word in words:
#             if word not in word_list and word not in java_operator_set:
#                 new_line[1] = re.sub(r'\b' + re.escape(word) + r'\b', 'x', new_line[1])
#
#         # leerzeichen um Java zeichen und Operatoren entfernen
#         pattern = r'\s*(' + '|'.join([re.escape(ch) for ch in sorted(java_syntax_chars, key=len, reverse=True)]) + r')\s*'
#         new_line[1] = re.sub(pattern, r'\1', new_line[1])
#
#         # alles innerhalb von Anführungszeichen ersetzen durch ein "x"
#         new_line[1] = re.sub(r'(["\']).*(["\'])', 'x', new_line[1])
#         new_lines.append(new_line)
#
#     return new_lines


# def find_java_files(folder_path):
#     """Returns a dictionary with all java files in the given folder and its subfolders,
#     while ignoring folders in the ignore_folders list and ignoring case."""
#     ignore_folders = ["__MACOSX"]
#     ignore_files = []
#
#     # sammle Files die ignoriert werden sollen
#     with open('./filter.txt', 'r') as f:
#         filter_list = ast.literal_eval(f.read())
#
#     for filter_str in filter_list:
#         if isinstance(filter_str, dict):
#             settings_dict = filter_str
#             continue
#
#         readed_filter = filter_str.split(":")
#         if readed_filter[0] == "Regex":
#             continue
#         elif readed_filter[0] == "File":
#             ignore_files.append(readed_filter[1].strip().lower())
#         else:
#             continue
#
#     # Konvertiere die Liste der zu ignorierenden Ordner in Kleinbuchstaben
#     ignore_folders = [folder.lower() for folder in ignore_folders]
#
#     java_files = {}
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             if file.lower() in ignore_files:
#                 continue
#             if file.lower().endswith(".java"):
#                 if not any(folder in root.lower().split(os.sep) for folder in ignore_folders):
#                     java_files[file] = os.path.join(root, file)
#     return java_files


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


# def filter_lines(file_as_list: list) -> list:
#     """Filters all lines from a file that contain a string from the filter.txt file"""
#     regexpattern_list = []
#     regexpattern_list_pre = []
#     filter_strings = []
#     files_list = []
#     settings_dict = {}
#     with open('./filter.txt', 'r') as f:
#         filter_list = ast.literal_eval(f.read())
#
#     for filter_str in filter_list:
#         if isinstance(filter_str, dict):
#             settings_dict = filter_str
#             continue
#
#         readed_filter = filter_str.split(":")
#         if readed_filter[0] == "Regex":
#             regexpattern_list_pre.append(readed_filter[1])
#         elif readed_filter[0] == "File":
#             continue
#         else:
#             filter_strings.append(filter_str)
#
#     filtered_lines = []
#     for regex_code in regexpattern_list_pre:
#         regexpattern_list.append(re.compile(regex_code))
#
#     for line in file_as_list:
#         if not any(exclude_string in line for exclude_string in filter_strings) and not any(
#                 regex_pattern.search(line[1]) for regex_pattern in regexpattern_list):
#             if settings_dict["ignorePrintStatemants"] == 1:
#                 if "System.out.print" in line[1]:
#                     continue
#             filtered_lines.append(line)
#
#     return filtered_lines


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
                if i >= len(file1_lines):
                    if count >= 5:
                        plag_list.append([start_datei1, file1_lines[i - 1][0], start_datei2, file2_lines[j][0]])
                    break
            else:
                if count >= 5:
                    plag_list.append([start_datei1, file1_lines[i][0], start_datei2, file2_lines[j][0]])
                count = 0
        i += 1

    # result_code_list = []
    # for plagiat in plag_list:
    #     result_code_list.append(
    #         [get_plagcode_from_filelist(file1_lines, plagiat), plagiat[0], plagiat[1], plagiat[2], plagiat[3]])
    #
    # return result_code_list
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
    mainGUI.GUI.info_textline.config(text="Files werden gesammelt...")
    student_dict = {}

    #TODO: Progressbar einfügen
    studenten = []
    for student_folder in student_folders_list:
        studenten.append(Student(student_folder, students_folder))

    # Wenn keine Studenten bzw Java-Dateien gefunden wurden, dann abbrechen
    if len(studenten) == 0:
        mainGUI.display_msgbox("Keine Studenten gefunden", "Es wurden keine Studenten gefunden. Bitte überprüfen Sie die ZIP-Datei.")
        return

    # 3. Schleife für alle Kombinationen von Studenten
    plagiat_list = []
    mainGUI.GUI.set_progressbar_start((math.pow(len(student_folders_list), 2) / 2))
    mainGUI.GUI.info_textline.config(text="Files werden verglichen...")
    for i, student1 in enumerate(studenten):
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
            if PlagiatPaar.getPlagiatAnteil() > Filter.getPlagiatAlert():
                plagiat_list.append(PlagiatPaar)

    # 4. Stats erstellen
    stats_list = create_stats(plagiat_list)
    stats_text = "PlagScan abgeschlossen!\n\nAnzahl Plagiate: " + str(stats_list[0]) + \
                 "\nAnzahl Studenten mit Plagiat: " + str(stats_list[1])
    threading.Thread(target=mainGUI.display_msgbox, args=("PlagScan", stats_text)).start()

    # 5. Ergebnis Sturktur erstellen und sortieren
    plagiat_list_sorted = sorted(plagiat_list, key=lambda paar: paar.getPlagiatAnteil(), reverse=True)

    # 6. Ergebnis speichern
    FileEditor.save_auswertung_to_file(plagiat_list_sorted)
