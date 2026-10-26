from modelle import Modul, ModulStatus

modul1 = Modul("Mathematik: Analysis", 5)
modul1.aktiviere()
modul1.pruefungsleistung.note = 2.0
modul1.schliesseAb()

assert modul1.status == ModulStatus.ABGESCHLOSSEN

modul2 = Modul("Einführung in Computer Vision", 5)
modul2.aktiviere()
modul2.pruefungsleistung.note = 5.0
modul2.schliesseAb()

assert modul2.status == ModulStatus.AKTIV

anerkanntes_modul = Modul("Kollaboratives Arbeiten", 5)

anerkanntes_modul.aktiviere()
anerkanntes_modul.pruefungsleistung.anerkannt = True
anerkanntes_modul.schliesseAb()

assert anerkanntes_modul.status == ModulStatus.ABGESCHLOSSEN
assert anerkanntes_modul.pruefungsleistung.note is None
assert anerkanntes_modul.pruefungsleistung.anerkannt is True

print("Alle Modelltests erfolgreich.")
