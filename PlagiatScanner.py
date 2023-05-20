import ast
import os
import threading
import tkinter
from tkinter import messagebox
import math
import re

import FileEditor
import mainGUI

java_syntax = {"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue",
               "default", "double", "do", "else", "enum", "extends", "final", "finally", "float", "for", "goto",
               "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package",
               "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch",
               "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while", "true",
               "false", "null", "String", "System", "out", "println", "print", "Scanner", "nextInt", "nextLine",
               "new", "File", "exists", "length", "length()", "charAt", "substring", "equals", "equalsIgnoreCase",
               "next", "hasNext", "hasNextLine", "hasNextInt", "hasNextDouble", "hasNextBoolean", "hasNextByte",
               "hasNextFloat", "hasNextLong", "hasNextShort", "hasNextBigDecimal", "hasNextBigInteger",
               "hasNextBigInteger", "hasNextBigDecimal", "hasNextBigInteger", "{", "}", "(", ")", "[", "]", ";", "=",
               ":", ",", "+", "-", "*", "%", "++", "--", "==", "!=", ">", "<", ">=", "<=", "&&", "||", "!", "&",
               "|", "^", "~", "<<", ">>", ">>>", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", ">>>=",
               "?", "Main", "main", "args", "array", "temp", "Exception", "printStackTrace", "getMessage", "abstrakt",
               "@override", "@Override", "Override", "toString", "equals", "hashCode", "clone", "compareTo", "finalize", "getClass",
               "IllegalArgumentException"}


def start_plagscan(gui: mainGUI):
    """Starts the PlagiatScanner, which compares all files in the students folder with each other"""
    selected_path = gui.zip_selection.cget("text")
    if selected_path == "":
        messagebox.showerror("Fehler", "Keine ZIP-Datei ausgewählt!")
        return
    elif selected_path.endswith(".zip"):
        gui.info_textline.config(text="ZIP-Datei wird entpackt...")
        selected_path = FileEditor.extract_zip(selected_path)
        gui.info_textline.config(text="ZIP-Datei entpackt")

    gui.progressbar.grid(row=4, column=1, sticky="ew")
    if gui.result_button is not None:
        gui.result_button.grid_forget()
    gui.root.update()

    gui.info_textline.config(text="Files werden entpackt...")
    try:
        students_folder = FileEditor.unpackZipFiles(selected_path, gui)
    except UnboundLocalError:
        gui.info_textline.config(text="")
        messagebox.showerror("Fehler", "ZIP-Dateien der Einzellabore nicht gefunden!")
        return
    gui.info_textline.config(text="Files entpackt")
    gui.info_textline.config(text="PlagiatScanner wird gestartet...")
    plagscan(students_folder, gui)
    gui.progressbar.grid_forget()
    gui.create_open_result_button(None)
    gui.info_textline.config(text="PlagiatScanner abgeschlossen")


