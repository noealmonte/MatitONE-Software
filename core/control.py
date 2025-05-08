import time
import threading
import pyautogui  # Pour bouger la souris

from tracking import TrackingManager # with control.py
# from core.tracking import TrackingManager  # with main.py

from calibration import CalibrationManager  # with control.py
# from core.calibration import CalibrationManager  # with main.py

class Control:
    def __init__(self):
        self.tracking = None
        self.calibration = None
        self.running = False
        self.smooth_pos = None  # Position lissée pour le mouvement de la souris
       
    def launch_tracking(self, camera_index=0, color_mode="JAUNE", flip_horizontal=False, flip_vertical=False):
        self.tracking = TrackingManager(camera_index, color_mode, flip_horizontal, flip_vertical)
        self.tracking.start_tracking()
        return self.tracking

    def start_control(self):
        print("Démarrage du contrôle...")
        return self.tracking

    def start_calibration(self, tracking, screen_size):
        self.calibration = CalibrationManager(tracking_manager=tracking, screen_size=screen_size)
        if self.calibration.is_loaded == True:
            print("Calibration déjà effectuée.")
        else:
            self.calibration.start_calibration()
            
        if self.calibration.calibrated:
            print("Calibration réussie. Lancement du suivi souris.")
            self.running = True
            mouse_thread = threading.Thread(target=self._follow_mouse, daemon=True)
            mouse_thread.start()
        else:
            print("Calibration échouée ou annulée.")

    
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
            time.sleep(0.005) # 


    # Suivit avec lissage de la souris
    # def _follow_mouse(self):
    #     screen_width, screen_height = pyautogui.size()
    #     alpha = 0.2  # Coefficient de lissage (entre 0 et 1)
        
    #     while self.running:
    #         pos = self.calibration.get_mouse_position()
    #         if pos:
    #             x, y = int(pos[0]), int(pos[1])
    #             if 0 <= x < screen_width and 0 <= y < screen_height:
    #                 if self.smooth_pos is None:
    #                     self.smooth_pos = (x, y)
    #                 else:
    #                     old_x, old_y = self.smooth_pos
    #                     new_x = int(old_x + alpha * (x - old_x))
    #                     new_y = int(old_y + alpha * (y - old_y))
    #                     self.smooth_pos = (new_x, new_y)

    #                 pyautogui.moveTo(self.smooth_pos[0], self.smooth_pos[1], duration=0)
    #         # time.sleep(0.005)

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
    tracking = control_app.launch_tracking(camera_index=1, color_mode="IR", flip_horizontal=False, flip_vertical=True)
    control_app.start_control()
    control_app.start_calibration(tracking,screen_size = pyautogui.size())
   
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        control_app.stop_control()