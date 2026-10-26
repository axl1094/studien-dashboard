from pathlib import Path

from controller import StudienController
from dashboard import Dashboard

projektordner = Path(__file__).resolve().parent
datenpfad = projektordner / "studium.json"

controller = StudienController(datenpfad)

studium = controller.laden()

dashboard = Dashboard()
dashboard.anzeigen(studium, controller)