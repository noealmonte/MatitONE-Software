from core.control import Control
from gui.gui import MainGUI

def main():
    """Démarre l'application principale."""
    print("Démarrage de l'application...")
    control_app = Control()  # Instance de contrôle
    gui_app = MainGUI(control_app)  # Passage de l'instance à la GUI
    gui_app.run()

if __name__ == "__main__":
    main()