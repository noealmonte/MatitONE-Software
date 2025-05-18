import cv2
import numpy as np
import threading
from core.camera import CameraManager # When using the main.py file
# from camera import CameraManager # When using the camera module directly

class TrackingManager:
    def __init__(self,camera_index=0, color_mode="IR", flip_horizontal=False, flip_vertical=False):
        """
        Initialise le tracking avec une caméra et un mode de couleur.
        color_mode : "IR" ou "JAUNE"
        """
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical
        self.camera_manager = CameraManager(camera_index, self.flip_horizontal , self.flip_vertical)  # Créer une instance de CameraManager
        self.camera_manager.start_camera()
        self.running = False
        self.thread = None
        self.last_position = None
        self.color_mode = color_mode  # Mode de couleur sélectionné
        # Thread pour le mode debug en parallèle (affichage en temps réel)
        self.debug_running = False
        self.debug_thread = None

    def start_tracking(self):
        """Lance le tracking en arrière-plan"""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._tracking_loop, daemon=True)
        self.thread.start()

    def _tracking_loop(self):
        """Boucle qui récupère les frames et détecte l’objet"""
        while self.running:
            #qprint("Tracking..")
            frame = self.camera_manager.get_frame()
            if frame is not None:
                self.last_position = self._process_frame(frame)
               # print(f"Last position: {self.last_position}")
  

    def _process_frame(self, frame):
        """Traitement pour détecter l’objet en fonction de la couleur sélectionnée"""
        if self.color_mode == "JAUNE":
            return self._track_yellow(frame)
           # return self._track_yellow_with_mask(frame)
        elif self.color_mode == "IR":
            return self._track_white(frame)
            #return self._track_IR(frame)
        else:
            print("Erreur : Mode de couleur non pris en charge.")
        return None
    
    def _track_yellow(self, frame):
        """Détection d’un objet jaune avec filtrage HSV"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        return self._find_largest_contour(mask)
    
    def _track_white(self, frame):
        """Détection d’un objet blanc avec filtrage HSV"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 25, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        return self._find_largest_contour(mask)
    
        
    def _find_largest_contour(self, binary_mask):
        """Trouve le plus grand contour et renvoie ses coordonnées"""
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            biggest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(biggest)
            return (x, y, w, h)
        return None

    def get_position(self):
        """Retourne la dernière position détectée"""
        return self.last_position

    def stop_tracking(self):
        """Arrête le tracking"""
        self.running = False
        self.camera_manager.stop_camera()


    def debug_display(self):
        self.debug_running = True
        while self.debug_running:
            frame = self.camera_manager.get_frame()
            if frame is not None:
                display_frame = frame.copy()
                if self.last_position:
                    x, y, w, h = self.last_position
                    cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(display_frame, f"Mode: {self.color_mode}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("Debug Tracking", display_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.debug_running = False
                break
        cv2.destroyAllWindows()
    
    def stop_debug(self):
        """Arrête le debug proprement"""
        self.debug_running = False


# A UTILISER POUR TESTER LE MODULE SANS LANCER LE PROGRAMME PRINCIPAL
if __name__ == "__main__":

    tracking_manager = TrackingManager(camera_index=1, color_mode="IR")
    tracking_manager.start_tracking()
    
    thread_debug = threading.Thread(target=tracking_manager.debug_display)
    thread_debug.start()

    try:
        while thread_debug.is_alive():
            position = tracking_manager.get_position()
            if position:
                print("Position mesurée:", position)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Arrêt manuel...")

    # Arrêt propre
    tracking_manager.stop_tracking()
    tracking_manager.debug_running = False
    thread_debug.join()
    cv2.destroyAllWindows()
    # tracking_manager = TrackingManager(camera_index=0, color_mode="JAUNE")
    # tracking_manager.start_tracking()
    # thread_debug = threading.Thread(target=tracking_manager.debug_display, daemon=True)
    # thread_debug.start()
    # # tracking_manager.debug_display()
    # active = True
    # while True:
    #     print("Position mesurée:", tracking_manager.get_position())
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # tracking_manager.stop_tracking()
    # tracking_manager.stop_debug()
    # cv2.destroyAllWindows()
    # thread_debug.join()
    # active = False
        