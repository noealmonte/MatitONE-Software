import win32gui
import time

class SoftwareDetector:
    """
    Classe permettant de détecter en continu sur quel logiciel l'utilisateur se trouve
    parmi Microsoft Whiteboard et OneNote, en se basant sur le titre de la fenêtre active.
    """

    def __init__(self, check_interval=1.0):
        """
        Args:
            check_interval (float): Intervalle en secondes entre chaque vérification.
        """
        self.active_window_title = ""
        self.current_software = None
        self.check_interval = check_interval

    def update_active_window_title(self):
        """
        Met à jour le titre de la fenêtre active en utilisant win32gui.
        """
        try:
            window_handle = win32gui.GetForegroundWindow()
            self.active_window_title = win32gui.GetWindowText(window_handle)
            # print(f"Titre détecté : {self.active_window_title}")  # debug
        except Exception as e:
            self.active_window_title = ""
            print(f"Erreur lors de la récupération de la fenêtre active: {e}")

    def detect_software(self):
        """
        Retourne la chaîne correspondant au logiciel détecté parmi 'whiteboard' et 'onenote'.
        Si aucun des deux n'est détecté, retourne None.
        """
        self.update_active_window_title()
        title = self.active_window_title.lower() if self.active_window_title else ""
        if "whiteboard" in title:
            return "whiteboard"
        elif "onenote" in title:
            return "onenote"
        else:
            return None

    def run_detection_loop(self):
        """
        Exécute une boucle continue qui détecte le logiciel utilisé et affiche les changements.
        Appuyez sur Ctrl+C pour arrêter la boucle.
        """
        try:
            while True:
                detected = self.detect_software()
                if detected != self.current_software:
                    self.current_software = detected
                    if detected:
                        print(f"Logiciel détecté : {detected}")
                    else:
                        print("Aucun logiciel (Whiteboard ou OneNote) détecté.")
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("Interruption par l'utilisateur. Arrêt de la détection.")

# Exemple d'utilisation
if __name__ == "__main__":
    detector = SoftwareDetector(check_interval=1.0)
    detector.run_detection_loop()
