import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from laborPlagScan.DataModels.plagiatPaare import PlagiatPaare
import laborPlagScan.fileEditor as FileEditor
from laborPlagScan.DataModels.student import Student
from laborPlagScan.filter import Filter


class VergleichGui:
    def __init__(self, plagiatPaar: PlagiatPaare = None, single_Student: Student = None):
        if plagiatPaar is None and single_Student is None:
            raise Exception("No PlagiatPaar or Student given")
        self.plagiatPaar = plagiatPaar

        self.root = tk.Tk()
        self.root.geometry("600x350")
        self.root.title("PlagScan for Java-Labore")
        self.root.configure(bg='#0a3055')

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

        if self.plagiatPaar is not None:
            self.display_stud_vergleich()
        else:
            self.display_stud(single_Student)
        self.create_button_panel_einzelauswertung()

        self.root.mainloop()

    def display_stud_vergleich(self):
        """Anzeige der Studierenden im Vergleichsmodus"""

        ttk.Label(self.inner_frame, text=self.plagiatPaar.student1.name, background="white", foreground="black", padding=5,
                  font=("Calibri", 12, "bold"), borderwidth=2, relief="solid").grid(row=0, column=0, sticky="nsew")
        ttk.Label(self.inner_frame, text=self.plagiatPaar.student2.name, background="white", foreground="black", padding=5,
                  font=("Calibri", 12, "bold"), borderwidth=2, relief="solid").grid(row=0, column=1, sticky="nsew")

        def display_Files(student_file_list, column):
            row = 1
            for file in student_file_list:
                ttk.Label(self.inner_frame, text=file.name, background="white", foreground="black", padding=5,
                          font=("Calibri", 12), borderwidth=2, relief="solid").grid(row=row, column=column,
                                                                                    sticky="nsew")
                row += 1

                file_textfeld = tk.Text(self.inner_frame, background="white", foreground="black", font=("Calibri", 12),
                                        borderwidth=2, relief="solid")
                file_textfeld.grid(row=row, column=column, sticky="nsew")
                file_textfeld.tag_config("red", foreground="red")
                file_textfeld.insert(tk.END, re.sub(r' {3,}', '   ', str(file.getFileString()).expandtabs(2)))
                height = int(file_textfeld.index('end-1c').split('.')[0])
                max_line_length = max(
                    [len(line.strip("\n\t\r")) for line in file_textfeld.get("1.0", "end-1c").split("\n")])
                file_textfeld.configure(state="disabled", yscrollcommand=lambda *args: None,
                                        xscrollcommand=lambda *args: None, height=height,
                                        width=int(max_line_length * 0.9), padx=5)

                for abschnitt in file.plagatierteZeilenMarktiert:
                    file_textfeld.tag_add("red", f"{abschnitt[0]}.0", f"{abschnitt[1]}.0")
                row += 1

        self.plagiatPaar.markPlagiatCodeinFiles()
        display_Files(self.plagiatPaar.student1.files, 0)
        display_Files(self.plagiatPaar.student2.files, 1)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.vergl_table.columnconfigure(0, weight=1)
        self.vergl_table.rowconfigure(0, weight=1)
        self.inner_frame.columnconfigure(list(range(2)), weight=1)

        self.root.update()

    def display_stud(self, student: Student):
        """Anzeige eines einzelnen Studierenden bei AI-Detektion"""
        ttk.Label(self.inner_frame, text=student.name, background="white", foreground="black", padding=5,
                  font=("Calibri", 12, "bold"), borderwidth=2, relief="solid").grid(row=0, column=0, sticky="nsew")

        row = 1
        for file in student.files:
            ttk.Label(self.inner_frame, text=file.name, background="white", foreground="black", padding=5,
                      font=("Calibri", 12), borderwidth=2, relief="solid").grid(row=row, column=0,
                                                                                sticky="nsew")
            row += 1

            file_textfeld = tk.Text(self.inner_frame, background="white", foreground="black", font=("Calibri", 12),
                                    borderwidth=2, relief="solid")
            file_textfeld.grid(row=row, column=0, sticky="nsew")
            row += 1
            file_textfeld.tag_config("red", foreground="red")
            file_textfeld.insert(tk.END, re.sub(r' {3,}', '   ', str(file.getFileString()).expandtabs(2)))
            height = int(file_textfeld.index('end-1c').split('.')[0])
            max_line_length = max(
                [len(line.strip("\n\t\r")) for line in file_textfeld.get("1.0", "end-1c").split("\n")])
            file_textfeld.configure(state="disabled", yscrollcommand=lambda *args: None,
                                    xscrollcommand=lambda *args: None, height=height,
                                    width=int(max_line_length * 0.9), padx=5)

            for injectedVar in Filter.getAiDetactionVarsList():
                # Startposition
                start_pos = '1.0'
                while True:
                    # Finde das nächste Vorkommen des Wortes
                    start_pos = file_textfeld.search(injectedVar, start_pos, nocase=True, stopindex=tk.END)
                    if not start_pos:
                        break
                    # Ende der Markierung für dieses Vorkommen finden
                    end_pos = f'{start_pos}+{len(injectedVar)}c'
                    # Tag hinzufügen
                    file_textfeld.tag_add('red', start_pos, end_pos)
                    # Update der Startposition für die nächste Suche
                    start_pos = end_pos

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.vergl_table.columnconfigure(0, weight=1)
        self.vergl_table.rowconfigure(0, weight=1)
        self.inner_frame.columnconfigure(list(range(2)), weight=1)

        self.root.update()

    def create_button_panel_einzelauswertung(self):
        """Erstellt das Button-Panel für den Einzel-Auswertungs-Modus"""
        # Button-Panel erstellen
        button_panel = ttk.Frame(self.root)
        button_panel.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=2)
        button_panel.columnconfigure(1, weight=1)

        # Buttons erstellen
        btn_expExcel = ttk.Button(button_panel, text="Export as Excel",
                               command=lambda: self.on_export_table_button(save_as="xlsx"))

        # Buttons positionieren
        btn_expExcel.grid(row=0, column=1, sticky="e")

    def on_export_table_button(self, save_as="xlsx"):
        data = []
        row = 0
        grid_size = self.inner_frame.grid_size()

        for row in range(grid_size[1]):
            row_content = []
            for column in range(grid_size[0]):
                if not self.inner_frame.grid_slaves(row=row, column=column):
                    row_content.append("")
                    continue
                grid_widget = self.inner_frame.grid_slaves(row=row, column=column)[0]
                if grid_widget.widgetName == "text":
                    row_content.append(grid_widget.get("1.0", "end-1c").replace("\t", "    "))
                elif grid_widget.widgetName == "frame":
                    frameinhalt = list(grid_widget.children.values())
                    row_content.append(frameinhalt[0].cget("text").split("  [")[0].replace("\t", "    "))
                    row_content.append(frameinhalt[1].cget("text"))
                else:
                    row_content.append(grid_widget.cget("text").replace("\t", "    "))
            data.append(row_content)

        if save_as == "xlsx":
            export_path = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                       initialfile=f"Plagiat ({str(round(self.plagiatPaar.plagiatAnteil_Relativ))} %) " + " - ".join(data[0]) + ".xlsx",
                                                       filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
            FileEditor.table_to_xlsx_export(export_path, data)
        else:
            Exception("Export format not given/supported")
            messagebox.showerror("Export Error", "Export format not given/supported")
