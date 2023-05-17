import tkinter as tk

root = tk.Tk()
root.title("Beispiel GUI")

# Beispiel-Daten
data = {
    "student1": {"Code": "123", "Student": "Max", "Datei": "max.txt"},
    "student2": {"Code": "456", "Student": "Anna", "Datei": "anna.txt"},
    "student3": {"Code": "789", "Student": "Tom", "Datei": "tom.txt"}
}

# Tabelle erstellen
table = tk.Frame(root)
table.pack()

# Überschriften
tk.Label(table, text="Code").grid(row=0, column=0)
tk.Label(table, text="Student").grid(row=0, column=1)
tk.Label(table, text="Datei").grid(row=0, column=2)

# Daten einfügen
for i, student in enumerate(data.values()):
    tk.Label(table, text=student["Code"]).grid(row=i+1, column=0)
    tk.Label(table, text=student["Student"]).grid(row=i+1, column=1)
    tk.Label(table, text=student["Datei"]).grid(row=i+1, column=2)

# Schaltflächen erstellen
buttons = tk.Frame(root)
buttons.pack()

unsicher_button = tk.Button(buttons, text="Unsicher")
unsicher_button.pack(side=tk.LEFT)

kein_plagiat_button = tk.Button(buttons, text="Kein Plagiat")
kein_plagiat_button.pack(side=tk.LEFT)

bestaetigt_button = tk.Button(buttons, text="Bestätigt")
bestaetigt_button.pack(side=tk.LEFT)

speichern_button = tk.Button(buttons, text="Speichern und verlassen")
speichern_button.pack(side=tk.RIGHT)

exportieren_button = tk.Button(buttons, text="Exportieren")
exportieren_button.pack(side=tk.RIGHT)

root.mainloop()
