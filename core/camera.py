import cv2
import threading

class CameraManager:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        self.frame = None
        self.thread = None

    def start_camera(self):
        """Démarre la capture vidéo en arrière-plan"""
        if self.running:
            return  
        self.running = True
        self.cap = cv2.VideoCapture(self.camera_index)
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):
        """Boucle de capture vidéo"""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame  

    def get_frame(self):
        """Retourne la dernière image capturée"""
        return self.frame

    def stop_camera(self):
        """Arrête la caméra proprement"""
        self.running = False
        if self.cap:
            self.cap.release()
        self.cap = None
        # arrêter le thread ? a revoir avec prof
