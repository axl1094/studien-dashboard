from datetime import date
from pathlib import Path

from modelle import Studiengang, Modul, ModulStatus
from json_speicher import JsonSpeicher

studium = Studiengang("Angewandte Künstliche Intelligenz", date(2028, 4, 30), 2.0, 180)

semester = studium.erstelleSemester(1)

analysis = Modul("Mathematik: Analysis", 5)
analysis.aktiviere()
analysis.pruefungsleistung.note = 2.0
analysis.schliesseAb()

computer_vision = Modul("Einführung in Computer Vision", 5)
computer_vision.aktiviere()

kollaboratives_arbeiten = Modul("Kollaboratives Arbeiten", 5)
kollaboratives_arbeiten.aktiviere()
kollaboratives_arbeiten.pruefungsleistung.anerkannt = True
kollaboratives_arbeiten.schliesseAb()

semester.fuegeModulHinzu(analysis)
semester.fuegeModulHinzu(computer_vision)
semester.fuegeModulHinzu(kollaboratives_arbeiten)

testdatei = Path(__file__).resolve().parent / "studium_test.json"

speicher = JsonSpeicher()
speicher.speichern(studium, testdatei)

geladenes_studium = speicher.laden(testdatei)

assert geladenes_studium.name == "Angewandte Künstliche Intelligenz"
assert geladenes_studium.ects_erreicht == 10
assert geladenes_studium.anzahl_abgeschlossen == 2
assert geladenes_studium.anzahl_aktiv == 1
assert geladenes_studium.anzahl_offen == 0
assert geladenes_studium.aktuelle_note == 2.0

geladenes_modul = None

for semester in geladenes_studium.semester:
    for modul in semester.module:
        if modul.name == "Kollaboratives Arbeiten":
            geladenes_modul = modul
            break

assert geladenes_modul is not None
assert geladenes_modul.status == ModulStatus.ABGESCHLOSSEN
assert geladenes_modul.pruefungsleistung.anerkannt is True
assert geladenes_modul.pruefungsleistung.note is None

testdatei.unlink()

print("Alle JSON-Tests erfolgreich.")