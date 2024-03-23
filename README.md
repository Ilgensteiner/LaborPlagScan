# LaborPlagScan
Labor Plagiat Scanner für Prog. an der HS-Harz. Ziel ist es die Abgaben der Studierenden auf Plagiate zu überprüfen.

## Installation

1. Du benötigst Python 3.10. Stelle sicher, dass während der Installation die Option "Add to PATH" aktiviert ist. Falls du Python noch nicht installiert hast, kannst du es [hier](https://www.python.org/downloads/) herunterladen. <br>(Wenn nötig) Eine Anleitung, wie du Python zum PATH hinzufügen kannst, findest du [hier](https://datatofish.com/add-python-to-windows-path/).

2. `run.bat` (Win) bzw. `run.sh` (Linux) ausführen um die erstmalige Installation zu starten.

## Anleitung

1. Starte `run.bat` (Win) bzw. `run.sh` (Linux)
2. Lade den vollständigen Abgaben Ordner aus StudIP herunter
3. Wähle die ZIP-Datei aus (Abgaben-Ordner)
4. Starte PlagScan
5. Schaue dir die Ergebnisse an

## Einstellungen des PlagiatScanners

Mit den Einstellungen des PlagiatScanners kannst du verschiedene Parameter anpassen, um die Effizienz und Genauigkeit der Plagiaterkennung zu verbessern. Hier findest du eine Übersicht der verfügbaren Einstellungsoptionen.

### Filter
Die Filteroptionen ermöglichen es dir, spezifische Abschnitte oder Codezeilen zu ignorieren, damit diese nicht fälschlicherweise als Plagiate identifiziert werden.
1. Variablennamen: Standardmäßig werden Variablennamen im Code mit 'x' bezeichnet. Beispiel: this.x = x;. Diese Konvention hilft, den Code einheitlich zu halten.
2. Reguläre Ausdrücke (Regex): Nutze reguläre Ausdrücke, um bestimmte Muster im Code zu identifizieren und zu ignorieren. Jede Regel sollte mit 'Regex:' eingeleitet werden. Diese Ausdrücke sind entscheidend, um diverse Codestrukturen zu erkennen und korrekt zu analysieren.
3. Dateinamen: Mit dieser Einstellung kannst du bestimmte Dateien von der Überprüfung ausschließen. Verwende das Format 'File:Dateiname.extension', um gezielt Dateien auszuwählen, die nicht auf Plagiate geprüft werden sollen.
4. AI-Detection-Variablen: Durch diese Einstellung, eingeleitet mit 'AI-Var:', kannst du spezifische Variablen identifizieren, die durch KI-basierte PromptInjection in Aufgabenstellungen generiert wurden. Dies unterstützt die Erkennung von potenziellen Plagiaten, die durch künstliche Intelligenz entstanden sind.

## Beitragen

Dieses Projekt ist öffentlich auf GitHub und wir freuen uns über Beiträge. Wenn du einen Bug findest oder eine Verbesserung vorschlagen möchtest, erstelle bitte ein neues Issue in unserem GitHub Repository. Wenn du einen Beitrag zum Code leisten möchtest, stelle bitte einen Pull Request mit deinen Änderungen bereit. Bitte stelle sicher, dass dein Code den aktuellen Standards entspricht und alle Tests besteht.

## Kontakt und Support

Falls du Fragen hast, auf Probleme stößt oder Unterstützung benötigst, kannst du ein Issue in unserem GitHub-Repository erstellen. Wir werden unser Bestes tun, um dir so schnell wie möglich zu helfen.
