import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from laborPlagScan.DataModels.plagiatPaare import PlagiatPaare
from laborPlagScan.DataModels.student import Student
from laborPlagScan.Gui.vergleich import VergleichGui
import laborPlagScan.fileEditor as FileEditor


def on_enter(e):
    frame = e.widget.master
    for button in frame.children.values():
        if isinstance(button, tk.Button):
            button.configure(bg='#e6e6e6')


def on_leave(e):
    frame = e.widget.master
    for button in frame.children.values():
        if isinstance(button, tk.Button):
            button.configure(bg='#ffffff')


class AuswertungGui:
    def __init__(self, plagiatPaareList: [PlagiatPaare], aiDetectedStudentList: [Student]):
        self.plagiatPaareList = plagiatPaareList
        self.aiDetectedStudentList = aiDetectedStudentList
        self.openVerlauf = []

        self.root = tk.Tk()
        self.root.geometry("600x350")
        self.root.title("PlagScan for Java-Labore")
        self.root.configure(bg='#0a3055')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Mainframe
        auswertung_gui = ttk.Frame(self.root)
        auswertung_gui.grid(row=0, column=0, sticky="nsew")
        auswertung_gui.columnconfigure(0, weight=1)
        auswertung_gui.rowconfigure(0, weight=1)

        # Canvas erstellen
        self.canvas = tk.Canvas(auswertung_gui)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)

        self.data_frame = ttk.Frame(self.canvas)
        self.data_frame.grid(row=0, column=0, sticky="nsew")
        self.data_frame.columnconfigure(0, weight=1)  # Volle Breite für das data_frame

        # Platzhalter-Label
        self.placeholder_label = ttk.Label(self.data_frame, text="", background="white", foreground="white", padding=0,
                                           font=("Calibri", 1), borderwidth=0, relief="flat",
                                           width=self.root.winfo_width() - 25)
        self.placeholder_label.grid(row=0, column=0, sticky="nsew")

        self.canvas.create_window((0, 0), window=self.data_frame, anchor="nw")
        self.canvas.bind("<Configure>", self.update_inner_frame, False)
        self.canvas.bind_all("<MouseWheel>",
                             lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        self.canvas.bind_all("<Button-4>", lambda event: self.canvas.xview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda event: self.canvas.xview_scroll(1, "units"))

        # Scrollbars
        yscrollbar = ttk.Scrollbar(auswertung_gui, orient=tk.VERTICAL, command=self.canvas.yview)
        yscrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar = ttk.Scrollbar(auswertung_gui, orient=tk.HORIZONTAL, command=self.canvas.xview)
        xscrollbar.grid(row=1, column=0, sticky="ew")

        # Canvas-Scrollbars-Konfiguration
        self.canvas.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")
        self.progressbar.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=2)
        self.progressbar['maximum'] = len(self.plagiatPaareList)
        self.progressbar['value'] = 0

        self.rowInDataframe = 0
        self.plagiatAuflistung()
        self.aiDetectedAuflistung()

        # Button-Panel erstellen
        button_panel = ttk.Frame(self.root)
        button_panel.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=2)
        button_panel.columnconfigure(1, weight=1)

        # Buttons erstellen
        btn_save = ttk.Button(button_panel, text="Speichern", command=self.on_speichern_button_click)
        btn_exsave = ttk.Button(button_panel, text="Export Savefile", command=self.on_export_savefile_button)
        btn_expdf = ttk.Button(button_panel, text="Export as PDF",
                               command=lambda: self.on_export_table_button(save_as="pdf"))

        # Buttons positionieren
        btn_save.grid(row=0, column=1, sticky="e")
        btn_exsave.grid(row=0, column=2, sticky="e")
        btn_expdf.grid(row=0, column=3, sticky="e")

        self.root.mainloop()

    def update_inner_frame(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.placeholder_label.configure(width=self.root.winfo_width() - 25)

    def update_progressbar(self):
        self.progressbar['value'] += 1
        self.root.update_idletasks()

    def plagiatAuflistung(self):
        self.rowInDataframe += 1
        heading_frame = tk.Frame(self.data_frame)
        heading_frame.grid(row=self.rowInDataframe, column=0, sticky="ew")

        name_button = tk.Button(heading_frame)
        name_button.configure(text="Plagiate", bg="white", foreground="black", padx=5, pady=5, justify="left",
                              anchor="center", font=("Calibri", 12), borderwidth=0.5, relief="solid")
        name_button.grid(row=0, column=0, sticky="ew")
        heading_frame.columnconfigure(0, weight=1)

        for plagiatPaar in self.plagiatPaareList:
            self.rowInDataframe += 1

            button_frame = tk.Frame(self.data_frame)
            button_frame.grid(row=self.rowInDataframe, column=0, sticky="ew")

            name_button_text = f"{plagiatPaar.student1.name[-15:]} - {plagiatPaar.student2.name[-15:]}\t{'[' + plagiatPaar.plagiatStatus + ']' if plagiatPaar.plagiatStatus != '' else ''}"
            name_button = tk.Button(button_frame)
            name_button.configure(text=name_button_text, bg="white", foreground="black", padx=5, pady=5, justify="left",
                                  anchor="w", font=("Calibri", 12), borderwidth=0.5, relief="solid",
                                  command=lambda plagiatPaar_auswahl=plagiatPaar,
                                                 name_button_auswahl=name_button: self.on_plagiatPaar_button(
                                      plagiatPaar_auswahl, name_button_auswahl))
            name_button.grid(row=0, column=0, sticky="ew")
            name_button.bind("<Enter>", on_enter)
            name_button.bind("<Leave>", on_leave)

            accordance_button_text = f"{round(plagiatPaar.plagiatAnteil)} %"
            accordance_button = tk.Button(button_frame,
                                          text=accordance_button_text,
                                          bg="white",
                                          foreground="black",
                                          padx=5, pady=5, justify="left", anchor="center", font=("Calibri", 12),
                                          borderwidth=0.5,
                                          relief="solid", width=8,
                                          command=lambda plagiatPaar_auswahl=plagiatPaar,
                                                         name_button_auswahl=name_button: self.on_plagiatPaar_button(
                                              plagiatPaar_auswahl, name_button_auswahl))
            accordance_button.grid(row=0, column=1, sticky="e")
            accordance_button.bind("<Enter>", on_enter)
            accordance_button.bind("<Leave>", on_leave)

            noplag_button_text = "Kein Plagiat✅"
            noplag_button = tk.Button(button_frame, text=noplag_button_text, bg="white", foreground="black",
                                      padx=5, pady=5, justify="left", anchor="w", font=("Calibri", 12), borderwidth=0.5,
                                      relief="solid",
                                      command=lambda plagiatPaar_entf=plagiatPaar,
                                                     button_frame_entf=button_frame: self.on_button_kein_Plagiat(
                                          plagiatPaar_entf, button_frame_entf))
            noplag_button.grid(row=0, column=2, sticky="e")
            noplag_button.bind("<Enter>", on_enter)
            noplag_button.bind("<Leave>", on_leave)

            button_frame.columnconfigure(0, weight=1)

            self.update_progressbar()
            self.root.update()
            self.update_inner_frame()

    def aiDetectedAuflistung(self):
        self.rowInDataframe += 1
        heading_frame = tk.Frame(self.data_frame)
        heading_frame.grid(row=self.rowInDataframe, column=0, sticky="ew")

        name_button = tk.Button(heading_frame)
        name_button.configure(text="AI Detected", bg="white", foreground="black", padx=5, pady=5, justify="left",
                              anchor="center", font=("Calibri", 12), borderwidth=0.5, relief="solid")
        name_button.grid(row=0, column=0, sticky="ew")
        heading_frame.columnconfigure(0, weight=1)

        for student in self.aiDetectedStudentList:
            self.rowInDataframe += 1

            button_frame = tk.Frame(self.data_frame)
            button_frame.grid(row=self.rowInDataframe, column=0, sticky="ew")

            name_button = tk.Button(button_frame)
            name_button.configure(text=student.name, bg="white", foreground="black", padx=5, pady=5, justify="left",
                                  anchor="w", font=("Calibri", 12), borderwidth=0.5, relief="solid",
                                  command=lambda student_auswahl=student: self.on_student_button(
                                      student_auswahl))
            name_button.grid(row=0, column=0, sticky="ew")
            name_button.bind("<Enter>", on_enter)
            name_button.bind("<Leave>", on_leave)

            button_frame.columnconfigure(0, weight=1)

    def on_button_kein_Plagiat(self, plagiatPaar: PlagiatPaare, button_frame: tk.Frame):
        self.plagiatPaareList.remove(plagiatPaar)
        threading.Thread(target=self.on_speichern_button_click).start()  # Speichern in Datei
        button_frame.destroy()
        self.root.update()

    def update_student_status_button(self, plagiatPaar: PlagiatPaare, name_button: tk.Button):
        self.openVerlauf.append([plagiatPaar, name_button])
        if len(self.openVerlauf) > 2:
            self.openVerlauf.pop(0)
        if len(self.openVerlauf) == 2:
            self.openVerlauf[0][0].plagiatStatus = "checked"
            self.openVerlauf[0][1].config(
                text=f"{self.openVerlauf[0][0].student1.name} - {self.openVerlauf[0][0].student2.name}\t[{self.openVerlauf[0][0].plagiatStatus}]")

        plagiatPaar.plagiatStatus = "last opened"
        name_button.config(
            text=f"{plagiatPaar.student1.name} - {plagiatPaar.student2.name}\t[{plagiatPaar.plagiatStatus}]")
        name_button.update()

    def on_plagiatPaar_button(self, plagiatPaar_auswahl, name_button_auswahl):
        self.update_student_status_button(plagiatPaar_auswahl, name_button_auswahl)
        threading.Thread(target=VergleichGui, kwargs={'plagiatPaar': plagiatPaar_auswahl}).start()

    def on_student_button(self, student_auswahl):
        threading.Thread(target=VergleichGui, kwargs={'single_Student': student_auswahl}).start()

    def on_speichern_button_click(self):
        FileEditor.save_auswertung_to_file([self.plagiatPaareList, self.aiDetectedStudentList])

    def on_export_savefile_button(self):
        FileEditor.save_auswertung_to_file([self.plagiatPaareList, self.aiDetectedStudentList], None, "Auswertung")

    def on_export_table_button(self, save_as="pdf"):
        data = [["Studenten", "Plagiat-Anteil"]]
        row = 0
        while self.data_frame.grid_slaves(row=row, column=0) != []:
            column = 0
            row_content = []
            while self.data_frame.grid_slaves(row=row, column=column) != []:
                grid_widget = self.data_frame.grid_slaves(row=row, column=column)[0]
                if grid_widget.widgetName == "frame":
                    frameinhalt = list(grid_widget.children.values())
                    row_content.append(frameinhalt[0].cget("text").split("[")[0].replace("\t", "    "))
                    row_content.append(frameinhalt[1].cget("text"))
                else:
                    row_content.append(grid_widget.cget("text").replace("\t", "    "))
                column += 1
            data.append(row_content)
            row += 1

        if save_as == "pdf":
            if data[0] == [""]:
                data.pop(0)
            export_path = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                       initialfile="Plagiat Auswertung" + ".pdf",
                                                       filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
            FileEditor.table_to_pdf_export(export_path, data)
        else:
            Exception("Export format not given/supported")
            messagebox.showerror("Export Error", "Export format not given/supported")
