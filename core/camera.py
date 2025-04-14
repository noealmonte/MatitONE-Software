import cv2
import threading

class CameraManager:
    def __init__(self, camera_index=0,flip_horizontal=False , flip_vertical =False):
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        self.frame = None
        self.thread = None
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical

    def start_camera(self):
        """Démarre la capture vidéo en arrière-plan"""
        if self.running:
            return  
        self.running = True
        self.cap = cv2.VideoCapture(self.camera_index,cv2.CAP_DSHOW) # enlever CAP_DSHOW si besoin
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        # self._capture_loop()

    def _capture_loop(self):
        """Boucle de capture vidéo"""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if self.flip_horizontal:
                    frame = cv2.flip(frame, 1)  # effet miroir horizontal
                if self.flip_vertical:
                    frame = cv2.flip(frame, 0)
                self.frame = frame
                print("Frame capturée par caméra\n") 

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



if __name__ == "__main__":
    camera_manager = CameraManager(camera_index=1, flip_horizontal=False)  # Changez l'index de la caméra si nécessaire
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