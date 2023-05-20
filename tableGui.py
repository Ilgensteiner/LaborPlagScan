import os.path
import tkinter as tk
from tkinter import ttk, messagebox

import FileEditor
import PlagiatScanner


class TableGui:
    def __init__(self, data):
        self.auswertung_label = None
        self.data = data
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
        self.display_plagiat()
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
        yscrollbar = ttk.Scrollbar(self.vergl_table, orient=tk.VERTICAL)
        yscrollbar.grid(row=0, column=3, rowspan=3, sticky="ns")
        xscrollbar = ttk.Scrollbar(self.vergl_table, orient=tk.HORIZONTAL)
        xscrollbar.grid(row=3, column=0, columnspan=3, sticky="ew")

        # Canvas-Scrollbars-Konfiguration
        canvas.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        # Konfiguration der Scrollbars
        yscrollbar.configure(command=canvas.yview)
        xscrollbar.configure(command=canvas.xview)

        self.inner_frame = ttk.Frame(canvas)
        self.inner_frame.grid(sticky="nsew")

        def update_inner_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        canvas.bind("<Configure>", update_inner_frame)
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        canvas.bind_all("<Button-4>", lambda event: canvas.xview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda event: canvas.xview_scroll(1, "units"))

    def display_plagiat(self):
        # Anzeige des Plagiats
        if self.current_item_index < len(self.items):
            plagiat = self.items[self.current_item_index]
            # Anzeige des Plagiats
            column = 1
            # Spalten
            ttk.Label(self.inner_frame, text="Name", background="white", foreground="black", padding=5,
                      font=("Calibri", 12, "bold"), borderwidth=2, relief="solid").grid(row=0, column=0, sticky="nsew")
            ttk.Label(self.inner_frame, text="Datei", background="white", foreground="black", padding=5,
                      font=("Calibri", 12, "bold"), borderwidth=2, relief="solid").grid(row=1, column=0, sticky="nsew")
            ttk.Label(self.inner_frame, text="Code", background="white", foreground="black", padding=5,
                      font=("Calibri", 12, "bold"), borderwidth=2, relief="solid").grid(row=2, column=0, sticky="nsew")

            for student_infos in plagiat[1][1]:
                ttk.Label(self.inner_frame, text=student_infos[0], background="white", foreground="black", padding=5,
                          font=("Calibri", 12), borderwidth=2, relief="solid").grid(row=0, column=column, sticky="nsew")
                ttk.Label(self.inner_frame, text=os.path.basename(student_infos[1]), background="white",  padding=5,
                          foreground="black", font=("Calibri", 12), borderwidth=2, relief="solid").grid(row=1, column=column, sticky="nsew")
                ttk.Label(self.inner_frame, text=str(FileEditor.read_file(student_infos[1], lines=student_infos[2])),
                          background="white", foreground="black", font=("Calibri", 12), borderwidth=2, padding=5,
                          relief="solid", anchor="nw").grid(row=2, column=column, sticky="nsew")
                column += 1

            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            self.vergl_table.columnconfigure(0, weight=1)
            self.vergl_table.rowconfigure(0, weight=1)
            self.inner_frame.columnconfigure(list(range(column)), weight=1)
        else:
            self.create_auswertung()
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
        self.btn_auswertung = ttk.Button(button_panel, text="Auswertung", command=self.on_auswertung_button_click)

        # Buttons positionieren
        self.btn_plagiat.grid(row=0, column=0, sticky="w")
        self.btn_unsicher.grid(row=0, column=1, sticky="w")
        self.btn_ok.grid(row=0, column=2, sticky="w")
        self.btn_speichern.grid(row=0, column=3, sticky="e")
        self.btn_auswertung.grid(row=0, column=4, sticky="e")

    def on_plagiat_button_click(self):
        # Info speichern
        self.items_plagiat.append(self.items[self.current_item_index])

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.create_table()  # Nächstes Plagiat anzeigen
        self.display_plagiat()

    def on_unsicher_button_click(self):
        self.items_unsicher.append(self.items[self.current_item_index])  # Info speichern

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.create_table()  # Nächstes Plagiat anzeigen
        self.display_plagiat()

    def on_ok_button_click(self):
        # Aktuelles Plagiat löschen
        del self.data[self.items[self.current_item_index][1][0]]

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.create_table()  # Nächstes Plagiat anzeigen
        self.display_plagiat()

    def on_speichern_button_click(self):
        # Aktion für den Speichern-Button
        FileEditor.save_auswertung_to_file(self.data)

    def on_auswertung_button_click(self):
        def on_button_click(answer):
            if answer == "Anzeigen":
                self.create_auswertung()
            elif answer == "Exportieren":
                # Führe hier die Funktion für "Exportieren" aus
                stats = PlagiatScanner.create_stats(self.data)
            else:
                # Abbruch der Funktion
                pass
            root.destroy()

        # Aktion für den Exportieren-Button
        root = tk.Tk()
        label = tk.Label(root, text="Die Auswertung wird erstellt, was möchten Sie tun?")
        label.pack()
        button1 = tk.Button(root, text="Anzeigen", command=lambda: on_button_click("Anzeigen"))
        button1.pack()
        button2 = tk.Button(root, text="Exportieren", command=lambda: on_button_click("Exportieren"))
        button2.pack()
        button3 = tk.Button(root, text="Abbrechen", command=lambda: on_button_click("Abbrechen"))
        button3.pack()
        root.mainloop()

    def create_auswertung(self):
        self.create_auswertung_data()
        self.create_auswertung_gui()

    def create_auswertung_gui(self):
        self.btn_plagiat.grid_remove()
        self.btn_unsicher.grid_remove()
        self.btn_ok.grid_remove()
        self.btn_speichern.grid_remove()
        self.create_table()
        auswertung_label = ttk.Label(self.inner_frame, text=self.auswertung, font=("Calibri", 12), anchor=tk.NW)
        auswertung_label.grid(row=0, column=0, sticky="nsew")

    def create_auswertung_data(self):
        stats = PlagiatScanner.create_stats(self.data)
        self.auswertung = "------Auswertung------\n\n"
        self.auswertung += "Anzahl ausgewerteter Code-Blöcke: " + str(stats[0]) + "\n"
        self.auswertung += "Anzahl der Plagiate: " + str(len(self.items_plagiat)) + "\n"
        self.auswertung += "Anzahl der unsicheren Plagiate: " + str(len(self.items_unsicher)) + "\n\n"
        self.auswertung += "Auswertung Studenten:\n"
        self.auswertung += "Anzahl der Studenten: " + str(stats[1]) + "\n"
        for student in stats[2]:
            self.auswertung += student + ": " + str(stats[2][student]) + "\n"

        self.auswertung += "\n\nStudenten-Paare:\n"
        for student in stats[3]:
            self.auswertung += student + ": " + str(stats[3][student]) + "\n"

