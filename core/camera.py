import cv2

class Camera:
    def __init__(self):
        self.cap = None  # Objet pour gérer la capture vidéo
        self.available_cams = []  # Liste des webcams disponibles

    def list_webcams(self):
        """Liste toutes les webcams connectées au PC."""
        self.available_cams = []
        for i in range(10):  # Test jusqu'à 10 webcams possibles
            temp_cap = cv2.VideoCapture(i)
            if temp_cap.isOpened():
                self.available_cams.append(i)
                temp_cap.release()
        return self.available_cams

    def connect_to_webcam(self, cam_index):
        """Connecte à la webcam spécifiée par son index."""
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(cam_index)
        if not self.cap.isOpened():
            raise ValueError(f"Impossible de se connecter à la webcam {cam_index}")

    def get_frame(self):
        """Récupère une image du flux vidéo."""
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("Aucune webcam connectée.")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Impossible de lire le flux vidéo.")
        return frame

    def show_live_feed(self):
        """Affiche le flux vidéo en direct (pour tester)."""
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("Aucune webcam connectée.")
        while True:
            frame = self.get_frame()
            cv2.imshow("Webcam Live Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Quitte avec la touche 'q'
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def release_webcam(self):
        """Libère la webcam."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
