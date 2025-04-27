import threading
import time
from pen import Pen
from softwareDetector import SoftwareDetector  # <- On importe ton détecteur

class PenLogic:
    """Gère la logique du stylo en fonction des événements reçus et du logiciel utilisé."""

    def __init__(self):
        self.pen = Pen()
        self.pen.set_data_callback(self.handle_data)

        self.software_detector = SoftwareDetector(check_interval=1.0)
        self.current_software = None
        self.running = False

    def start(self):
        """Démarre la connexion au stylo et la détection du logiciel."""
        self.pen.connect()
        self.running = True

        # Démarre un thread pour détecter en continu l'application active
        self.software_thread = threading.Thread(target=self._software_detection_loop, daemon=True)
        self.software_thread.start()

    def stop(self):
        """Arrête la connexion au stylo."""
        self.running = False
        self.pen.stop_listening()

    def _software_detection_loop(self):
        """Boucle de détection continue du logiciel actif."""
        while self.running:
            detected = self.software_detector.detect_software()
            if detected != self.current_software:
                self.current_software = detected
                if detected:
                    print(f"🖥️ Logiciel détecté : {detected}")
                else:
                    print("🖥️ Aucun logiciel reconnu (Whiteboard ou OneNote)")
            time.sleep(self.software_detector.check_interval)

    def handle_data(self, message: str):
        """Traite les messages reçus du stylo BLE."""
        print(f"🖋️ Nouveau message reçu: {message}")

        if message == "Salut":
            self.handle_switch1()
        elif message == "S2":
            self.handle_switch2()
        # Ajoute ici d'autres cas si besoin

    def handle_switch1(self):
        """Action pour Switch 1 en fonction du logiciel détecté."""
        if self.current_software == "whiteboard":
            print("✏️ Switch 1: Action spéciale pour Whiteboard")
            # Implémente ici une action spécifique
        elif self.current_software == "onenote":
            print("📝 Switch 1: Action spéciale pour OneNote")
            # Implémente ici une action spécifique
        else:
            print("🔄 Switch 1: Action générique (aucun logiciel spécifique)")

    def handle_switch2(self):
        """Action pour Switch 2 en fonction du logiciel détecté."""
        if self.current_software == "whiteboard":
            print("✏️ Switch 2: Action secondaire pour Whiteboard")
        elif self.current_software == "onenote":
            print("📝 Switch 2: Action secondaire pour OneNote")
        else:
            print("🔄 Switch 2: Action générique (aucun logiciel spécifique)")


if __name__ == "__main__":
    logic = PenLogic()
    logic.start()

    try:
        print("⌛ Test de la logique du stylo en cours... Ctrl+C pour arrêter.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Arrêt demandé par l'utilisateur.")
        logic.stop()
















# # core/pen_logic.py

# from softwareDetector import SoftwareDetector  # si tu as une classe SoftwareDetector existante

# class PenLogic:
#     """Gère les actions à effectuer en fonction des données du stylo et de l'application active."""

#     def __init__(self, pen):
#         """
#         Args:
#             pen (Pen): Instance de la classe Pen.
#         """
#         self.pen = pen
#         self.pen.set_data_callback(self.handle_pen_data)  # Connecte le parsing automatique
#         self.software_detector = SoftwareDetector(check_interval=1.0)
#         self.current_software = None

#     def handle_pen_data(self, data: str):
#         """Traite la donnée reçue du stylo."""
#         self.current_software = self.software_detector.detect_software()

#         if self.current_software == "whiteboard":
#             self._handle_whiteboard(data)
#         elif self.current_software == "onenote":
#             self._handle_onenote(data)
#         else:
#             self._handle_other_apps(data)

#     def _handle_whiteboard(self, data: str):
#         """Logique pour Microsoft Whiteboard."""
#         print(f"[Whiteboard] Action pour {data}")
#         if data == "S1":
#             print("Action spéciale Whiteboard : Click S1")

#     def _handle_onenote(self, data: str):
#         """Logique pour Microsoft OneNote."""
#         print(f"[OneNote] Action pour {data}")
#         if data == "S1":
#             print("Action spéciale OneNote : Click S1")

#     def _handle_other_apps(self, data: str):
#         """Logique pour les autres applications."""
#         print(f"[Autre App] Action générique pour {data}")

#     def start(self):
#         """Méthode pour démarrer la détection si besoin."""
#         print("Démarrage de la logique du stylo.")
#         self.pen.start_listening()

#     def stop(self):
#         """Méthode pour arrêter proprement."""
#         print("Arrêt de la logique du stylo.")
#         self.pen.stop_listening()



# if __name__ == "__main__":
#     from pen import Pen  # pour que le test soit autonome

#     # --- Paramètres à adapter ---
#     COM_PORT = "COM5"  # 🔥 MET TON PORT ici (Windows: "COMx" / Linux: "/dev/ttySx")
#     BAUD_RATE = 9600   # Celui que tu as programmé dans ton Arduino (classique: 9600)

#     try:
#         # Créer le stylo et la logique
#         pen = Pen(port=COM_PORT, baudrate=BAUD_RATE)
#         pen.connect()

#         pen_logic = PenLogic(pen)
#         pen_logic.start()

#         print("Test en cours... Ctrl+C pour arrêter.")
#         while True:
#             pass  # Boucle infinie pour laisser tourner (car tout est dans des threads)

#     except KeyboardInterrupt:
#         print("Interruption par l'utilisateur.")
#         pen_logic.stop()