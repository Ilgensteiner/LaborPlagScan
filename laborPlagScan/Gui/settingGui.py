import ast
import tkinter as tk
from tkinter import ttk


def read_filters_from_file():
    with open('./filter.txt', 'r') as f:
        filter_list = ast.literal_eval(f.read())
    return filter_list


def save_filters_to_file(filters):
    with open('./filter.txt', 'w') as f:
        f.write(repr(filters))


class SettingsGUI:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Einstellungen")
        self.master.geometry("600x350")

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        # Main Frame
        main_frame = ttk.Frame(self.master)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Canvas
        self.canvas = tk.Canvas(main_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.configure(borderwidth=0)
        self.canvas.bind("<Configure>", self.adjust_wraplenght)

        self.filter_frame = ttk.Frame(self.canvas)
        self.filter_frame.grid(row=0, column=0, sticky="nsew")
        self.filter_frame.columnconfigure(0, weight=1)
        self.filter_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.filter_frame, anchor="nw")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.filter_row = 0
        self.label = ttk.Label(self.filter_frame, font=("Calibri", 12), text="""   - Variablennamen werden allgemein mit x bezeichnen. Bsp: (this.x = x;.)
    - Reguläre Ausdrücke (beginnend mit 'Regex:'), die Muster innerhalb des Codes erkennen.
    - Dateinamen (beginnend mit 'File:') um bestimmte Dateien von der Überprüfung auszuschließen.""")
        self.label.grid(row=self.filter_row, column=0, sticky="ew")
        self.filter_row += 1
        ttk.Separator(self.filter_frame, orient="horizontal").grid(row=self.filter_row, column=0, sticky="ew")

        # Binden des Scroll-Events an das Canvas-Widget für das Mausrad
        self.master.bind_all('<MouseWheel>', self.on_mousewheel)  # für Windows
        self.master.bind_all('<Button-4>', self.on_mousewheel)  # für Linux & MacOS
        self.master.bind_all('<Button-5>', self.on_mousewheel)  # für Linux & MacOS

        self.filters = read_filters_from_file()
        self.entries = []
        self.settingsVars = {}

        self.filter_row += 1
        for plag_filter in self.filters:
            if isinstance(plag_filter, dict):
                for key, value in plag_filter.items():
                    self.add_filter_settings(key, value)
            elif plag_filter == '':
                ttk.Separator(self.filter_frame, orient="horizontal").grid(row=self.filter_row, column=0, sticky="ew")
                self.filter_row += 1
            else:
                self.add_filter_row(plag_filter)

        self.add_button = ttk.Button(self.filter_frame, text="Filter hinzufügen", command=self.add_filter_row)
        self.add_button.grid(row=100, column=0, padx=10)

        # Frame für die Buttons unter dem Canvas
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=1, column=0, sticky="ew")

        self.reset_button = ttk.Button(button_frame, text="Filter zurücksetzen", command=self.reset)
        self.reset_button.grid(row=0, column=0, padx=10, sticky="e")

        self.save_button = ttk.Button(button_frame, text="Speichern", command=self.save)
        self.save_button.grid(row=0, column=2, padx=10, sticky="w")

    def add_filter_row(self, plag_filter=""):
        row = ttk.Frame(self.filter_frame)
        row.grid(row=self.filter_row, column=0, sticky="ew")
        self.filter_row += 1

        entry = ttk.Entry(row)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        entry.insert(0, plag_filter)

        delete_button = ttk.Button(row, text="Löschen", command=lambda: self.delete_row(row, entry))
        delete_button.pack(side=tk.RIGHT)

        self.entries.append((row, entry))

    def add_filter_settings(self, name, value):
        row = ttk.Frame(self.filter_frame)
        row.grid(row=self.filter_row, column=0, sticky="ew")
        self.filter_row += 1

        if name == "ignorePrintStatemants":
            checkbox = ttk.Checkbutton(row, text="Print-Statements ignorieren", variable="var", onvalue=True, offvalue=False)
            checkbox.pack(side=tk.LEFT, padx=(0, 5))
            checkbox.setvar("var", value)
            self.settingsVars["ignorePrintStatemants"] = checkbox
        elif name == "PlagiatAlert":
            ttk.Label(row, text="Plagiate speichern ab %:").pack(side=tk.LEFT, padx=(0, 5))
            entry = ttk.Entry(row)
            entry.pack(padx=(0, 5))
            entry.insert(0, value)
            self.settingsVars["PlagiatAlert"] = entry

    def delete_row(self, row, entry):
        row.destroy()
        self.entries.remove((row, entry))
        # Update das scrollable region des Canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save(self):
        settings_dict = {"ignorePrintStatemants": self.settingsVars["ignorePrintStatemants"].getvar("var"), "PlagiatAlert": self.settingsVars["PlagiatAlert"].get()}
        updated_filters = [entry.get() for _, entry in self.entries]
        updated_filters.insert(0, settings_dict)
        save_filters_to_file(updated_filters)
        self.master.destroy()

    def reset(self):
        filters = [{"ignorePrintStatemants": True, "PlagiatAlert": 30}, '', 'this.x = x;', 'Regex:(protected|private|public)\s(static\s)?(String|double|float|boolean|int)\s(x;)', 'Regex:(public)\s(String|double|float|boolean|int)\s(x\(\) {)', 'Regex:(return)\s(x;)', 'Regex:(public\svoid\sx\()(String|double|float|boolean|int)\s(x\) {)', 'Regex:(this\.x\s=\sx;)', 'Regex:(\})']
        save_filters_to_file(filters)
        self.master.destroy()

    def adjust_wraplenght(self, event):
        self.label.config(wraplength=self.master.winfo_width() - 20)

    def on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:  # Scrollen nach oben
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scrollen nach unten
            self.canvas.yview_scroll(1, "units")
