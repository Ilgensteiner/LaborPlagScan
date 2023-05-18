import os.path
import tkinter as tk
from tkinter import ttk

import FileEditor


class TableGui:
    def __init__(self, data):
        self.data = data
        print(self.data)
        self.items = []
        self.items_plagiat = []
        self.items_unsicher = []
        self.items_kein_plagiat = []
        for i, item in enumerate(data.items()):
            self.items.append([i, item])

        self.current_item_index = 0  # Aktueller Index im Datensatz

        self.root = tk.Tk()
        self.root.geometry("600x350")
        self.root.title("PlagScan for Java-Labore")
        self.root.configure(bg='#0a3055')

        self.create_table()
        self.create_button_panel()

        self.root.mainloop()

    def create_table(self):
        # Tabelle erstellen
        self.vergl_table = ttk.Frame(self.root)
        self.vergl_table.grid(row=0, column=0, sticky="nsew")

        # Canvas erstellen
        canvas = tk.Canvas(self.vergl_table)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        yscrollbar = ttk.Scrollbar(self.vergl_table, orient="vertical", command=canvas.yview)
        yscrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar = ttk.Scrollbar(self.vergl_table, orient="horizontal", command=canvas.xview)
        xscrollbar.grid(row=1, column=0, sticky="ew")

        # Canvas-Scrollbars-Konfiguration
        canvas.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        self.inner_frame = ttk.Frame(canvas)
        self.inner_frame.grid(sticky="nsew")

        def update_inner_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        canvas.bind("<Configure>", update_inner_frame)

        # Create Style Table.Tlabel
        style = ttk.Style()
        style.configure("Table.TLabel", background="white", foreground="black",
                        font=("Calibri", 12), borderwidth=2, relief="solid", minwidth=40, padding=5, anchor=tk.NW)
        style.configure("TableHead.TLabel", background="white", foreground="black",
                        font=("Calibri", 12, "bold"), borderwidth=2, relief="solid", minwidth=40, padding=5, anchor=tk.NW)

        self.display_plagiat()

    def display_plagiat(self):
        # Anzeige des Plagiats
        if self.current_item_index < len(self.items):
            plagiat = self.items[self.current_item_index]
            # Anzeige des Plagiats
            column = 1
            print(plagiat[1][1])
            # Spalten
            ttk.Label(self.inner_frame, text="Name", style="TableHead.TLabel").grid(row=0, column=0, sticky="nsew")
            ttk.Label(self.inner_frame, text="Datei", style="TableHead.TLabel").grid(row=1, column=0, sticky="nsew")
            ttk.Label(self.inner_frame, text="Code", style="TableHead.TLabel").grid(row=2, column=0, sticky="nsew")
            for student_infos in plagiat[1][1]:
                ttk.Label(self.inner_frame, text=student_infos[0], style="Table.TLabel").grid(row=0, column=column, sticky="nsew")
                ttk.Label(self.inner_frame, text=os.path.basename(student_infos[1]), style="Table.TLabel").grid(row=1, column=column, sticky="nsew")
                ttk.Label(self.inner_frame, text=str(FileEditor.read_file(student_infos[1], lines=student_infos[2])), style="Table.TLabel").grid(row=2, column=column, sticky="nsew")
                column += 1

            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            self.vergl_table.columnconfigure(0, weight=1)
            self.vergl_table.rowconfigure(0, weight=1)
            self.inner_frame.columnconfigure(list(range(column)), weight=1)
        else:
            self.create_auswertung()
            print(f"{self.items_plagiat}")
            print(self.data)
        self.root.update()

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
        self.btn_plagiat = ttk.Button(button_panel, text="Plagiat", command=self.on_plagiat_button_click)
        self.btn_unsicher = ttk.Button(button_panel, text="Unsicher", command=self.on_unsicher_button_click)
        self.btn_ok = ttk.Button(button_panel, text="OK", command=self.on_ok_button_click)
        self.btn_speichern = ttk.Button(button_panel, text="Speichern", command=self.on_speichern_button_click)
        self.btn_exportieren = ttk.Button(button_panel, text="Exportieren", command=self.on_exportieren_button_click)

        # Buttons positionieren
        self.btn_plagiat.grid(row=0, column=0, sticky="w")
        self.btn_unsicher.grid(row=0, column=1, sticky="w")
        self.btn_ok.grid(row=0, column=2, sticky="w")
        self.btn_speichern.grid(row=0, column=3, sticky="e")
        self.btn_exportieren.grid(row=0, column=4, sticky="e")

    def on_plagiat_button_click(self):
        # Info speichern
        self.items_plagiat.append(self.items[self.current_item_index])

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.display_plagiat()  # Nächstes Plagiat anzeigen

    def on_unsicher_button_click(self):
        self.items_unsicher.append(self.items[self.current_item_index])  # Info speichern

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.display_plagiat()  # Nächstes Plagiat anzeigen

    def on_ok_button_click(self):
        # Aktuelles Plagiat löschen
        del self.data[self.items[self.current_item_index][1][0]]

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.display_plagiat()  # Nächstes Plagiat anzeigen

    def on_speichern_button_click(self):
        # Aktion für den Speichern-Button
        FileEditor.save_auswertung_to_file(self.data)

    def on_exportieren_button_click(self):
        # Aktion für den Exportieren-Button
        pass

    def create_auswertung(self):
        self.create_auswertung_data()
        self.create_auswertung_gui()

    def create_auswertung_gui(self):
        pass

    def create_auswertung_data(self):
        pass


# table = TableGui(FileEditor.load_auswertung_from_file("last_result"))
