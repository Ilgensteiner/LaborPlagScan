import os
import zipfile

import GUI


def extract_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        folder_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_path = os.path.join(os.path.dirname(zip_path), folder_name)
        zip_file.extractall(path=extract_path)
    return extract_path


def unpackZipFiles(folder_path: str, gui: GUI):
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
