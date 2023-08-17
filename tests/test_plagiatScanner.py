import unittest
import warnings
from unittest.mock import MagicMock
import os
import shutil
import json

from laborPlagScan.plagiatScanner import plagscan
from laborPlagScan.fileEditor import extract_zip, unpackZipFiles, save_auswertung_to_file

class TestPlagScan(unittest.TestCase):

    def setUp(self):
        # GUI-Mock erstellen
        self.gui_mock = MagicMock()

        # Arbeitsverzeichnis ändern
        self.original_cwd = os.getcwd()
        parent_directory = os.path.dirname(self.original_cwd)
        os.chdir(parent_directory)

        # DeprecationWarning ignorieren
        warnings.simplefilter("ignore", category=DeprecationWarning)

        # Entpacken der ZIP-Datei
        self.students_folder = extract_zip('tests/resources/Test_Labor.zip')
        self.students_folder = unpackZipFiles(self.students_folder, self.gui_mock)

    def tearDown(self):
        # Testdateien aufräumen
        last_result_path = 'tests/resources/last_result.json'
        if os.path.exists(last_result_path):
            os.remove(last_result_path)
        if os.path.exists("tests/resources/Test_Labor"):
            shutil.rmtree("tests/resources/Test_Labor")

        # Arbeitsverzeichnis zurücksetzen
        os.chdir(self.original_cwd)

        # DeprecationWarning wieder anzeigen
        warnings.simplefilter("default", category=DeprecationWarning)

    def test_plagscan_result(self):
        # Mock für FileEditor.save_auswertung_to_file
        with unittest.mock.patch('laborPlagScan.fileEditor.save_auswertung_to_file') as save_mock:
            save_mock.side_effect = self.save_mock

            # Mock für mainGUI.display_msgbox, um die Anzeige der Message-Box zu unterdrücken
            with unittest.mock.patch('laborPlagScan.mainGUI.display_msgbox') as msgbox_mock:
                msgbox_mock.return_value = None

                # Testaufruf
                plagscan(self.students_folder, self.gui_mock)

                # Überprüfen Sie das Ergebnis
                with open('tests/resources/last_result.json', 'r') as f:
                    result = json.load(f)
                with open('tests/resources/sollResult.json', 'r') as f:
                    expected = json.load(f)

                self.assertEqual(result, expected)

    def test_plagscan_empty_folder(self):
        # Mock für FileEditor.save_auswertung_to_file
        with unittest.mock.patch('laborPlagScan.fileEditor.save_auswertung_to_file') as save_mock:
            save_mock.side_effect = self.save_mock

            # Mock für mainGUI.display_msgbox, um die Anzeige der Message-Box zu unterdrücken
            with unittest.mock.patch('laborPlagScan.mainGUI.display_msgbox') as msgbox_mock:
                msgbox_mock.return_value = None

                # Testaufruf mit leerem Ordner
                empty_folder_path = "tests/resources/Empty_Labor"  # Pfad zum leeren Testordner
                plagscan(empty_folder_path, self.gui_mock)

                # Überprüfen Sie das erwartete Verhalten (kann je nach Anforderungen angepasst werden)
                save_mock.assert_not_called()  # Es sollte kein Ergebnis gespeichert werden

    def test_plagscan_no_java_files(self):
        # Mock für FileEditor.save_auswertung_to_file
        with unittest.mock.patch('laborPlagScan.fileEditor.save_auswertung_to_file') as save_mock:
            save_mock.side_effect = self.save_mock

            # Mock für mainGUI.display_msgbox, um die Anzeige der Message-Box zu unterdrücken
            with unittest.mock.patch('laborPlagScan.mainGUI.display_msgbox') as msgbox_mock:
                msgbox_mock.return_value = None

                # Testaufruf mit einem Ordner ohne Java-Dateien
                no_java_folder_path = "tests/resources/NoJars_Labor/Updated_Labor/extracted"  # Pfad zum Testordner ohne Java-Dateien
                plagscan(no_java_folder_path, self.gui_mock)

                # Überprüfen Sie das erwartete Verhalten (kann je nach Anforderungen angepasst werden)
                save_mock.assert_not_called()  # Es sollte kein Ergebnis gespeichert werden

    def save_mock(self, sorted_plagiat_dict):
        # Ersetzen Sie den Speicherpfad und speichern Sie das Ergebnis
        path = 'tests/resources/'
        save_auswertung_to_file(sorted_plagiat_dict, path=path)


if __name__ == '__main__':
    unittest.main()
