import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pygame

import laborPlagScan.FileEditor as FileEditor
import laborPlagScan.PlagiatScanner as PlagiatScanner
import laborPlagScan.tableGui as tableGui


def on_enter(e):
    e.widget['background'] = '#1e79ff'


def on_leave(e):
    e.widget['background'] = '#1e90ff'


def display_msgbox(title, message):
    messagebox.showinfo(title, message)


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x350")
        self.root.title("PlagScan for Java-Labore")
        self.root.configure(bg='#0a3055')

        # Create placeholders for column 0 and 2
        tk.Label(self.root, text="", bg="#0a3055", width=28).grid(row=0, column=0)
        tk.Label(self.root, text="", bg="#0a3055", width=28).grid(row=0, column=2)

        zip_button = tk.Button(self.root, text="ZIP auswählen", command=self.select_zip)
        zip_button.grid(row=0, column=1, pady=10, sticky="ew")
        zip_button.config(width=20, height=2, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        zip_button.bind("<Enter>", on_enter)
        zip_button.bind("<Leave>", on_leave)

        self.zip_selection = tk.Label(self.root, text="", bg="#0a3055", fg="white", font=("Calibri", 12))
        self.zip_selection.grid(row=1, column=0, columnspan=3, sticky="ew")

        start_button = tk.Button(self.root, text="PlagScan starten",
                                 command=lambda: PlagiatScanner.start_plagscan(self))
        start_button.grid(row=2, column=1, pady=10, sticky="ew")
        start_button.config(width=20, height=2, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)

        self.info_textline = tk.Label(self.root, text="", bg="#0a3055", fg="white", font=("Calibri", 12))
        self.info_textline.grid(row=3, column=0, columnspan=3, sticky="ew")

        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")

        self.result_button = None
        last_save = FileEditor.get_last_modified_file()
        if last_save is not None:
            self.create_open_result_button(last_save)

        self.result_from_button = tk.Button(self.root, text="🔽", command=lambda: self.open_table_gui())
        self.result_from_button.grid(row=5, column=2, pady=10, sticky="w")
        self.result_from_button.config(width=2, height=2, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        self.result_from_button.bind("<Enter>", on_enter)
        self.result_from_button.bind("<Leave>", on_leave)

        self.name_textline = tk.Button(self.root, text="© 2023 by Erik Ilgenstein", bg="#0a3055", fg="grey",
                                       font=("Calibri", 10), border=0, command=self.hidden_button_click,
                                       activebackground="#0a3055", activeforeground="grey", takefocus=0)
        self.name_textline.place(relx=1.0, rely=1.0, anchor="se")
        # easteregg
        self.clicks = 0
        self.music_playing = False
        pygame.mixer.init()

    def hidden_button_click(self):
        # Zähle Klicks
        self.clicks += 1

        # Wenn 5 Klicks erreicht sind, starte Musik
        if self.clicks >= 5:
            # toggle Music
            if not self.music_playing:
                music_path = os.path.join(os.getcwd(), 'laborPlagScan', 'resources', 'UniversalAdobePatcherMusic.mp3')
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play()
                self.music_playing = True
            else:
                pygame.mixer.music.pause()
                self.music_playing = False

    def create_open_result_button(self, filename: str):
        if filename is None:
            filename = FileEditor.get_last_modified_file()
        self.result_button = tk.Button(self.root, text=f"Open {filename}", command=lambda: self.open_table_gui(filename))
        self.result_button.grid(row=5, column=1, pady=10, sticky="ew")
        self.result_button.config(width=20, height=2, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        self.result_button.bind("<Enter>", on_enter)
        self.result_button.bind("<Leave>", on_leave)

    def open_table_gui(self, filename=None):
        self.root.destroy()
        table = tableGui.TableGui(FileEditor.load_auswertung_from_file(filename))

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

    def remove_progressbar(self):
        self.progressbar.style = 'none'

    def select_zip(self):
        filepath = filedialog.askopenfilename(title="ZIP auswählen")
        if filepath:
            self.zip_selection.config(text=filepath)
