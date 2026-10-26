from datetime import date
from pathlib import Path

from controller import StudienController
from json_speicher import JsonSpeicher
from modelle import Studiengang, Modul, ModulStatus

testdatei = Path(__file__).resolve().parent / "studium_controller_test.json"

studium = Studiengang("Angewandte Künstliche Intelligenz", date(2028, 4, 30), 2.0, 180)

semester = studium.erstelleSemester(1)
analysis = Modul("Mathematik: Analysis", 5)
analysis.aktiviere()
analysis.pruefungsleistung.note = 2.0
analysis.schliesseAb()

computer_vision = Modul("Einführung in Computer Vision", 5)
computer_vision.aktiviere()

semester.fuegeModulHinzu(analysis)
semester.fuegeModulHinzu(computer_vision)

speicher = JsonSpeicher()
speicher.speichern(studium, testdatei)

controller = StudienController(testdatei)
geladenes_studium = controller.laden()

assert geladenes_studium.name == "Angewandte Künstliche Intelligenz"

analysis = controller.finde_modul("Mathematik: Analysis")

assert analysis is not None
assert analysis.status == ModulStatus.ABGESCHLOSSEN

computer_vision = controller.finde_modul("Einführung in Computer Vision")

assert computer_vision is not None
assert computer_vision.status == ModulStatus.AKTIV

erfolg = controller.deaktiviere_modul("Einführung in Computer Vision")

assert erfolg is True
assert computer_vision.status == ModulStatus.OFFEN

testdatei.unlink()

print("Alle Controller-Tests erfolgreich")