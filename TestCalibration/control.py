import time
import threading
import pyautogui  # Pour bouger la souris
# from core.tracking import TrackingManager # with main.py
# from core.testCalibrationHmgVideo import CalibrationManager
from tracking import TrackingManager  # with main.py
# from testCalibrationHmgVideo import CalibrationManager
from calibration_MatriceSave import CalibrationManager  # with main.py

class Control:
    def __init__(self):
        self.tracking = None
        self.calibration = None
        self.running = False
       
    def launch_tracking(self, camera_index=0, color_mode="JAUNE", flip_horizontal=False, flip_vertical=False):
        self.tracking = TrackingManager(camera_index, color_mode, flip_horizontal, flip_vertical)
        self.tracking.start_tracking()
        return self.tracking

    def start_control(self):
        print("Démarrage du contrôle...")
        return self.tracking

    def start_calibration(self, tracking):
        self.calibration = CalibrationManager(tracking_manager=tracking)
        # self.calibration = CalibrationManager(tracking, screen_size=(1920, 1080), screen_offset=(3840, 0))
        self.calibration.start_calibration()

        if self.calibration.calibrated:
            print("Calibration réussie. Lancement du suivi souris.")
            self.running = True
            mouse_thread = threading.Thread(target=self._follow_mouse, daemon=True)
            mouse_thread.start()
        else:
            print("Calibration échouée ou annulée.")

    # def _follow_mouse(self):
    #     """Bouge la souris selon la position transformée du suivi."""
    #     while self.running:
    #         pos = self.calibration.get_mouse_position()
    #         if pos:
    #             x, y = int(pos[0]), int(pos[1])
                
    #             pyautogui.moveTo(x, y, duration=0.05)  # Déplacement fluide
    #         time.sleep(0.01)  # Fréquence de mise à jour

    def _follow_mouse(self):
        """Bouge la souris selon la position transformée du suivi."""
        screen_width, screen_height = pyautogui.size()
        # print(f"Résolution de l'écran : {screen_width}x{screen_height}")
        while self.running:
            pos = self.calibration.get_mouse_position()
            if pos:
                x, y = int(pos[0]), int(pos[1])
                # Vérifie que les coordonnées sont valides
                if 0 <= x < screen_width and 0 <= y < screen_height:
                    pyautogui.moveTo(x, y, duration=0)  # Instantané (plus rapide)
                else:
                    print(f"Coordonnées invalides : ({x}, {y})")
            time.sleep(0.005)  # Mise à jour plus fréquente

    def stop_control(self):
        self.running = False
        if self.tracking:
            self.tracking.stop_tracking()
            self.tracking.stop_debug_display()
        print("Fin du programme")

    def connect_to_pen(self):
        # Logique de connexion au stylo
        print("Connexion au stylo...")
        # self.pen = PenManager()
        # self.pen.connect()


if __name__ == "__main__":
    control_app = Control()
    tracking = control_app.launch_tracking(camera_index=0, color_mode="JAUNE", flip_horizontal=True, flip_vertical=False)
    control_app.start_control()
    control_app.start_calibration(tracking)
    # mouse_thread = threading.Thread(target=control_app._follow_mouse, daemon=True)
    # mouse_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        control_app.stop_control()




# from tracking import TrackingManager
# # from core.tracking import TrackingManager
# from core.calibration import Calibration§
# #from tracking import TrackingManager # When using the control module directly
# import time
# import threading



# class Control:
#     def __init__(self):
#         pass
#         self.tracking = None
#         self.calibration = None


#     def lauch_tracking(self):
#         self.tracking = TrackingManager(camera_index=0,color_mode="JAUNE")
#         self.tracking.start_tracking()
#         return self.tracking
    
#     def start_control(self):
#         # self.tracking = TrackingManager(camera_index=0,color_mode="JAUNE")
#         # self.thread_tracking = threading.Thread(target=self.tracking.start_tracking, daemon=True)
#         # self.thread_tracking.start()
#         # calibration = Calibration(tracking_manager=self.tracking)
#         # self.tracking.start_tracking()
#         # self.tracking.debug_display()
#         print("Démarrage du controle...")
#         return self.tracking
        
#     def start_calibration(self, tracking):
#         calibration = Calibration(tracking_manager=tracking)
#         # Attendre la fin de la calibration
#         while not calibration.is_calibration_complete():
#             time.sleep(1)
        
#         # Une fois la calibration terminée, obtenir la matrice d'homographie
#         homography_matrix = calibration.get_homography_matrix()
#         print("Matrice d'Homographie calculée:", homography_matrix)

#         # self.point = self.tracking.get_last_position()
#         # mouse_coords = calibration.apply_homography(self.point)
#         # Appliquer l'homographie à un point détecté
#         point = (150, 200)  # Exemple de point à transformer
#         real_coords = calibration.apply_homography(point)
#         print(f"Point transformé : {real_coords}")

#     def stop_control(self):
#         self.tracking.stop_tracking()
#         self.tracking.stop_debug_display()
#         print("Fin du programme")   

    


# if __name__ == "__main__":
#     control_app = Control()
#     tracking = control_app.start_control()
#     control_app.start_calibration(tracking)

    




