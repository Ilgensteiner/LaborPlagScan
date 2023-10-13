import logging
import os
import datetime
import tkinter as tk


# TODO: Mit GUI Update verschieben in Parent
def showErrorMassage(msg, log_dir):
    def open_logs_folder():
        # Plattformabhängige Methode, um den Ordner zu öffnen
        if os.name == 'nt':  # Windows
            os.system(f'start "" "{log_dir}"')
        elif os.name == 'posix':  # macOS and Linux
            os.system(f'open "{log_dir}"')
        else:
            print("Diese Plattform wird nicht unterstützt, um den Ordner zu öffnen.")

    # Erstellen Sie ein Hauptfenster und verstecken Sie es
    root = tk.Tk()
    root.withdraw()

    # Erstellen Sie eine benutzerdefinierte Fehlermeldung
    error_win = tk.Toplevel()
    error_win.title("Fehler")

    # Entfernen Sie die Minimieren/Maximieren-Buttons
    error_win.resizable(0, 0)

    error_win.attributes('-topmost', True)
    error_win.lift()
    error_win.focus_force()

    label = tk.Label(error_win, text="Ein Fehler ist aufgetreten!\nFür Details siehe Log-Datei.", padx=10, pady=10)
    label.pack(pady=10)

    button_frame = tk.Frame(error_win)
    button_frame.pack(pady=10)

    ok_button = tk.Button(button_frame, text="OK", command=error_win.destroy, width=10)
    ok_button.pack(side=tk.LEFT, padx=5)

    open_logs_button = tk.Button(button_frame, text="Logs öffnen", command=open_logs_folder, width=10)
    open_logs_button.pack(side=tk.LEFT, padx=5)

    error_win.mainloop()


def handle_exception(exc_type, exc_value, exc_traceback):
    now = datetime.datetime.now()
    formatted_time = now.strftime('%Y-%m-%d')

    log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'logs')
    log_file = os.path.join(log_dir, f'error_{formatted_time}.log')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Erstellen des FileHandler, wenn der Fehler auftritt
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Handler zum logging hinzufügen
    logging.getLogger('').addHandler(file_handler)

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    # Entfernen des Handler
    logging.getLogger('').removeHandler(file_handler)

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    showErrorMassage(str(exc_value), log_dir)
