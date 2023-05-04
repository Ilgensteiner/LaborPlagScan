import tkinter as tk
from tkinter import filedialog, ttk

import PlagiatScanner


def on_enter(e):
    e.widget['background'] = '#1e79ff'


def on_leave(e):
    e.widget['background'] = '#1e90ff'


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x400")
        self.root.title("PlagScan GUI")
        self.root.configure(bg='#0a3055')

        zip_button = tk.Button(self.root, text="ZIP auswählen", command=self.select_zip)
        zip_button.pack(pady=10)
        zip_button.config(width=20, height=3, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        zip_button.bind("<Enter>", on_enter)
        zip_button.bind("<Leave>", on_leave)

        self.zip_selection = tk.Label(self.root, text="")
        self.zip_selection.pack()

        start_button = tk.Button(self.root, text="PlagScan starten", command=lambda: PlagiatScanner.start_plagscan(self))
        start_button.pack(pady=10)
        start_button.config(width=20, height=3, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)

        self.info_textline = tk.Label(self.root, text="")
        self.info_textline.pack()

        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")

    def set_progressbar_start(self, value: int):
        self.progressbar['maximum'] = value
        self.progressbar['value'] = 0
        self.root.update_idletasks()

    def set_progressbar_value(self, value: int):
        self.progressbar['value'] = value
        self.root.update_idletasks()

    def update_progressbar_value(self, value: int):
        self.progressbar['value'] += value
        self.root.update_idletasks()

    def select_zip(self):
        filepath = filedialog.askopenfilename(title="ZIP auswählen")
        if filepath:
            self.zip_selection.config(text=filepath)

