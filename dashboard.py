import streamlit as st
import plotly.express as px

from modelle import ModulStatus

class Dashboard:

    def anzeigen(self, studiengang, controller):
        st.set_page_config(page_title="Studien-Dashboard", layout="wide")
        
        st.title("Studien-Dashboard")
        st.subheader(studiengang.name)

        # Obere Kennzahlen
        spalte1, spalte2, spalte3, spalte4 = st.columns(4)

        gesamt_module = sum(len(semester.module) for semester in studiengang.semester)

        monatsname = {
            1: "Januar",
            2: "Februar",
            3: "März",
            4: "April",
            5: "Mai",
            6: "Juni",
            7: "Juli",
            8: "August",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Dezember"
        }

        with spalte1:
            st.subheader("Zielabschluss")

            zielmonat = monatsname[studiengang.zielabschluss.month]
            
            st.write(f"bis {zielmonat} {studiengang.zielabschluss.year}")
            st.write(f"noch {studiengang.verbleibende_monate} Monate")

        with spalte2:
            st.subheader("ECTS")

            st.metric("ECTS", f"{studiengang.ects_erreicht} / {studiengang.gesamt_ects}", label_visibility="collapsed")
            st.write("ECTS")

        with spalte3:
            st.subheader("Abgeschlossen")
            
            st.metric("Abgeschlossen", f"{studiengang.anzahl_abgeschlossen} / {gesamt_module}", label_visibility="collapsed")
            st.write("Module")

        with spalte4:
            st.subheader("Notenvergleich")

            notenspalte1, notenspalte2 = st.columns(2)

            with notenspalte1:
                st.write("Zielnote")

                zielnote = f"{studiengang.zielnote:.1f}".replace(".", ",")
                st.metric("Zielnote", zielnote, label_visibility="collapsed")

            with notenspalte2:
                st.write("Aktuelle Note")

                if studiengang.aktuelle_note is None:
                    aktuelle_note = "-"
                else:
                    aktuelle_note = (f"{studiengang.aktuelle_note:.2f}".replace(".", ","))

                st.metric("Aktuelle Note", aktuelle_note, label_visibility="collapsed")

        # Unterer Bereich
        linke_spalte, rechte_spalte = st.columns(2)

        with linke_spalte:
            st.subheader("Studienfortschritt")

            abgeschlossen = studiengang.anzahl_abgeschlossen
            nicht_abgeschlossen = studiengang.anzahl_aktiv + studiengang.anzahl_offen

            diagramm = px.pie(
                values=[abgeschlossen, nicht_abgeschlossen],
                names=[f"{abgeschlossen} abgeschlossen", f"{nicht_abgeschlossen} nicht abgeschlossen"],
                hole=0.6
            )

            fortschritt_prozent = abgeschlossen / gesamt_module * 100


            diagramm.update_traces(textinfo="none")

            diagramm.update_layout(
                annotations=[
                    dict(
                        text=f"<b>{fortschritt_prozent:.0f}%</b>", 
                        x=0.5, 
                        y=0.5, 
                        font_size=34, 
                        showarrow=False
                    )
                ],
            legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5))

            st.plotly_chart(diagramm, width="stretch")

        with rechte_spalte:
            st.subheader("Aktive Module")

            aktive_module = []

            for semester in studiengang.semester:
                for modul in semester.module:
                    if modul.status == ModulStatus.AKTIV:
                        aktive_module.append(modul.name)

            if aktive_module:
                for nummer, modulname in enumerate(aktive_module, start=1):
                    st.write(f"{nummer}. {modulname}")
            else:
                st.write("Keine aktiven Module")

            st.divider()

            status_spalte1, status_spalte2, status_spalte3 = st.columns(3)

            with status_spalte1:
                st.metric("Aktiv", studiengang.anzahl_aktiv)

            with status_spalte2:
                st.metric("Offen", studiengang.anzahl_offen)

            with status_spalte3:
                st.metric("Abgeschlossen", studiengang.anzahl_abgeschlossen)

        st.divider()
        st.subheader("Modul bearbeiten")

        modul_liste = []

        for semester in studiengang.semester:
            for modul in semester.module:
                modul_liste.append((f"Semester {semester.nummer}: {modul.name}", modul))
            
        if modul_liste:
            optionen = [eintrag[0] for eintrag in modul_liste]

            auswahl = st.selectbox("Modul auswählen", optionen)
        
            ausgewaehltes_modul = None

            for beschriftung, modul in modul_liste:
                if beschriftung == auswahl:
                    ausgewaehltes_modul = modul
                    break

            if ausgewaehltes_modul is not None:
                info1, info2, info3 = st.columns(3)

                with info1:
                    st.write("**Status:**", ausgewaehltes_modul.status.value)

                with info2:
                    st.write("**ECTS:**", ausgewaehltes_modul.ects)

                with info3:
                    if ausgewaehltes_modul.pruefungsleistung.anerkannt:
                        ergebnis = "Anerkannt"

                    elif ausgewaehltes_modul.pruefungsleistung.note is not None:
                        ergebnis = (f"{ausgewaehltes_modul.pruefungsleistung.note:.1f}".replace(".",","))

                    else:
                        ergebnis = "-"

                    st.write("**Ergebnis:**", ergebnis)

                if ausgewaehltes_modul.status == ModulStatus.OFFEN:
                    if st.button("Modul aktivieren"):
                        controller.aktiviere_modul(ausgewaehltes_modul.name)

                        st.success("Modul wurde aktiviert.")
                        st.rerun()
            
                elif ausgewaehltes_modul.status == ModulStatus.AKTIV:
                    if st.button("Modul deaktivieren"):
                        controller.deaktiviere_modul(ausgewaehltes_modul.name)

                        st.success("Modul wurde deaktiviert.")
                        st.rerun()

                    note = st.number_input(
                        "Note eingeben", 
                        min_value=1.0, 
                        max_value=5.0, 
                        step=0.1, 
                        value=( ausgewaehltes_modul.pruefungsleistung.note if ausgewaehltes_modul.pruefungsleistung.note is not None else 1.0)
                    )

                    button1, button2 = st.columns(2)

                    with button1:
                        if st.button("Note speichern"):
                            erfolg = controller.setze_note(ausgewaehltes_modul.name, note)

                            if erfolg:
                                st.success("Note wurde gespeichert.")
                                st.rerun()

                    with button2:
                        if st.button("Modul abschließen"):
                            erfolg = controller.schliesse_modul_ab(ausgewaehltes_modul.name)

                            if erfolg:
                                st.success("Modul wurde abgeschlossen.")
                                st.rerun()
                            else:
                                st.error( 
                                    "Das Modul kann nicht abgeschlossen werden. "
                                    "Bitte prüfe, ob eine bestandene Note eingetragen wurde"
                                )
                elif ausgewaehltes_modul.status == ModulStatus.ABGESCHLOSSEN:
                    st.info("Dieses Modul ist bereits abgeschlossen.")
