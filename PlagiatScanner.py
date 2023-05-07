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


def replace_words_in_file(filepath, word_list):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines:
        if '//' in line:
            line = line.split('//')[0] + '\n'
        words = re.findall(r'\b\w+\b', line)
        for word in words:
            if word not in word_list:
                line = re.sub(r'\b' + re.escape(word) + r'\b', 'x', line)
        new_lines.append(line)
    new_text = ''.join(new_lines)

    return new_text


def find_java_files(folder_path):
    java_files = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files[file] = os.path.join(root, file)
    return java_files


def compare_files(file1_path: str, file2_path: str) -> float:
    datei1 = replace_words_in_file(file1_path, java_syntax)
    datei2 = replace_words_in_file(file2_path, java_syntax)

    lines1 = datei1.split('\n')
    lines2 = datei2.split('\n')
    lines1 = [line.rstrip() for line in lines1 if line.strip() != '']
    lines2 = [line.rstrip() for line in lines2 if line.strip() != '']

    for i in range(len(lines1)):
        count = 0
        for j in range(len(lines2)):
            if lines1[i] == lines2[j]:
                count += 1
                i += 1
                if count >= 5:
                    return True
                if i >= len(lines1):
                    break
            else:
                count = 0
    return False


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
    gui.set_progressbar_start(math.pow(len(student_folders_list), 2))
    gui.info_textline.config(text="Files werden verglichen...")
    for i, student1 in enumerate(student_dict):
        for student2 in list(student_dict)[i + 1:]:
            for file1 in student_dict[student1]:
                if file1 in student_dict[student2]:
                    plagiat = compare_files(student_dict[student1][file1], student_dict[student2][file1])
                    print(student1 + file1 + " " + student2 + file1 + " " + str(plagiat))
                else:
                    for file2 in student_dict[student2]:
                        plagiat = compare_files(student_dict[student1][file1], student_dict[student2][file2])
                        print(student1 + file1 + " " + student2 + file2 + " " + str(plagiat))
            gui.update_progressbar_value(1)

    # for student1 in student_dict:
    #     for student2 in student_dict:
    #         if student1 == student2:
    #             continue
    #         for file1 in student_dict[student1]:
    #             if file1 in student_dict[student2]:
    #                 plagiat = compare_files(student_dict[student1][file1], student_dict[student2][file1])
    #                 print(student1 + file1 + " " + student2 + file1 + " " + str(plagiat))
    #             else:
    #                 for file2 in student_dict[student2]:
    #                     plagiat = compare_files(student_dict[student1][file1], student_dict[student2][file2])
    #                     print(student1 + file1 + " " + student2 + file2 + " " + str(plagiat))
    #         gui.update_progressbar_value(1)


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
