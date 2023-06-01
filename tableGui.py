import os.path
import re
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.ttk import Frame
import FileEditor
import PlagiatScanner


def filter_dict(data: dict, filters: list):
    """Filtert ein Dictionary (StudPlagData) nach den angegebenen Filtern (Liste mit Studentennamen)"""
    result = []
    filtered_items = []
    for pos, value in enumerate(data.values()):
        student_name = []
        for item in value:
            student_name.append(item[0])
        if set(filters).issubset(student_name):
            for item in value:
                if item[0] in filters:
                    filtered_items.append(item)

        if filtered_items:
            result.append([pos, filtered_items])
            filtered_items = []

    return result


class TableGui:
    inner_frame: Frame

    def __init__(self, data, stud_filter=None):
        self.btn_speichern = None
        self.btn_auswertung = None
        self.btn_ok = None
        self.btn_unsicher = None
        self.btn_plagiat = None
        self.vergl_table = None
        self.auswertung_label = None
        self.data = data
        self.items = []
        self.items_plagiat = []
        self.items_unsicher = []
        self.items_kein_plagiat = []
        if stud_filter is None:
            for i, item in enumerate(data.items()):
                self.items.append([i, item])
        else:
            self.items = filter_dict(data, stud_filter)

        self.current_item_index = 0  # Aktueller Index im Datensatz

        self.root = tk.Tk()
        self.root.geometry("600x350")
        self.root.title("PlagScan for Java-Labore")
        self.root.configure(bg='#0a3055')

        if stud_filter is None:
            self.create_auswertung()
        else:
            self.create_table_plag()
            self.display_stud_vergleich(stud_filter)
            self.create_button_panel_einzelauswertung()

        self.root.mainloop()

    def create_table_plag(self):
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
                ttk.Label(self.inner_frame, text=os.path.basename(student_infos[1]), background="white", padding=5,
                          foreground="black", font=("Calibri", 12), borderwidth=2, relief="solid").grid(row=1,
                                                                                                        column=column,
                                                                                                        sticky="nsew")
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

    def display_stud_vergleich(self, filtered_studs):
        # create and fill dict with all files / plag of students
        stud_files = {}
        for plagiat in self.items:
            for stud in plagiat[1]:
                stud_files.setdefault(stud[0], {}).setdefault(stud[1], []).append(stud[2])
        # display files
        for i, stud in enumerate(filtered_studs):
            ttk.Label(self.inner_frame, text=stud, background="white", foreground="black", padding=5,
                      font=("Calibri", 12, "bold"), borderwidth=2, relief="solid").grid(row=0, column=i, sticky="nsew")
            j = 1
            for file in stud_files[stud]:
                ttk.Label(self.inner_frame, text=os.path.basename(file), background="white", foreground="black",
                          padding=5, font=("Calibri", 12), borderwidth=2, relief="solid").grid(row=j, column=i,
                                                                                               sticky="nsew")
                j += 1
                textfeld = tk.Text(self.inner_frame, background="white", foreground="black", font=("Calibri", 12),
                                   borderwidth=2, relief="solid")
                textfeld.grid(row=j, column=i, sticky="nsew")
                textfeld.tag_config("red", foreground="red")
                textfeld.insert(tk.END, re.sub(r' {3,}', '   ', str(FileEditor.read_file(file)).expandtabs(2)))

                height = int(textfeld.index('end-1c').split('.')[0])
                max_line_length = max([len(line.strip("\n\t\r")) for line in textfeld.get("1.0", "end-1c").split("\n")])
                textfeld.configure(state="disabled", yscrollcommand=lambda *args: None,
                                   xscrollcommand=lambda *args: None, height=height, width=int(max_line_length * 0.9),
                                   padx=5)
                for plag in stud_files[stud][file]:
                    textfeld.tag_add("red", str(plag[0] + 1) + ".0", str(plag[1] + 1) + ".599")
                j += 1

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.vergl_table.columnconfigure(0, weight=1)
        self.vergl_table.rowconfigure(0, weight=1)
        self.inner_frame.columnconfigure(list(range(2)), weight=1)

        self.root.update()

    def create_button_panel_plagiat(self):
        # Button-Panel erstellen
        button_panel = ttk.Frame(self.root)
        button_panel.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=2)
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

    def create_button_panel_auswertung(self):
        # Button-Panel erstellen
        button_panel = ttk.Frame(self.root)
        button_panel.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=2)
        button_panel.columnconfigure(1, weight=1)

        # Buttons erstellen
        btn_einzelplag = ttk.Button(button_panel, text="Einzel Plagiate", command=self.on_open_einzelplagiat_button)
        btn_exsave = ttk.Button(button_panel, text="Export Savefile", command=self.on_export_savefile_button)
        btn_expdf = ttk.Button(button_panel, text="Export as PDF",
                               command=lambda: self.on_export_table_button(save_as="pdf"))

        # Buttons positionieren
        btn_einzelplag.grid(row=0, column=0, sticky="w")
        btn_exsave.grid(row=0, column=1, sticky="e")
        btn_expdf.grid(row=0, column=2, sticky="e")

    def create_button_panel_einzelauswertung(self):
        # Button-Panel erstellen
        button_panel = ttk.Frame(self.root)
        button_panel.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=2)
        button_panel.columnconfigure(1, weight=1)

        # Buttons erstellen
        btn_expdf = ttk.Button(button_panel, text="Export as Excel",
                               command=lambda: self.on_export_table_button(save_as="xlsx"))

        # Buttons positionieren
        btn_expdf.grid(row=0, column=0, sticky="e")

    def on_open_einzelplagiat_button(self):
        self.create_table_plag()
        self.display_plagiat()
        self.create_button_panel_plagiat()

    def on_plagiat_button_click(self):
        # Information speichern
        self.items_plagiat.append(self.items[self.current_item_index])

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.create_table_plag()  # Nächstes Plagiat anzeigen
        self.display_plagiat()

    def on_unsicher_button_click(self):
        self.items_unsicher.append(self.items[self.current_item_index])  # Information speichern

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.create_table_plag()  # Nächstes Plagiat anzeigen
        self.display_plagiat()

    def on_ok_button_click(self):
        # Aktuelles Plagiat löschen
        del self.data[self.items[self.current_item_index][1][0]]

        self.current_item_index += 1  # Zum nächsten Element wechseln
        self.create_table_plag()  # Nächstes Plagiat anzeigen
        self.display_plagiat()

    def on_speichern_button_click(self):
        # Aktion für den Speichern-Button
        FileEditor.save_auswertung_to_file(self.data)

    def on_auswertung_button_click(self):
        self.create_auswertung()

    def create_auswertung(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_auswertung_gui()

    def create_auswertung_gui(self):
        stats = PlagiatScanner.create_stats(self.data)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Mainframe
        auswertung_gui = ttk.Frame(self.root)
        auswertung_gui.grid(row=0, column=0, sticky="nsew")
        auswertung_gui.columnconfigure(0, weight=1)
        auswertung_gui.rowconfigure(0, weight=1)

        self.create_button_panel_auswertung()

        # Canvas erstellen
        canvas = tk.Canvas(auswertung_gui)
        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.columnconfigure(0, weight=1)
        canvas.rowconfigure(0, weight=1)

        data_frame = ttk.Frame(canvas)
        data_frame.grid(row=0, column=0, sticky="nsew")
        data_frame.columnconfigure(0, weight=1)  # Volle Breite für das data_frame

        # Platzhalter-Label
        placeholder_label = ttk.Label(data_frame, text="", background="white", foreground="white", padding=0,
                                      font=("Calibri", 1), borderwidth=0, relief="flat", width=self.root.winfo_width()-25)
        placeholder_label.grid(row=0, column=0,  columnspan=3, sticky="nsew")

        def update_inner_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            placeholder_label.configure(width=self.root.winfo_width()-25)

        canvas.create_window((0, 0), window=data_frame, anchor="nw")
        canvas.bind("<Configure>", update_inner_frame, False)
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        canvas.bind_all("<Button-4>", lambda event: canvas.xview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda event: canvas.xview_scroll(1, "units"))

        # Scrollbars
        yscrollbar = ttk.Scrollbar(auswertung_gui, orient=tk.VERTICAL, command=canvas.yview)
        yscrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar = ttk.Scrollbar(auswertung_gui, orient=tk.HORIZONTAL, command=canvas.xview)
        xscrollbar.grid(row=1, column=0, sticky="ew")

        # Canvas-Scrollbars-Konfiguration
        canvas.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        # DATA
        tk.Label(data_frame, text="\tÜbersicht", background="white", foreground="black", padx=5, pady=5,
                 justify="center",
                 font=("Calibri", 12, "bold"), borderwidth=0.5, relief="solid", anchor="w").grid(row=1, column=0, columnspan=3, sticky="ew")
        tk.Label(data_frame, text="Anzahl ausgewerteter Code-Blöcke: " + str(stats[0]), background="white",
                 foreground="black", padx=5, pady=5, justify="center",
                 font=("Calibri", 12), borderwidth=0.5, relief="solid", anchor="w").grid(row=2, column=0, columnspan=3, sticky="ew")
        tk.Label(data_frame, text="Anzahl der Plagiate: " + str(len(self.items_plagiat)), background="white",
                 foreground="black", padx=5, pady=5, justify="center",
                 font=("Calibri", 12), borderwidth=0.5, relief="solid", anchor="w").grid(row=3, column=0, columnspan=3, sticky="ew")
        tk.Label(data_frame, text="Anzahl der unsicheren Plagiate: " + str(len(self.items_unsicher)),
                 background="white", foreground="black", padx=5, pady=5, justify="center",
                 font=("Calibri", 12), borderwidth=0.5, relief="solid", anchor="w").grid(row=4, column=0, columnspan=3, sticky="ew")

        tk.Label(data_frame, text="\tAuswertung Studenten:", background="white", foreground="black", padx=5, pady=5,
                 justify="center",
                 font=("Calibri", 12, "bold"), borderwidth=0.5, relief="solid", anchor="w").grid(row=5, column=0, columnspan=3,
                                                                                                 sticky="ew")
        tk.Label(data_frame, text="Anzahl der Studenten mit Plagiaten: " + str(stats[1]), background="white",
                 foreground="black",
                 padx=5, pady=5, justify="left",
                 font=("Calibri", 12), borderwidth=0.5, relief="solid", anchor="w").grid(row=6, column=0, columnspan=3, sticky="ew")
        tk.Label(data_frame, text="\tGefundene Plagiate pro Student", background="white", foreground="black", padx=5,
                 pady=5,
                 justify="center",
                 font=("Calibri", 12), borderwidth=0.5, relief="solid", anchor="w").grid(row=7, column=0, columnspan=3, sticky="ew")

        row = 7
        for student in stats[2]:
            row += 1
            tk.Button(data_frame, text=student + ": " + str(stats[2][student]), bg="white", foreground="black",
                      padx=5, pady=5, justify="left", anchor="w", font=("Calibri", 12), borderwidth=0.5,
                      relief="solid",
                      command=lambda student_filter=student: self.on_student_button([student_filter])).grid(row=row,
                                                                                                            column=0,
                                                                                                            sticky="ew")

            tk.Button(data_frame, text=str(self.stud_plagiat_accordance([student])) + " %", bg="white", foreground="black",
                      padx=5, pady=5, justify="left", anchor="w", font=("Calibri", 12), borderwidth=0.5,
                      relief="solid",
                      command=lambda student_filter=student: self.on_student_button([student_filter])).grid(row=row,
                                                                                                            column=1,
                                                                                                            sticky="ew")

            tk.Button(data_frame, text="Kein Plagiat✅", bg="white", foreground="black",
                      padx=5, pady=5, justify="left", anchor="w", font=("Calibri", 12), borderwidth=0.5,
                      relief="solid",
                      command=self.on_auswertung_kein_plagiat_button).grid(row=row, column=2, sticky="ew")

        row += 1
        tk.Label(data_frame, text="\tAnzahl Plagiate bei Studentenpaaren:", background="white", foreground="black",
                 padx=5, pady=5,
                 justify="center", font=("Calibri", 12, "bold"), borderwidth=0.5, relief="solid",
                 anchor="w").grid(row=row, column=0, columnspan=3, sticky="ew")

        for student in stats[3]:
            row += 1
            tk.Button(data_frame, text=student + ": " + str(stats[3][student]), bg="white", foreground="black",
                      padx=5, pady=5, justify="left", anchor="w", font=("Calibri", 12), borderwidth=0.5,
                      relief="solid",
                      command=lambda student_filter=student.split(" - "): self.on_student_button(student_filter)).grid(
                row=row, column=0, sticky="ew")

            tk.Button(data_frame, text=str(self.stud_plagiat_accordance(student.split(" - "))) + " %", bg="white",
                      foreground="black",
                      padx=5, pady=5, justify="left", anchor="w", font=("Calibri", 12), borderwidth=0.5,
                      relief="solid",
                      command=lambda student_filter=student.split(" - "): self.on_student_button(student_filter)).grid(
                row=row, column=1, sticky="ew")

            tk.Button(data_frame, text="Kein Plagiat✅", bg="white", foreground="black",
                      padx=5, pady=5, justify="left", anchor="w", font=("Calibri", 12), borderwidth=0.5,
                      relief="solid",
                      command=self.on_auswertung_kein_plagiat_button).grid(row=row, column=2, sticky="ew")

        self.inner_frame = data_frame
        self.root.update()

    def stud_plagiat_accordance(self, studentlist: list):
        """
        :param studentlist: list of students
        :return: %-value of students with plagiarism
        """
        filedict = {}
        items = filter_dict(self.data, studentlist)
        for item in items:
            for plagiat in item[1]:
                if plagiat[0] + str(os.path.basename(plagiat[1])) not in filedict:
                    file_as_list = []
                    for c, line in enumerate(FileEditor.read_file(plagiat[1]).split("\n")):
                        file_as_list.append([c, line])
                    file = PlagiatScanner.filter_lines(file_as_list)
                    filedict[plagiat[0] + str(os.path.basename(plagiat[1]))] = file

                for i, file_line in enumerate(filedict[plagiat[0] + str(os.path.basename(plagiat[1]))]):
                    if plagiat[2][0] <= file_line[0] <= plagiat[2][1] and not \
                    filedict[plagiat[0] + str(os.path.basename(plagiat[1]))][i][1].startswith("plag###"):
                        filedict[plagiat[0] + str(os.path.basename(plagiat[1]))][i][1] = "plag###" + filedict[
                            plagiat[0] + str(os.path.basename(plagiat[1]))][i][1]

        row_all = 0
        row_plag = 0
        for file in filedict:
            for row in filedict[file]:
                row[1].strip()
                if row[1] == "":
                    continue
                row_all += 1
                if row[1].startswith("plag###"):
                    row_plag += 1

        return round((row_plag / row_all) * 100, 2)

    def on_auswertung_kein_plagiat_button(self):
        pass

    def on_student_button(self, filter_list):
        TableGui(self.data, filter_list)

    def on_export_savefile_button(self):
        FileEditor.save_auswertung_to_file(self.data, None, "Auswertung")

    def on_export_table_button(self, save_as="pdf"):
        data = []
        row = 0
        while self.inner_frame.grid_slaves(row=row, column=0) != []:
            column = 0
            row_content = []
            while self.inner_frame.grid_slaves(row=row, column=column) != []:
                grid_widget = self.inner_frame.grid_slaves(row=row, column=column)[0]
                if grid_widget.widgetName == "text":
                    row_content.append(grid_widget.get("1.0", "end-1c"))
                else:
                    row_content.append(grid_widget.cget("text"))
                column += 1
            data.append(row_content)
            row += 1

        if save_as == "pdf":
            if data[0] == [""]:
                data.pop(0)
            export_path = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                       initialfile="Plagiat " + "-".join(data[0]).strip(
                                                           '\t\n') + ".pdf",
                                                       filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
            FileEditor.table_to_pdf_export(export_path, data)
        elif save_as == "xlsx":
            export_path = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                       initialfile="Plagiat " + "-".join(data[0]) + ".xlsx",
                                                       filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
            FileEditor.table_to_xlsx_export(export_path, data)
        else:
            Exception("Export format not given/supported")
            messagebox.showerror("Export Error", "Export format not given/supported")
