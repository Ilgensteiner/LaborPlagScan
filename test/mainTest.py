import FileEditor
import tkinter as tk
from GUI import GUI
from PlagiatScanner import plagscan


def start_plagscanTest(gui: GUI):
    selected_path = "C:\\Users\\eriki\\Downloads\\Test-Labor.zip"
    if selected_path == "":
        return
    elif selected_path.endswith(".zip"):
        selected_path = FileEditor.extract_zip(selected_path)

    try:
        students_folder = FileEditor.unpackZipFiles(selected_path, gui)
    except UnboundLocalError:
        return
    plagscan(students_folder, gui)


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)

    start_plagscanTest(gui)
