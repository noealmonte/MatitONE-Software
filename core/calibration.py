import threading
import time

class Calibration:
    def __init__(self):
        self.running = threading.Event()

    def start(self):
        """Démarre la calibration (peut être bloquante ou en thread)."""
        self.running.set()
        self.thread = threading.Thread(target=self._calibration_process, daemon=True)
        self.thread.start()

    def _calibration_process(self):
        print("Affichage des croix de calibration...")
        time.sleep(3)  # Simulation du processus de calibration
        print("Calibration terminée.")

    def stop(self):
        self.running.clear()
        self.thread.join()
