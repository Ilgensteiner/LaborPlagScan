import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pygame

import laborPlagScan.fileEditor as FileEditor
import laborPlagScan.plagiatScanner as PlagiatScanner
import laborPlagScan.Gui.settingGui as settingsGui
from laborPlagScan.Gui.auswertung import AuswertungGui


def on_enter(e):
    e.widget['background'] = '#1e79ff'


def on_leave(e):
    e.widget['background'] = '#1e90ff'


def display_msgbox(title, message):
    messagebox.showinfo(title, message)


class GUI:
    progressbar: ttk.Progressbar = None
    info_textline: tk.Label = None
    root: tk.Tk = None

    @staticmethod
    def set_progressbar_start(value: int):
        GUI.progressbar['maximum'] = value
        GUI.progressbar['value'] = 0
        GUI.progressbar.grid(row=5, column=1, pady=10, sticky="ew")
        GUI.root.update()

    @staticmethod
    def set_progressbar_value(value: int):
        GUI.progressbar['value'] = value
        GUI.root.update_idletasks()

    @staticmethod
    def update_progressbar_value(value: int):
        GUI.progressbar['value'] += value
        GUI.root.update_idletasks()

    @staticmethod
    def remove_progressbar():
        GUI.progressbar.grid_remove()
        GUI.root.update_idletasks()

    @staticmethod
    def set_info_text(text: str):
        GUI.info_textline.config(text=text)
        GUI.root.update_idletasks()
        
    @staticmethod
    def update_root():
        GUI.root.update()
        
    def __init__(self, root):
        GUI.root = root
        GUI.root.geometry("600x400")
        GUI.root.title("PlagScan for Java-Labore")
        GUI.root.configure(bg='#0a3055')

        # Create placeholders for column 0 and 2
        tk.Label(GUI.root, text="", bg="#0a3055", width=28).grid(row=0, column=0)
        tk.Label(GUI.root, text="", bg="#0a3055", width=28).grid(row=0, column=2)

        zip_button = tk.Button(GUI.root, text="ZIP auswählen", command=self.select_zip)
        zip_button.grid(row=0, column=1, pady=10, sticky="ew")
        zip_button.config(width=20, height=2, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        zip_button.bind("<Enter>", on_enter)
        zip_button.bind("<Leave>", on_leave)
        self.zipPfad = ""

        self.zip_selection = tk.Label(GUI.root, text="", bg="#0a3055", fg="white", font=("Calibri", 12))
        self.zip_selection.grid(row=1, column=0, columnspan=3, sticky="ew")

        settings_button = tk.Button(GUI.root, text="Einstellungen⚙️", command=self.open_settings)
        settings_button.grid(row=2, column=1, pady=10, sticky="ew")
        settings_button.config(bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        settings_button.bind("<Enter>", on_enter)
        settings_button.bind("<Leave>", on_leave)

        start_button = tk.Button(GUI.root, text="PlagScan starten",
                                 command=lambda: PlagiatScanner.start_plagscan(self.zipPfad, self))
        start_button.grid(row=3, column=1, pady=10, sticky="ew")
        start_button.config(width=20, height=2, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)

        GUI.info_textline = tk.Label(GUI.root, text="", bg="#0a3055", fg="white", font=("Calibri", 12))
        GUI.info_textline.grid(row=4, column=0, columnspan=3, sticky="ew")

        GUI.progressbar = ttk.Progressbar(GUI.root, orient="horizontal", length=200, mode="determinate")

        self.result_button = None
        last_save = FileEditor.get_last_modified_file()
        if last_save is not None:
            self.create_open_result_button(last_save)
        else:
            self.create_open_result_button(None)

        self.result_from_button = tk.Button(GUI.root, text="🔽", command=lambda: self.open_table_gui())
        self.result_from_button.grid(row=6, column=2, pady=10, sticky="w")
        self.result_from_button.config(width=2, height=2, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        self.result_from_button.bind("<Enter>", on_enter)
        self.result_from_button.bind("<Leave>", on_leave)

        self.name_textline = tk.Button(GUI.root, text="© 2023 by Erik Ilgenstein", bg="#0a3055", fg="grey",
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
            if filename is None:
                self.result_button = tk.Button(GUI.root, text=f"Open Save", command=lambda: self.open_table_gui())
            else:
                self.result_button = tk.Button(GUI.root, text=f"Open {filename}", command=lambda: self.open_table_gui(filename))
        else:
            self.result_button = tk.Button(GUI.root, text=f"Open {filename}", command=lambda: self.open_table_gui(filename))

        self.result_button.grid(row=6, column=1, pady=10, sticky="ew")
        self.result_button.config(width=20, height=2, bg="#1e90ff", fg="white", font=("Calibri", 14, "bold"))
        self.result_button.bind("<Enter>", on_enter)
        self.result_button.bind("<Leave>", on_leave)

    def open_table_gui(self, filename=None):
        try:
            auswertung = FileEditor.load_auswertung_from_file(filename)
            GUI.root.destroy()
            table = AuswertungGui(auswertung)
        except FileNotFoundError:
            print("File not found")

    def open_settings(self):
        settings = settingsGui.SettingsGUI()

    def select_zip(self):
        filepath = filedialog.askopenfilename(title="ZIP auswählen")
        if filepath:
            self.zipPfad = filepath

            if len(filepath) > 50:
                filepath = "..." + filepath[-50:]
            self.zip_selection.config(text=filepath)
