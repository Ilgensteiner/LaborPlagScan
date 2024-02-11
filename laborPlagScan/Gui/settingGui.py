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

        self.label = ttk.Label(self.master, font=("Calibri", 12), text="""   - Variablennamen werden allgemein mit x bezeichnet.
    - Spezifische Codezeilen wie this.x = x;.
    - Reguläre Ausdrücke (beginnend mit 'Regex:'), die Muster innerhalb des Codes erkennen.
    - Dateinamen, die direkt angegeben werden können, wie vorlage.java, um bestimmte Dateien von der Überprüfung auszuschließen.""")
        self.label.pack(pady=10, fill=tk.X)

        # Container für Canvas und Scrollbar
        container = ttk.Frame(self.master)
        container.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        self.canvas = tk.Canvas(container)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Binden des Scroll-Events an das Canvas-Widget für das Mausrad
        self.master.bind_all('<MouseWheel>', self.on_mousewheel)  # für Windows
        self.master.bind_all('<Button-4>', self.on_mousewheel)  # für Linux & MacOS
        self.master.bind_all('<Button-5>', self.on_mousewheel)  # für Linux & MacOS

        self.filters = read_filters_from_file()
        self.entries = []

        for filter in self.filters:
            self.add_filter_row(filter)

        # Frame für die Buttons unter dem Canvas
        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        self.add_button = ttk.Button(button_frame, text="Filter hinzufügen", command=self.add_filter_row)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.save_button = ttk.Button(button_frame, text="Speichern", command=self.save)
        self.save_button.pack(side=tk.RIGHT, padx=10)

    def add_filter_row(self, filter=""):
        row = ttk.Frame(self.scrollable_frame)
        row.pack(fill=tk.X, pady=5)

        entry = ttk.Entry(row)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        entry.insert(0, filter)

        delete_button = ttk.Button(row, text="Löschen", command=lambda: self.delete_row(row, entry))
        delete_button.pack(side=tk.RIGHT)

        self.entries.append((row, entry))

    def delete_row(self, row, entry):
        row.destroy()
        self.entries.remove((row, entry))
        # Update das scrollable region des Canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save(self):
        updated_filters = [entry.get() for _, entry in self.entries]
        save_filters_to_file(updated_filters)
        self.master.destroy()

    def reset(self):
        filters = ['', 'this.x = x;', 'Regex:(protected|private|public)\s(static\s)?(String|double|float|boolean|int)\s(x;)', 'Regex:(public)\s(String|double|float|boolean|int)\s(x\(\) {)', 'Regex:(return)\s(x;)', 'Regex:(public\svoid\sx\()(String|double|float|boolean|int)\s(x\) {)', 'Regex:(this\.x\s=\sx;)', 'Regex:(\})']
        save_filters_to_file(filters)
        SettingsGUI()

    def adjust_wraplenght(self, event):
        self.label.config(wraplength=event.winfo_width() - 20)

    def on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:  # Scrollen nach oben
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scrollen nach unten
            self.canvas.yview_scroll(1, "units")
