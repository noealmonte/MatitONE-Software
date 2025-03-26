import cv2
import threading
import queue

class Camera:
    def __init__(self, source=0):
        self.capture = cv2.VideoCapture(source)
        self.frame_queue = queue.Queue(maxsize=1)  # Stocke la dernière image
        self.running = threading.Event()

    def start(self):
        """Démarre la capture vidéo en continu sur un thread."""
        self.running.set()
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        print("Camera thread démarré.")

    def _capture_loop(self):
        while self.running.is_set():
            ret, frame = self.capture.read()
            if ret:
                if not self.frame_queue.empty():
                    self.frame_queue.get_nowait()  # Supprime l’ancienne image
                self.frame_queue.put(frame)
        #print("Arrêt de la capture vidéo.")


    def get_frame(self):
        """Récupère la dernière image capturée."""
        return self.frame_queue.get() if not self.frame_queue.empty() else None

    def stop(self):
        """Arrête la capture vidéo proprement."""
        self.running.clear()
        self.thread.join()
        self.capture.release()
        print("Camera thread arrêté.")
