import json
from datetime import date

from modelle import Studiengang, Modul, ModulStatus

class JsonSpeicher:

    def speichern(self, studiengang, dateiname):
        # Die Python-Objekte werden in eine JSON-kompatible Struktur umgewandelt.
        daten = {
            "name": studiengang.name,
            "zielabschluss": studiengang.zielabschluss.isoformat(),
            "zielnote": studiengang.zielnote,
            "gesamt_ects": studiengang.gesamt_ects,
            "semester": []
        }

        for semester in studiengang.semester:
            semester_daten = {
                "nummer": semester.nummer,
                "module": []
            }

            for modul in semester.module:
                modul_daten = {
                    "name": modul.name,
                    "ects": modul.ects,
                    "status": modul.status.value,
                    "note": modul.pruefungsleistung.note,
                    "anerkannt": modul.pruefungsleistung.anerkannt
                }

                semester_daten["module"].append(modul_daten)

            daten["semester"].append(semester_daten)

        with open(dateiname, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, ensure_ascii=False, indent=4)
    
    def laden(self, dateiname):
        with open(dateiname, "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        studiengang = Studiengang(
            daten["name"],
            date.fromisoformat(daten["zielabschluss"]),
            daten["zielnote"],
            daten["gesamt_ects"]
        )

        for semester_daten in daten["semester"]:
            semester = studiengang.erstelleSemester(semester_daten["nummer"])

            for modul_daten in semester_daten["module"]:
                modul = Modul(modul_daten["name"], modul_daten["ects"])

                modul.pruefungsleistung.note = modul_daten["note"]
                modul.pruefungsleistung.anerkannt = modul_daten.get("anerkannt", False)

                # Der gespeicherte Status wird über die vorgesehenen Modellmethoden wiederhergestellt.
                status = ModulStatus(modul_daten["status"])

                if status == ModulStatus.AKTIV:
                    modul.aktiviere()

                elif status == ModulStatus.ABGESCHLOSSEN:
                    modul.aktiviere()
                    modul.schliesseAb()

                semester.fuegeModulHinzu(modul)

        return studiengang
