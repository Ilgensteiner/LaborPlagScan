import tkinter as tk
from tkinter import *
from tkinter import ttk

import FileEditor


class TableGui:
    def __init__(self, data):
        items = []
        self.items_plagiat = []
        self.items_unsicher = []
        self.items_kein_plagiat = []
        for i, item in enumerate(data.items()):
            items.append([i, item])

        self.root = tk.Tk()
        self.root.geometry("600x350")
        self.root.title("PlagScan for Java-Labore")
        self.root.configure(bg='#0a3055')

        # Tabelle erstellen
        vergl_table = ttk.Frame(self.root)
        vergl_table.grid(row=0, column=0, sticky="nsew")

        # Canvas erstellen
        canvas = tk.Canvas(vergl_table)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        yscrollbar = ttk.Scrollbar(vergl_table, orient="vertical", command=canvas.yview)
        yscrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar = ttk.Scrollbar(vergl_table, orient="horizontal", command=canvas.xview)
        xscrollbar.grid(row=1, column=0, sticky="ew")

        # Canvas-Scrollbars-Konfiguration
        canvas.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        inner_frame = ttk.Frame(canvas)
        inner_frame.grid(sticky="nsew")

        def update_inner_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        canvas.bind("<Configure>", update_inner_frame)

        # Create Style Table.Tlabel
        style = ttk.Style()
        style.configure("Table.TLabel", background="white", foreground="black",
                        font=("Calibri", 12), borderwidth=2, relief="solid", width=50)
        style.configure("TableHead.TLabel", background="white", foreground="black",
                        font=("Calibri", 12, "bold"), borderwidth=2, relief="solid", width=10)

        for plagiat in items:
            column = 1
            print(plagiat[1][1])
            # Spalten
            ttk.Label(inner_frame, text="Name", style="TableHead.TLabel").grid(row=0, column=0)
            ttk.Label(inner_frame, text="Datei", style="TableHead.TLabel").grid(row=1, column=0)
            ttk.Label(inner_frame, text="Code", style="TableHead.TLabel").grid(row=2, column=0)
            for student_infos in plagiat[1][1]:
                ttk.Label(inner_frame, text=student_infos[0], style="Table.TLabel").grid(row=0, column=column)
                ttk.Label(inner_frame, text=student_infos[1], style="Table.TLabel").grid(row=1, column=column)
                ttk.Label(inner_frame, text=str(student_infos[2]) + "\nfasd\n\nfasd\n\nfasd\n\nfasd\n\nfasd\n\nfasd\n\nfasd\n\nfasd\n\nfasd\n\nfasd\n\tdasd", style="Table.TLabel").grid(row=2, column=column)
                column += 1

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        vergl_table.columnconfigure(0, weight=1)
        vergl_table.rowconfigure(0, weight=1)
        inner_frame.columnconfigure(list(range(column)), weight=1)

        self.create_button_panel()

        self.root.mainloop()

    def create_button_panel(self):
        # Button-Panel erstellen
        button_panel = ttk.Frame(self.root)
        button_panel.grid(row=1, column=0, sticky="ew")
        button_panel.columnconfigure(0, weight=0)
        button_panel.columnconfigure(1, weight=0)
        button_panel.columnconfigure(2, weight=0)
        button_panel.columnconfigure(3, weight=1)
        button_panel.columnconfigure(4, weight=0)

        # Buttons erstellen
        btn_plagiat = ttk.Button(button_panel, text="Plagiat", command=self.on_plagiat_button_click)
        btn_unsicher = ttk.Button(button_panel, text="Unsicher", command=self.on_unsicher_button_click)
        btn_ok = ttk.Button(button_panel, text="OK", command=self.on_ok_button_click)
        btn_speichern = ttk.Button(button_panel, text="Speichern", command=self.on_speichern_button_click)
        btn_exportieren = ttk.Button(button_panel, text="Exportieren", command=self.on_exportieren_button_click)

        # Buttons positionieren
        btn_plagiat.grid(row=0, column=0, sticky="w")
        btn_unsicher.grid(row=0, column=1, sticky="w")
        btn_ok.grid(row=0, column=2, sticky="w")
        btn_speichern.grid(row=0, column=3, sticky="e")
        btn_exportieren.grid(row=0, column=4, sticky="e")

    def on_plagiat_button_click(self):
        # Aktion für den Plagiat-Button
        pass

    def on_unsicher_button_click(self):
        # Aktion für den Unsicher-Button
        pass

    def on_ok_button_click(self):
        # Aktion für den OK-Button
        pass

    def on_speichern_button_click(self):
        # Aktion für den Speichern-Button
        pass

    def on_exportieren_button_click(self):
        # Aktion für den Exportieren-Button
        pass


table = TableGui(FileEditor.load_auswertung_from_file("last_result"))
