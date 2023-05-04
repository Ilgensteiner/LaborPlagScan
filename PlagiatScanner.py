import os
from tkinter import messagebox
import math

import FileEditor
import GUI


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
    gui.info_textline.config(text="PlagiatScanner beendet")


def plagscan(students_folder: str, gui: GUI) -> list:
    # 1. Festlegen der Struktur für das Vergleichsergebnis
    results = []

    # 2. Sammeln aller Java-Dateien für jeden Studenten
    student_folders = os.listdir(students_folder)
    gui.set_progressbar_start(math.pow(len(student_folders), 2))

    for student_folder in student_folders:
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
