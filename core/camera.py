import cv2
import threading
import sys  # À ajouter en haut du fichier

class CameraManager:
    def __init__(self, camera_index=0, flip_horizontal=False, flip_vertical=False):
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        self.frame = None
        self.thread = None
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical
        self.lock = threading.Lock()  # Verrou pour protéger l'accès à la caméra

    def start_camera(self):
        """Démarre la capture vidéo en arrière-plan."""
        if self.running:
            print("La caméra est déjà en cours d'exécution.")
            return
        try:
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                raise Exception(f"Impossible d'ouvrir la caméra avec l'index {self.camera_index}.")
            # Définir la résolution de la caméra
            self.running = True
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            print("Caméra démarrée avec succès.")
        except Exception as e:
            print(f"Erreur lors du démarrage de la caméra : {e}")
            self.running = False
            sys.exit(1) # Ajouter pour quitter le programme en cas d'erreur connexion caméra

    def _capture_loop(self):
        """Boucle de capture vidéo."""
        while self.running:
            try:
                with self.lock:  # Protéger l'accès à la caméra
                    ret, frame = self.cap.read()
                    if not ret:
                        print("Erreur lors de la capture de la frame.")
                        continue
                    if self.flip_horizontal:
                        frame = cv2.flip(frame, 1)
                    if self.flip_vertical:
                        frame = cv2.flip(frame, 0)
                    self.frame = frame
            except Exception as e:
                print(f"Erreur dans la boucle de capture : {e}")
                break

    def get_frame(self):
        """Retourne la dernière image capturée."""
        with self.lock:  # Protéger l'accès à la frame
            return self.frame

    def stop_camera(self):
        """Arrête la caméra proprement."""
        self.running = False
        if self.thread:
            self.thread.join()  # Attendre la fin du thread
        with self.lock:  # Protéger l'accès à la caméra
            if self.cap:
                self.cap.release()
                self.cap = None
        print("Caméra arrêtée proprement.")

if __name__ == "__main__":
    camera_manager = CameraManager(camera_index=1, flip_horizontal=False, flip_vertical=True)
    camera_manager.start_camera()
    try:
        while True:
            frame = camera_manager.get_frame()
            if frame is not None:
                cv2.imshow("Camera Feed", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        camera_manager.stop_camera()
        cv2.destroyAllWindows()