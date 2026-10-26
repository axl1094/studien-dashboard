from datetime import date
from pathlib import Path

from modelle import Studiengang, Modul, ModulStatus
from json_speicher import JsonSpeicher

studium = Studiengang("Angewandte Künstliche Intelligenz", date(2028, 4, 30), 2.0, 180)

def fuege_modul_hinzu(semester, name, ects, status=ModulStatus.OFFEN, note=None, anerkannt=False):

    modul = Modul(name, ects)

    if status == ModulStatus.AKTIV:
        modul.aktiviere()

    elif status == ModulStatus.ABGESCHLOSSEN:
        modul.aktiviere()
        modul.pruefungsleistung.note = note
        modul.pruefungsleistung.anerkannt = anerkannt
        modul.schliesseAb()

    semester.fuegeModulHinzu(modul)

semester1 = studium.erstelleSemester(1)

fuege_modul_hinzu(semester1, "Artificial Intelligence", 5, ModulStatus.ABGESCHLOSSEN, 2.0)
fuege_modul_hinzu(semester1, "Einführung in das wissenschaftliche Arbeiten für IT und Technik", 5, ModulStatus.ABGESCHLOSSEN, 2.0)
fuege_modul_hinzu(semester1, "Einführung in die Programmierung mit Python", 5, ModulStatus.ABGESCHLOSSEN, 2.3)
fuege_modul_hinzu(semester1, "Mathematik: Analysis", 5, ModulStatus.AKTIV)
fuege_modul_hinzu(semester1, "Kollaboratives Arbeiten", 5, ModulStatus.ABGESCHLOSSEN, anerkannt=True)
fuege_modul_hinzu(semester1, "Statistik - Wahrscheinlichkeit und deskriptive Statistik", 5, ModulStatus.AKTIV)

semester2 = studium.erstelleSemester(2)

fuege_modul_hinzu(semester2, "Projekt: Objektorientierte und funktionale Programmierung mit Python", 5, ModulStatus.AKTIV)
fuege_modul_hinzu(semester2, "Mathematik: Lineare Algebra", 5)
fuege_modul_hinzu(semester2, "Interkulturelle und ethische Handlungskompetenzen", 5, ModulStatus.ABGESCHLOSSEN, 2.7)
fuege_modul_hinzu(semester2, "Statistik - Induktive Statistik", 5)
fuege_modul_hinzu(semester2, "Projekt: Cloud Programming", 5)
fuege_modul_hinzu(semester2, "Cloud Computing", 5, ModulStatus.ABGESCHLOSSEN, 2.7)

semester3 = studium.erstelleSemester(3)

fuege_modul_hinzu(semester3, "Maschinelles Lernen - Supervised Learning", 5)
fuege_modul_hinzu(semester3, "Maschinelles Lernen - Unsupervised Learning und Feature Engineering", 5)
fuege_modul_hinzu(semester3, "Einführung in Computer Vision", 5, ModulStatus.AKTIV)
fuege_modul_hinzu(semester3, "Einführung in das Reinforcement Learning", 5)
fuege_modul_hinzu(semester3, "Projekt: Computer Vision", 5)
fuege_modul_hinzu(semester3, "Neuronale Netze und Deep Learning", 5)

semester4 = studium.erstelleSemester(4)

fuege_modul_hinzu(semester4, "Einführung in NLP", 5)
fuege_modul_hinzu(semester4, "Projekt: NLP", 5)
fuege_modul_hinzu(semester4, "Data Science Software Engineering", 5)
fuege_modul_hinzu(semester4, "Projekt: Vom Modell zum Produktvertrieb", 5)
fuege_modul_hinzu(semester4, "Einführung in Datenschutz und IT-Sicherheit", 5)
fuege_modul_hinzu(semester4, "Seminar: Ethische Fragen der Data Science", 5)

semester5 = studium.erstelleSemester(5)

fuege_modul_hinzu(semester5, "UX-Projekt", 5)
fuege_modul_hinzu(semester5, "Projekt: Edge AI", 5)
fuege_modul_hinzu(semester5, "Einführung in die Robotik", 5)
fuege_modul_hinzu(semester5, "Projekt: Agiles Projektmanagement", 5)
fuege_modul_hinzu(semester5, "User Experience", 5)

semester6 = studium.erstelleSemester(6)

fuege_modul_hinzu(semester6, "Bachelorarbeit", 10)
fuege_modul_hinzu(semester6, "Wahlpflichtbereich - noch nicht gewählt", 25)

projektordner = Path(__file__).resolve().parent
datenpfad = projektordner / "studium.json"

speicher = JsonSpeicher()
speicher.speichern(studium, datenpfad)

print("studium.json wurde erstellt.")
print("ECTS erreicht:", studium.ects_erreicht)
print("Abgeschlossen:", studium.anzahl_abgeschlossen)
print("Aktiv:", studium.anzahl_aktiv)
print("Offen:", studium.anzahl_offen)
print("Aktuelle Note:", studium.aktuelle_note)
