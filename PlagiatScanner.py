import os


def plagscan(students_folder: str) -> list:
    # 1. Festlegen der Struktur für das Vergleichsergebnis
    results = []

    # 2. Sammeln aller Java-Dateien für jeden Studenten
    student_folders = os.listdir(students_folder)
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

    # 6. Zurückgabe der Ergebnisse
    return results
