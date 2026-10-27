from enum import Enum
from datetime import date

class ModulStatus(Enum):
    OFFEN = "OFFEN"
    AKTIV = "AKTIV"
    ABGESCHLOSSEN = "ABGESCHLOSSEN"

class Pruefungsleistung:

    def __init__(self, note=None, anerkannt=False):
        self.note = note
        self.anerkannt = anerkannt

    @property
    def bestanden(self):
        # Anerkannte Prüfungsleistungen gelten auch ohne Note als bestanden.
        if self.anerkannt:
            return True

        return self.note is not None and 1.0 <= self.note <= 4.0

class Modul:

    def __init__(self, name, ects):
        self.name = name
        self.ects = ects
        self.status = ModulStatus.OFFEN
        self.__pruefungsleistung = Pruefungsleistung()

    @property
    def pruefungsleistung(self):
        return self.__pruefungsleistung

    def aktiviere(self):
        if self.status == ModulStatus.OFFEN:
            self.status = ModulStatus.AKTIV

    def deaktiviere(self):
        if self.status == ModulStatus.AKTIV:
            self.status = ModulStatus.OFFEN

    def schliesseAb(self):
        if self.status == ModulStatus.AKTIV and self.pruefungsleistung.bestanden:
            self.status = ModulStatus.ABGESCHLOSSEN

class Semester:

    def __init__(self, nummer):
        self.nummer = nummer
        self.module = []

    def fuegeModulHinzu(self, modul):
        self.module.append(modul)

class Studiengang:

    def __init__(self, name, zielabschluss, zielnote, gesamt_ects):
        self.name = name
        self.zielabschluss = zielabschluss
        self.zielnote = zielnote
        self.gesamt_ects = gesamt_ects
        self.semester = []

    def erstelleSemester(self, nummer):
        semester = Semester(nummer)
        self.semester.append(semester)
        return semester

    @property
    def ects_erreicht(self):
        summe = 0

        for semester in self.semester:
            for modul in semester.module:
                if modul.status == ModulStatus.ABGESCHLOSSEN:
                    summe += modul.ects

        return summe
    
    @property
    def anzahl_abgeschlossen(self):
        anzahl = 0

        for semester in self.semester:
            for modul in semester.module:
                if modul.status == ModulStatus.ABGESCHLOSSEN:
                    anzahl += 1

        return anzahl

    @property
    def anzahl_aktiv(self):
        anzahl = 0

        for semester in self.semester:
            for modul in semester.module:
                if modul.status == ModulStatus.AKTIV:
                    anzahl += 1

        return anzahl

    @property
    def anzahl_offen(self):
        anzahl = 0

        for semester in self.semester:
            for modul in semester.module:
                if modul.status == ModulStatus.OFFEN:
                    anzahl += 1

        return anzahl

    @property
    def aktuelle_note(self):
        gewichtete_summe = 0.0
        benotete_ects = 0

        #Für den Durchschnitt werden nur abgeschlossene und benotete Module berücksichtigt.
        for semester in self.semester:
            for modul in semester.module:
                if modul.status == ModulStatus.ABGESCHLOSSEN and modul.pruefungsleistung.note is not None:
                    gewichtete_summe += modul.pruefungsleistung.note * modul.ects
                    benotete_ects += modul.ects

        if benotete_ects == 0:
            return None

        return gewichtete_summe / benotete_ects

    @property
    def verbleibende_monate(self):
        heute = date.today()

        # Berechnung der verbleibenden Zeit bis zum geplanten Studienabschluss.
        monate = (self.zielabschluss.year - heute.year) * 12 + self.zielabschluss.month - heute.month

        if heute.day > self.zielabschluss.day:
            monate -= 1

        return max(monate, 0)