def file_to_list(filepath: str) -> list:
    """Converts a file to a list of lines, each line is a list with the line number and the line itself"""
    with open(filepath, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for i, line in enumerate(lines):
        line_list = [i, line]
        new_lines.append(line_list)

    return new_lines


def replace_words_in_file(file_list: list, word_list: set) -> list:
    """Replaces all variables in a file with a placeholder and deletes all comments"""
    new_lines = []
    commentblock = False

    for line in file_list:
        new_line = line[:]
        if '/**' in new_line[1]:
            commentblock = True
            new_line[1] = ''
            new_lines.append(new_line)
            continue
        elif '*/' in new_line[1]:
            commentblock = False
            new_line[1] = ''
            new_lines.append(new_line)
            continue
        elif commentblock:
            new_line[1] = ''
            new_lines.append(new_line)
            continue
        else:
            if '//' in new_line[1]:
                new_line[1] = new_line[1].split('//')[0] + '\n'
            words = re.findall(r'\b\w+\b', new_line[1])
            for word in words:
                if word not in word_list:
                    new_line[1] = re.sub(r'\b' + re.escape(word) + r'\b', 'x', new_line[1])
            new_lines.append(new_line)

    return new_lines


def find_java_files(folder_path):
    """Returns a dictionary with all java files in the given folder and its subfolders"""
    java_files = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files[file] = os.path.join(root, file)
    return java_files


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


def filter_lines(file_as_list: list) -> list:
    """Filters all lines from a file that contain a string from the filter.txt file"""
    with open('filter.txt', 'r') as f:
        exclude_strings = ast.literal_eval(f.read())
    filtered_lines = []
    for line in file_as_list:
        if not any(exclude_string in line for exclude_string in exclude_strings):
            filtered_lines.append(line)
    return filtered_lines


def compare_files(file1_path: str, file2_path: str) -> list:
    """Compares two files and returns the lines of code that are the same in both files"""
    datei1_lines_orginal = file_to_list(file1_path)
    datei2_lines_orginal = file_to_list(file2_path)

    datei1_lines_prepared = replace_words_in_file(datei1_lines_orginal, java_syntax)
    datei2_lines_prepared = replace_words_in_file(datei2_lines_orginal, java_syntax)

    for line in datei1_lines_prepared:
        line[1] = line[1].strip()

    for line in datei2_lines_prepared:
        line[1] = line[1].strip()

    datei1_lines = filter_lines(datei1_lines_prepared)
    datei2_lines = filter_lines(datei2_lines_prepared)

    start_datei1 = 0
    start_datei2 = 0
    plag_list = []

    i = 0
    while i < len(datei1_lines):
        count = 0
        for j in range(len(datei2_lines)):
            if datei1_lines[i][1] == datei2_lines[j][1]:
                if count == 0:
                    start_datei1 = datei1_lines[i][0]
                    start_datei2 = datei2_lines[j][0]
                count += 1
                i += 1
                if i >= len(datei1_lines):
                    if count >= 5:
                        plag_list.append([start_datei1, datei1_lines[i-1][0], start_datei2, datei2_lines[j][0]])
                    break
            else:
                if count >= 5:
                    plag_list.append([start_datei1, datei1_lines[i][0], start_datei2, datei2_lines[j][0]])
                count = 0
        i += 1

    result_code_list = []
    for plagiat in plag_list:
        result_code_list.append([get_plagcode_from_filelist(datei1_lines, plagiat), plagiat[0], plagiat[1], plagiat[2], plagiat[3]])

    return result_code_list


def create_stats(plag_dict: dict) -> list:
    """Creates a list with the stats for the given dictionary\n
    [Plag_Count, Stud_Count, Stud_dict]"""
    # Zählen wie oft ein Student plagiiert hat
    stud_plag_count = {}
    for key, value in plag_dict.items():
        for element in value:
            if element[0] not in stud_plag_count:
                stud_plag_count[element[0]] = 0
            stud_plag_count[element[0]] += 1

    # zählen von allen Studenten Paaren
    stud_pair_dict = {}
    for key, value in plag_dict.items():
        students = []
        for element in value:
            students.append(element[0])
        students.sort()
        for i, student1 in enumerate(students):
            for student2 in students[i+1:]:
                stud_pair = student1 + " - " + student2
                if stud_pair not in stud_pair_dict:
                    stud_pair_dict[stud_pair] = 0
                stud_pair_dict[stud_pair] += 1

    # dict sorted by value
    stud_plag_count = {k: v for k, v in sorted(stud_plag_count.items(), key=lambda item: item[1], reverse=True)}
    stud_pair_dict = {k: v for k, v in sorted(stud_pair_dict.items(), key=lambda item: item[1], reverse=True)}

    return [len(plag_dict), len(stud_plag_count), stud_plag_count, stud_pair_dict]


def plagscan(students_folder: str, gui: mainGUI):
    """Scans all files in the given folder for plagiarism"""
    # 1. Festlegen der Struktur für das Vergleichsergebnis
    results = {}

    # 2. Sammeln aller Java-Dateien für jeden Studenten
    student_folders_list = os.listdir(students_folder)
    gui.set_progressbar_start(len(student_folders_list))
    gui.info_textline.config(text="Files werden gesammelt...")
    student_dict = {}

    for student_folder in student_folders_list:
        student_files_dict = find_java_files(os.path.join(students_folder, student_folder))
        if len(student_files_dict) == 0:
            print("Keine Java-Files gefunden für Student: " + student_folder)
        student_dict[student_folder] = student_files_dict
        gui.update_progressbar_value(1)

    # 3. Schleife für alle Kombinationen von Studenten
    plagiat_dict = {}
    gui.set_progressbar_start((math.pow(len(student_folders_list), 2) / 2))
    gui.info_textline.config(text="Files werden verglichen...")
    for i, student1 in enumerate(student_dict):
        for student2 in list(student_dict)[i + 1:]:
            for file1 in student_dict[student1]:
                if file1 in student_dict[student2]:
                    # plagiat = [[CODE, Stud1-ZeileStart, Stud1-ZeileEnde, Stud2-ZeileStart, Stud2-ZeileEnde], ...]
                    plagiat = compare_files(student_dict[student1][file1], student_dict[student2][file1])
                    for plagiat_code in plagiat:
                        if plagiat_code[0] not in plagiat_dict:
                            plagiat_dict[plagiat_code[0]] = []
                        # plagiat_dict[plagiat_code[0]].append([student1, file1, [plagiat_code[1], plagiat_code[2]]])
                        # plagiat_dict[plagiat_code[0]].append([student2, file1, [plagiat_code[3], plagiat_code[4]]])
                        plagiat_dict[plagiat_code[0]].append([student1, student_dict[student1][file1], [plagiat_code[1], plagiat_code[2]]])
                        plagiat_dict[plagiat_code[0]].append([student2, student_dict[student2][file1], [plagiat_code[3], plagiat_code[4]]])
                else:
                    for file2 in student_dict[student2]:
                        # plagiat = [[CODE, Stud1-ZeileStart, Stud1-ZeileEnde, Stud2-ZeileStart, Stud2-ZeileEnde], ...]
                        plagiat = compare_files(student_dict[student1][file1], student_dict[student2][file2])
                        for plagiat_code in plagiat:
                            if plagiat_code[0] not in plagiat_dict:
                                plagiat_dict[plagiat_code[0]] = []
                            # plagiat_dict[plagiat_code[0]].append([student1, file1, [plagiat_code[1], plagiat_code[2]]])
                            # plagiat_dict[plagiat_code[0]].append([student2, file2, [plagiat_code[3], plagiat_code[4]]])
                            plagiat_dict[plagiat_code[0]].append([student1, student_dict[student1][file1], [plagiat_code[1], plagiat_code[2]]])
                            plagiat_dict[plagiat_code[0]].append([student2, student_dict[student2][file2], [plagiat_code[3], plagiat_code[4]]])
            gui.update_progressbar_value(1)

    # 4. Ergebnisstruktur erstellen
    stats_list = create_stats(plagiat_dict)
    stats_text = "PlagScan abgeschlossen!\n\nAnzahl Plagiate: " + str(stats_list[0]) + \
                             "\nAnzahl Studenten mit Plagiat: " + str(stats_list[1]) + "\n\n" + str(stats_list[2])
    threading.Thread(target=mainGUI.display_msgbox, args=("PlagScan", stats_text)).start()

    # 5. Ergebnis speichern
    FileEditor.save_auswertung_to_file(plagiat_dict)
