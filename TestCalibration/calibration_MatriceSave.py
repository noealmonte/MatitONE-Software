#VERSION FONCTIONNELLE SANS PROJECTION SUR L'ECRAN, A GARDER
import cv2
import numpy as np
import threading
import os
# from core.tracking import TrackingManager  # ou depuis core.tracking si appelé depuis main
from tracking import TrackingManager  # ou depuis core.tracking si appelé depuis main

class CalibrationManager:
    def __init__(self, tracking_manager, screen_size=(3840, 2400)):
        self.tracking_manager = tracking_manager
        delta = 50 # zone de détection en pixels
        self.screen_points = [
            (0+delta, 0+delta),
            (screen_size[0]-delta, 0+delta),
            (screen_size[0]-delta, screen_size[1]-delta),
            (0+delta, screen_size[1]-delta)
        ]
        # self.screen_points = [
        #     (0, 0),
        #     (screen_size[0], 0),
        #     (screen_size[0], screen_size[1]),
        #     (0, screen_size[1])
        # ]
        self.camera_points = []
        self.homography = None
        self.calibrated = False
        self.calibration_path = "calibration_data/homography.npy"

        # Charger l'homographie existante si elle existe
        self._ensure_data_folder()
        self.load_homography()

    def _ensure_data_folder(self):
        os.makedirs(os.path.dirname(self.calibration_path), exist_ok=True)


    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_clicked = True

    def start_calibration(self):
        print("Calibration en cours... Suivez les instructions.")
        self.tracking_manager.start_tracking()
        self.mouse_clicked = False
        idx = 0

        while idx < len(self.screen_points):
            frame = self.tracking_manager.camera_manager.get_frame()
            pos = self.tracking_manager.get_position()

            if frame is not None:
                display = frame.copy()
                h, w, _ = frame.shape
                # print("h et w",h, w)

                # Affichage des points cibles
                for i, pt in enumerate(self.screen_points):
                    color = (0, 255, 0) if i == idx else (100, 100, 100)
                    # cv2.circle(display, (int(pt[0] * w / 1920), int(pt[1] * h / 1080)), 10, color, -1)
                    cv2.circle(display, (int(pt[0] * w / self.screen_points[2][0]), int(pt[1] * h / self.screen_points[2][1])), 10, color, -1)


                # Affichage de la position détectée
                if pos:
                    x, y, w_rect, h_rect = pos
                    center = (x + w_rect // 2, y + h_rect // 2)
                    cv2.circle(display, center, 5, (0, 0, 255), -1)

                cv2.putText(display, f"Point {idx + 1}/4 - Appuyez sur Espace", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.imshow("Calibration", display)
                cv2.setMouseCallback("Calibration", self._mouse_callback)

                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    print("Calibration annulée.")
                    break
                elif (key == 32 or self.mouse_clicked) and pos:
                    center = (pos[0] + pos[2] // 2, pos[1] + pos[3] // 2)
                    self.camera_points.append(center)
                    print(f"Point {idx+1} enregistré à {center}")
                    idx += 1
                    self.mouse_clicked = False

        cv2.destroyWindow("Calibration")

        if len(self.camera_points) == 4:
            self._compute_homography()
            self._save_homography()
            self.calibrated = True
            print("Calibration réussie.")
        else:
            print("Calibration incomplète.")

    def _compute_homography(self):
        camera_pts = np.array(self.camera_points, dtype=np.float32)
        screen_pts = np.array(self.screen_points, dtype=np.float32)
        self.homography, _ = cv2.findHomography(camera_pts, screen_pts)

    def _save_homography(self):
        if self.homography is not None:
            np.save(self.calibration_path, self.homography)
            print(f"Homographie sauvegardée dans '{self.calibration_path}'")

    # Si matrice existante, ne calibre pas
    def load_homography(self):
        if os.path.exists(self.calibration_path):
            self.homography = np.load(self.calibration_path)
            self.calibrated = True
            self.tracking_manager.start_tracking()
            print(f"Homographie chargée depuis '{self.calibration_path}'")
            return True
        print("Aucune homographie trouvée.")
        return False

    def get_mouse_position(self):
        if not self.calibrated or self.homography is None:
            return None

        pos = self.tracking_manager.get_position()
        if pos is None:
            # print("ici")
            return None

        # # Affichage de la position trackée pour le débogage
        # frame = self.tracking_manager.camera_manager.get_frame()
        # if frame is not None:
        #     display_frame = frame.copy()
        #     if pos:
        #         x, y, w, h = pos
        #         cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     cv2.putText(display_frame, f"Mode:Jaune", (10, 30),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        #     cv2.imshow("Debug Tracking", display_frame)
        # #---------------------------------


        center = np.array([[pos[0] + pos[2] // 2, pos[1] + pos[3] // 2]], dtype=np.float32)
        center = np.array([center])
        transformed = cv2.perspectiveTransform(center, self.homography)
        return tuple(transformed[0][0])
    
    
# Exemple d'utilisation en dehors
if __name__ == "__main__":
    tracker = TrackingManager(camera_index=0, color_mode="JAUNE", flip_horizontal=True, flip_vertical=False)
    calibration = CalibrationManager(tracker)

    if not calibration.calibrated:
        calibration.start_calibration()

    while calibration.calibrated:
        pos = calibration.get_mouse_position()   
        if pos:
            print("Position souris :", pos)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    tracker.stop_tracking()
    
