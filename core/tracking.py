import threading
import time

class Tracking:
    def __init__(self, camera):
        self.camera = camera
        self.running = threading.Event()
        self.position = None  # Stocke la dernière position détectée

    def start(self):
        """Démarre le tracking sur un thread séparé."""
        self.running.set()
        self.thread = threading.Thread(target=self._tracking_loop, daemon=True)
        self.thread.start()
        print("Tracking thread démarré.")

    def _tracking_loop(self):
        while self.running.is_set():
            frame = self.camera.get_frame()
            if frame is not None:
                self.position = self._process_frame(frame)
            time.sleep(0.01)  # Petit délai pour éviter d'utiliser 100% du CPU

    def _process_frame(self, frame):
        """Simule la détection de la LED IR (à implémenter avec OpenCV)."""

        return (100, 200)  # Exemple de coordonnées

    def get_position(self):
        return self.position

    def stop(self):
        """Arrête le tracking proprement."""
        self.running.clear()
        self.thread.join()
        print("Tracking thread arrêté.")
