import cv2

class Camera:
    """
    Classe pour gérer le flux vidéo d'une webcam.

    Attributes:
        camera_id (int): ID de la webcam (0 par défaut pour la caméra principale).
        cap (cv2.VideoCapture): Instance d'OpenCV pour capturer le flux vidéo.
    """

    def __init__(self, camera_id=0):
        """
        Initialise la caméra.

        Args:
            camera_id (int): ID de la caméra. Par défaut, 0 pour la caméra principale.
        """
        self.camera_id = camera_id
        self.cap = None

    def start(self):
        """
        Démarre le flux vidéo de la webcam.
        """
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise Exception(f"Impossible d'ouvrir la caméra avec l'ID {self.camera_id}")
        print("Caméra démarrée.")

    def get_frame(self):
        """
        Capture une frame actuelle depuis la webcam.

        Returns:
            frame (numpy.ndarray): L'image capturée en tant que tableau NumPy.
        """
        if self.cap is None or not self.cap.isOpened():
            raise Exception("La caméra n'est pas démarrée.")
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Impossible de lire la frame de la webcam.")
        return frame

    def capture_image(self, filename="capture.jpg"):
        """
        Capture et enregistre une image depuis la webcam.

        Args:
            filename (str): Le nom du fichier où enregistrer l'image.
        """
        frame = self.get_frame()
        cv2.imwrite(filename, frame)
        print(f"Image capturée et enregistrée sous '{filename}'.")

    def stop(self):
        """
        Arrête le flux vidéo et libère la webcam.
        """
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        print("Caméra arrêtée.")

    def __del__(self):
        """
        Assure que la caméra est libérée à la destruction de l'objet.
        """
        self.stop()
