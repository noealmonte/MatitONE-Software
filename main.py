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

    # control_thread = threading.Thread(target=control_app.start_control, daemon=True)
    # control_thread.start()         
    app.run()

#     app.sample_button.config(command=stop_control)


# def stop_control():
#     """Arrête le contrôle."""
#     print("Arrêt du contrôle")


    #control_app.stop_control()

if __name__ == "__main__":
    main()