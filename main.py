import time
from core.control import Control
from core.tracking import TrackingManager
from gui.gui import MainGUI
import threading


def main():
    # Logique principale
    print("Démarrage de l'application...")
    # Création des instances de GUI et de Control
    tracker = TrackingManager(camera_index=1,color_mode="IR", flip_horizontal=True, flip_vertical=True)
    control_app = Control(tracker)
    guiapp = MainGUI(control_app)
    guiapp.run()


if __name__ == "__main__":
    main()
