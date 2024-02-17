import logging
import os
import datetime
import sys
import tkinter as tk

ERROR_WINDOW_OPEN = False


def showErrorMassage(msg, log_dir, custom_msg: str = None):
    def open_logs_folder():
        # Plattformabhängige Methode, um den Ordner zu öffnen
        if os.name == 'nt':  # Windows
            os.system(f'start "" "{log_dir}"')
        elif os.name == 'posix':  # macOS and Linux
            os.system(f'open "{log_dir}"')
        else:
            print("Diese Plattform wird nicht unterstützt, um den Ordner zu öffnen.")

    def close_window():
        global ERROR_WINDOW_OPEN
        ERROR_WINDOW_OPEN = False
        error_win.destroy()
        if custom_msg is None:
            sys.exit(0)

    if custom_msg is None:
        # Soll neues Hauptfenster sein weil kritischer Fehler
        root = tk.Tk()
        root.withdraw()
    else:
        global ERROR_WINDOW_OPEN
        ERROR_WINDOW_OPEN = True

    # Erstellen Sie eine benutzerdefinierte Fehlermeldung
    error_win = tk.Toplevel()
    error_win.title("Fehler")

    # Entfernen Sie die Minimieren/Maximieren-Buttons
    error_win.resizable(0, 0)

    error_win.attributes('-topmost', True)
    error_win.lift()
    error_win.focus_force()

    if custom_msg is not None:
        label = tk.Label(error_win, text=custom_msg + "\nFür Details siehe Log-Datei.", padx=10, pady=10)
    else:
        label = tk.Label(error_win, text="Ein kritischer Fehler ist aufgetreten und das Programm wird beendet!\nFür Details siehe Log-Datei.", padx=10, pady=10)

    label.pack(pady=10)

    button_frame = tk.Frame(error_win)
    button_frame.pack(pady=10)

    ok_button = tk.Button(button_frame, text="OK", command=close_window, width=10)
    ok_button.pack(side=tk.LEFT, padx=5)

    open_logs_button = tk.Button(button_frame, text="Logs öffnen", command=open_logs_folder, width=10)
    open_logs_button.pack(side=tk.LEFT, padx=5)

    if custom_msg is None:
        error_win.mainloop()


def handle_exception(exc_type, exc_value, exc_traceback, custom_msg: str = None, custom_log_info: str = "Uncaught exception"):
    try:
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d')

        log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'logs')
        log_file = os.path.join(log_dir, f'error_{formatted_time}.log')

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Erstellen des FileHandler, wenn der Fehler auftritt
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setFormatter(logging.Formatter('\n%(asctime)s - %(levelname)s - %(message)s'))

        # Handler zum logging hinzufügen
        logging.getLogger('').addHandler(file_handler)

        logging.error(custom_log_info, exc_info=(exc_type, exc_value, exc_traceback))

        # Entfernen des Handler
        logging.getLogger('').removeHandler(file_handler)

        global ERROR_WINDOW_OPEN
        if ERROR_WINDOW_OPEN is False:
            showErrorMassage(str(exc_value), log_dir, custom_msg)
    except Exception as e:
        print(f"Kritischer Fehler in handle_exceptio: {e}")
        sys.exit(0)
