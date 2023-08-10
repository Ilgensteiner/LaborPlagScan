import tkinter as tk
from laborPlagScan.mainGUI import GUI


def run() -> None:
    root = tk.Tk()
    gui = GUI(root)

    root.mainloop()
