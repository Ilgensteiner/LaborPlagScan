import os
import shutil
import unittest
import tempfile
import zipfile

from laborPlagScan.fileEditor import extract_zip, unpackZipFiles

class MockGUI:
    def __init__(self):
        self.progressbar_value = 0
        self.progressbar_max = 0

    def set_progressbar_start(self, value):
        self.progressbar_max = value

    def update_progressbar_value(self, increment):
        self.progressbar_value += increment

class TestExtractZip(unittest.TestCase):

    def setUp(self):
        # Test-ZIP-Dateien erstellen
        self.valid_zip_path = 'test.zip'
        with zipfile.ZipFile(self.valid_zip_path, 'w') as zipf:
            zipf.writestr('test.txt', 'This is a test')

        self.empty_zip_path = 'empty.zip'
        with zipfile.ZipFile(self.empty_zip_path, 'w') as zipf:
            pass

        self.invalid_zip_path = 'invalid.zip'

    def tearDown(self):
        # Aufräumen
        os.remove(self.valid_zip_path)
        os.remove(self.empty_zip_path)
        shutil.rmtree('test', ignore_errors=True)
        shutil.rmtree('empty', ignore_errors=True)

    def test_valid_zip(self):
        path = extract_zip(self.valid_zip_path)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(os.path.join(path, 'test.txt')))

    def test_invalid_zip(self):
        with self.assertRaises(FileNotFoundError):
            extract_zip(self.invalid_zip_path)

    def test_empty_zip(self):
        path = extract_zip(self.empty_zip_path)
        #weil bei leerer zip datei kein ordner erstellt wird
        self.assertFalse(os.path.exists(path))

class TestUnpackZipFiles(unittest.TestCase):
    def create_zip(self, path, name):
        zip_path = os.path.join(path, name + '.zip')
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.writestr('test_file.txt', 'Test content')
        return zip_path

    def test_unpack_zip_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # ZIP-Datei im Hauptordner erstellen
            self.create_zip(temp_dir, 'main_zip')

            # Mock GUI erstellen
            gui = MockGUI()

            # Die unpackZipFiles-Funktion aufrufen
            extract_path = unpackZipFiles(temp_dir, gui)

            # Überprüfen, ob die ZIP-Dateien korrekt extrahiert wurden
            self.assertTrue(os.path.exists(os.path.join(temp_dir, 'extracted', 'main_zip', 'test_file.txt')))

            # Überprüfen, ob die GUI-Methoden korrekt aufgerufen wurden
            self.assertEqual(gui.progressbar_max, len(os.listdir(temp_dir))-1)
            self.assertEqual(gui.progressbar_value, len(os.listdir(temp_dir))-1)

            # Überprüfen, ob der zurückgegebene Pfad korrekt ist
            expected_extract_path = os.path.join(temp_dir, "extracted")
            self.assertEqual(extract_path, expected_extract_path)

if __name__ == '__main__':
    unittest.main()
