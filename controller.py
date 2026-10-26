from json_speicher import JsonSpeicher
from modelle import ModulStatus

class StudienController:

    def __init__(self, dateiname):
        self.dateiname = dateiname
        self.speicher = JsonSpeicher()
        self.studiengang = None

    def laden(self):
        self.studiengang = self.speicher.laden(self.dateiname)

        return self.studiengang

    def speichern(self):
        if self.studiengang is not None:
            self.speicher.speichern(self.studiengang, self.dateiname)
    
    def finde_modul(self, modulname):
        if self.studiengang is None:
            return None
        
        for semester in self.studiengang.semester:
            for modul in semester.module:
                if modul.name == modulname:
                    return modul

        return None

    def aktiviere_modul(self, modulname):
        modul = self.finde_modul(modulname)

        if modul is None:
            return False
        
        alter_status = modul.status
        modul.aktiviere()

        if modul.status != alter_status:
            self.speichern()
            return True

        return False

    def deaktiviere_modul(self, modulname):
        modul = self.finde_modul(modulname)

        if modul is None:
            return False

        alter_status = modul.status
        modul.deaktiviere()

        if modul.status != alter_status:
            self.speichern()
            return True

        return False

    def setze_note(self, modulname, note):
        modul = self.finde_modul(modulname)

        if modul is None:
            return False
        
        if not 1.0 <= note <= 5.0:
            return False

        modul.pruefungsleistung.note = note
        self.speichern()

        return True

    def schliesse_modul_ab(self, modulname):
        modul = self.finde_modul(modulname)

        if modul is None:
            return False

        alter_status = modul.status
        modul.schliesseAb()

        if modul.status != alter_status and modul.status == ModulStatus.ABGESCHLOSSEN:
            self.speichern()
            return True

        return False