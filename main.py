import time
from core.control import Control 
from gui.gui import MainGUI
import threading

def main():
    # Logique principale
    print("Démarrage de l'application...")
    # Création des instances de GUI et de Control
    control_app = Control()
    app = MainGUI(control_app)     
    app.run()

if __name__ == "__main__":
    main()