import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage
from PIL import Image, ImageTk
import pygame

import PlagiatScanner


def on_enter(e):
    e.widget['background'] = '#1e79ff'


def on_leave(e):
    e.widget['background'] = '#1e90ff'


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x300")
        self.root.title("PlagScan for Java-Labore")
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

        self.name_textline = tk.Button(self.root, text="© 2023 by Erik Ilgenstein", bg="#0a3055", fg="grey",
                                       font=("Calibri", 10), border=0, command=self.hidden_button_click,
                                       activebackground="#0a3055", activeforeground="grey", takefocus=0)
        self.name_textline.place(relx=1.0, rely=1.0, anchor="se")
        # easteregg
        self.clicks = 0
        self.music_playing = False
        pygame.mixer.init()

        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")

    def hidden_button_click(self):
        # Zähle Klicks
        self.clicks += 1

        # Wenn 5 Klicks erreicht sind, starte Musik
        if self.clicks >= 5:
            # toggle Music
            if not self.music_playing:
                pygame.mixer.music.load('resources/UniversalAdobePatcherMusic.mp3')
                pygame.mixer.music.play()
                self.music_playing = True
            else:
                pygame.mixer.music.pause()
                self.music_playing = False

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

