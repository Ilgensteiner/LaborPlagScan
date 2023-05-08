import os
from tkinter import messagebox
import math
import re

import FileEditor
import GUI


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


def start_plagscan(gui: GUI):
    selected_path = gui.zip_selection.cget("text")
    if selected_path == "":
        messagebox.showerror("Fehler", "Keine ZIP-Datei ausgewählt!")
        return
    elif selected_path.endswith(".zip"):
        gui.info_textline.config(text="ZIP-Datei wird entpackt...")
        selected_path = FileEditor.extract_zip(selected_path)
        gui.info_textline.config(text="ZIP-Datei entpackt")

    gui.progressbar.pack()

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
    gui.progressbar.pack_forget()
    gui.info_textline.config(text="PlagiatScanner abgeschlossen")


def file_to_list(filepath: str) -> list:
    with open(filepath, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for i, line in enumerate(lines):
        line_list = [i, line]
        new_lines.append(line_list)

    return new_lines


def replace_words_in_file(file_list: list, word_list: list) -> list:
    new_lines = []
    for line in file_list:
        if '//' in line[1]:
            line[1] = line[1].split('//')[0] + '\n'
        words = re.findall(r'\b\w+\b', line[1])
        for word in words:
            if word not in word_list:
                line[1] = re.sub(r'\b' + re.escape(word) + r'\b', 'x', line[1])
        line_list = [line[0], line[1]]
        new_lines.append(line_list)

    return new_lines


def find_java_files(folder_path):
    java_files = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files[file] = os.path.join(root, file)
    return java_files


def get_plagcode_from_file(org_file_as_list: list, plag_result: list) -> str:
    plag_code = ""
    for i in range(plag_result[0], plag_result[1] + 1):
        plag_code += org_file_as_list[i][1]
    return plag_code


def compare_files(file1_path: str, file2_path: str) -> float:
    datei1_lines_orginal = file_to_list(file1_path)
    datei2_lines_orginal = file_to_list(file2_path)

    datei1_lines = replace_words_in_file(datei1_lines_orginal, java_syntax)
    datei2_lines = replace_words_in_file(datei2_lines_orginal, java_syntax)

    datei1_lines = [line for line in datei1_lines if line[1] != '\n']
    datei2_lines = [line for line in datei2_lines if line[1] != '\n']

    for line in datei1_lines:
        line[1] = line[1].strip()

    for line in datei2_lines:
        line[1] = line[1].strip()

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
        result_code_list.append(get_plagcode_from_file(datei1_lines_orginal, plagiat))

    return result_code_list


def plagscan(students_folder: str, gui: GUI) -> list:
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
                    plagiat = compare_files(student_dict[student1][file1], student_dict[student2][file1])
                    for plagiat_code in plagiat:
                        if plagiat_code not in plagiat_dict:
                            plagiat_dict[plagiat_code] = []
                        plagiat_dict[plagiat_code].append([student1, file1])
                        plagiat_dict[plagiat_code].append([student2, file1])
                else:
                    for file2 in student_dict[student2]:
                        plagiat = compare_files(student_dict[student1][file1], student_dict[student2][file2])
                        for plagiat_code in plagiat:
                            if plagiat_code not in plagiat_dict:
                                plagiat_dict[plagiat_code] = []
                            plagiat_dict[plagiat_code].append([student1, file1])
                            plagiat_dict[plagiat_code].append([student2, file2])
            gui.update_progressbar_value(1)

    # 4. Ergebnisstruktur erstellen
    stud_plag_count = {}
    for key, value in plagiat_dict.items():
        for element in value:
            if element[0] not in stud_plag_count:
                stud_plag_count[element[0]] = 0
            stud_plag_count[element[0]] += 1

    # 5. Ergebnis speichern
    save_path = os.path.join(students_folder.rsplit(os.sep, 3)[0], "plagiat_result.txt")
    with open(save_path, "w") as f:
        f.write("Anzahl Plagiate:" + str(len(plagiat_dict)) + "\n")
        f.write(str(plagiat_dict) + "\n")
        f.write("Anzahl Studenten mit Plagiat:" + str(len(stud_plag_count)) + "\n")
        f.write(str(stud_plag_count) + "\n")


def plagscanAlt(students_folder: str, gui: GUI) -> list:
    # 1. Festlegen der Struktur für das Vergleichsergebnis
    results = []

    # 2. Sammeln aller Java-Dateien für jeden Studenten
    student_folders = os.listdir(students_folder)
    gui.set_progressbar_start(math.pow(len(student_folders), 2))

    for student_folder in student_folders:
        # TODO: Funktion find Java-Files, Problem: Java-Files können in Unterordnern sein (Rekursion),
        #  wenn keine Java-Files gefunden werden, dann Fehlermeldung mit Studentenname
        java_files = [f for f in os.listdir(os.path.join(students_folder, student_folder)) if f.endswith('.java')]
        student_files = [(student_folder, f) for f in java_files]

        # 3. Schleife für alle Kombinationen von Studenten
        for other_student_folder in student_folders:
            if other_student_folder == student_folder:
                continue

            other_java_files = [f for f in os.listdir(os.path.join(students_folder, other_student_folder)) if
                                f.endswith('.java')]
            other_student_files = [(other_student_folder, f) for f in other_java_files]

            for student_file in student_files:
                for other_student_file in other_student_files:
                    # 4. Vergleich von Java-Dateien
                    if student_file[1] == other_student_file[1]:
                        continue

                    student_file_path = os.path.join(students_folder, student_file[0], student_file[1])
                    other_student_file_path = os.path.join(students_folder, other_student_file[0],
                                                           other_student_file[1])

                    with open(student_file_path) as f1, open(other_student_file_path) as f2:
                        student_lines = f1.readlines()
                        other_student_lines = f2.readlines()

                        for i, student_line in enumerate(student_lines):
                            if i >= len(other_student_lines):
                                break

                            other_student_line = other_student_lines[i]

                            # Vergleich der Zeilen
                            if student_line.strip() != other_student_line.strip():
                                continue

                            # 5. Speicherung von Plagiatsinformationen
                            result = {
                                'students': [student_file[0], other_student_file[0]],
                                'files': [student_file[1], other_student_file[1]],
                                'line': i + 1
                            }
                            results.append(result)
                gui.update_progressbar_value(1)

    # 6. Zurückgabe der Ergebnisse
    return results
