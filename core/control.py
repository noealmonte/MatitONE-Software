import time
import threading
import pyautogui  # Pour bouger la souris
import pynput  # Pour lire les entrées clavier
from pynput.mouse import Button

from .tracking import TrackingManager  # with control.py
# from core.tracking import TrackingManager  # with main.py

# from calibration_copy_2 import CalibrationManager  # with control.py
from .calibration import CalibrationManager  # with control.py
# from core.calibration import CalibrationManager  # with main.py

from .pen_logic import PenLogic  # with control.py
# from core.pen_logic import PenLogic  # with main.py


class Control:
    def __init__(self, tracking_manager: TrackingManager):
        self.tracking = tracking_manager
        self.calibration = CalibrationManager(
            tracking_manager=self.tracking, screen_size=pyautogui.size())
        self.pen_logic = None  # <- Ajoute ça pour le stylo
        self.running = False
        self.smooth_pos = None
        self.mouse = pynput.mouse.Controller()

    def launch_tracking(self):
        self.tracking.start_tracking()

    def start_calibration(self, screen_size=pyautogui.size()):
        if self.calibration is None:
            self.calibration = CalibrationManager(
                tracking_manager=tracking, screen_size=pyautogui.size())
        else:
            self.calibration.set_screen_size(screen_size)
        if self.calibration.is_loaded:
            print("Calibration déjà effectuée.")
        else:
            self.calibration.start_calibration()

        if self.calibration.calibrated:
            print("Calibration réussie. Lancement du suivi souris.")
            self.running = True
            # print("pen logic calibrated:", self.pen_logic.calibrated)
            # self.pen_logic.set_calibrated(True)
            mouse_thread = threading.Thread(
                target=self._follow_mouse, daemon=True)
            mouse_thread.start()
        else:
            print("Calibration échouée ou annulée.")

    def delete_calibration(self):
        if self.calibration is None:
            print("No Calibration was found")
            return
        if self.calibration.is_loaded:
            print("Previous Calibration was deleted")
            self.calibration.is_loaded = False
        else:
            print("No Calibration was found to delete")

    def _follow_mouse(self):
        screen_width, screen_height = pyautogui.size()
        drawing = False
        print("iCI follow mouse")
        
        while self.running:
            pos = self.calibration.get_mouse_position()
            # print("Position du stylo :", pos)
            if pos:
                x, y = int(pos[0]), int(pos[1])
                # print("screen size:", screen_width, screen_height)
                if 0 <= x < screen_width and 0 <= y < screen_height:
                    self.mouse.position = (x, y)
                    # print("→ Mouse position set to:", (x, y))

                    if self.pen_logic and self.pen_logic.get_current_software() == "whiteboard":
                        if not drawing:
                            print("→ Pressing mouse button")
                            self.mouse.press(Button.left)
                            drawing = True
                else:
                    if self.pen_logic and self.pen_logic.get_current_software() == "whiteboard":
                        if drawing:
                            print("→ Releasing mouse button (out of bounds)")
                            self.mouse.release(Button.left)
                            drawing = False
            else:
                if drawing:
                    print("→ Releasing mouse button (no tracking)")
                    self.mouse.release(Button.left)
                    drawing = False

            time.sleep(0.001)

    # def _follow_mouse(self):
    #     screen_width, screen_height = pyautogui.size()
    #     while self.running:
    #         pos = self.calibration.get_mouse_position()
    #         if pos:
    #             x, y = int(pos[0]), int(pos[1])
    #             if 0 <= x < screen_width and 0 <= y < screen_height:
    #                 # pyautogui.moveTo(x, y, duration=0)
    #                 self.mouse.position = (x, y)
    #                 #pyautogui.click()
    #                 self.mouse.press(Button.left)
    #                 time.sleep(0.1)  # Maintient le clic pendant 0.1 seconde
    #                 self.mouse.release(Button.left)

    #             else:
    #                 print(f"Coordonnées invalides : ({x}, {y})")
    #         #time.sleep(0.005)

    # def _follow_mouse(self):
    #     screen_width, screen_height = pyautogui.size()
    #     drawing = True  # Suivi de l'état du "clic"

    #     while self.running:
    #         pos = self.calibration.get_mouse_position()
    #         if pos:
    #             x, y = int(pos[0]), int(pos[1])
    #             if 0 <= x < screen_width and 0 <= y < screen_height:
    #                 self.mouse.position = (x, y)

    #                 if not drawing:
    #                     self.mouse.press(Button.left)
    #                     drawing = True

    #             else:
    #                 print(f"Coordonnées invalides : ({x}, {y})")
    #                 if drawing:
    #                     self.mouse.release(Button.left)
    #                     drawing = False
    #         else:
    #             if drawing:
    #                 self.mouse.release(Button.left)
    #                 drawing = False

    #         time.sleep(0.005)  # Évite d'inonder le système d'événements

    def connect_to_pen(self):
        print("Connexion au stylo...")
        self.pen_logic = PenLogic()
        self.pen_logic.start()  # Démarre la connexion et le thread de détection

    def stop_control(self):
        self.running = False
        if self.tracking:
            self.tracking.stop_tracking()
            # self.tracking.stop_debug_display()

        if self.pen_logic:
            self.pen_logic.stop()  # Très important d'arrêter proprement
            print("Stylo arrêté.")

        print("Fin du programme")


if __name__ == "__main__":

    control_app = Control()

    # Lancer tracking + calibration
    tracking = control_app.launch_tracking(
        camera_index=0, color_mode="JAUNE", flip_horizontal=True, flip_vertical=False)
    control_app.start_control()
    control_app.start_calibration(tracking, screen_size=pyautogui.size())

    # Lancer la connexion au stylo BLE
    control_app.connect_to_pen()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        control_app.stop_control()
