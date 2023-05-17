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
        vergl_table.grid(row=0, column=0, sticky=N+S+E+W)

        # Scrollbars
        yscrollbar = ttk.Scrollbar(vergl_table, orient=VERTICAL)
        yscrollbar.grid(row=0, column=3, rowspan=3, sticky=N+S)
        xscrollbar = ttk.Scrollbar(vergl_table, orient=HORIZONTAL)
        xscrollbar.grid(row=3, column=0, columnspan=3, sticky=E+W)

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
            ttk.Label(vergl_table, text="Name", style="TableHead.TLabel").grid(row=0, column=0)
            ttk.Label(vergl_table, text="Datei", style="TableHead.TLabel").grid(row=1, column=0)
            ttk.Label(vergl_table, text="Code", style="TableHead.TLabel").grid(row=2, column=0)
            for student_infos in plagiat[1][1]:
                ttk.Label(vergl_table, text=student_infos[0], style="Table.TLabel").grid(row=0, column=column)
                ttk.Label(vergl_table, text=student_infos[1], style="Table.TLabel").grid(row=1, column=column)
                ttk.Label(vergl_table, text=str(student_infos[2]) + "\nfasd\n\tdasd", style="Table.TLabel").grid(row=2, column=column)
                column += 1

        self.root.mainloop()


table = TableGui(FileEditor.load_auswertung_from_file("last_result"))
