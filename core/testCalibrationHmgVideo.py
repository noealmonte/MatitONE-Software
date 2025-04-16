# import cv2
# import numpy as np
# import threading
# from tracking import TrackingManager  # ou depuis core.tracking si appelé depuis main

# class CalibrationManager:
#     def __init__(self, tracking_manager, screen_size=(1920, 1080), margin_ratio=0.05):
#         self.tracking_manager = tracking_manager
#         self.screen_size = screen_size
#         self.margin_ratio = margin_ratio

#         w, h = screen_size
#         mx, my = int(w * margin_ratio), int(h * margin_ratio)

#         self.screen_points = [
#             (mx, my),               # coin haut gauche
#             (w - mx, my),           # coin haut droit
#             (w - mx, h - my),       # coin bas droit
#             (mx, h - my)            # coin bas gauche
#         ]

#         self.camera_points = []
#         self.homography = None
#         self.calibrated = False

#     def start_calibration(self):
#         print("Calibration en cours... Suivez les instructions.")
#         self.tracking_manager.start_tracking()
#         idx = 0

#         while idx < len(self.screen_points):
#             frame = self.tracking_manager.camera_manager.get_frame()
#             pos = self.tracking_manager.get_position()

#             if frame is not None:
#                 display = frame.copy()
#                 h, w, _ = frame.shape
#                 ref_w, ref_h = self.screen_size
#                 scale_x = w / ref_w
#                 scale_y = h / ref_h

#                 # Affichage des points cibles avec échelle adaptée
#                 for i, pt in enumerate(self.screen_points):
#                     color = (0, 255, 0) if i == idx else (100, 100, 100)
#                     disp_x = int(pt[0] * scale_x)
#                     disp_y = int(pt[1] * scale_y)
#                     cv2.circle(display, (disp_x, disp_y), 10, color, -1)

#                 # Affichage de la position détectée
#                 if pos:
#                     x, y, w_rect, h_rect = pos
#                     center = (x + w_rect // 2, y + h_rect // 2)
#                     cv2.circle(display, center, 5, (0, 0, 255), -1)

#                 cv2.putText(display, f"Point {idx + 1}/4 - Appuyez sur Espace", (10, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

#                 cv2.imshow("Calibration", display)

#                 key = cv2.waitKey(1) & 0xFF
#                 if key == 27:  # ESC
#                     print("Calibration annulée.")
#                     break
#                 elif key == 32 and pos:  # Espace
#                     center = (pos[0] + pos[2] // 2, pos[1] + pos[3] // 2)
#                     self.camera_points.append(center)
#                     print(f"Point {idx+1} enregistré à {center}")
#                     idx += 1

#         cv2.destroyWindow("Calibration")

#         if len(self.camera_points) == 4:
#             self._compute_homography()
#             self.calibrated = True
#             print("Calibration réussie.")
#         else:
#             print("Calibration incomplète.")

#     def _compute_homography(self):
#         camera_pts = np.array(self.camera_points, dtype=np.float32)
#         screen_pts = np.array(self.screen_points, dtype=np.float32)
#         self.homography, _ = cv2.findHomography(camera_pts, screen_pts)
    
#     def get_mouse_position(self):
#         """Retourne la position du curseur à afficher, basée sur la position trackée"""
#         if not self.calibrated or self.homography is None:
#             return None
        
#         pos = self.tracking_manager.get_position()
#         if pos is None:
#             return None

#         center = np.array([[pos[0] + pos[2] // 2, pos[1] + pos[3] // 2]], dtype=np.float32)
#         center = np.array([center])  # Homographie attend (1, 1, 2)
#         transformed = cv2.perspectiveTransform(center, self.homography)
#         return tuple(transformed[0][0])  # (x, y)

# # Exemple d'utilisation
# if __name__ == "__main__":
#     tracker = TrackingManager(camera_index=0, color_mode="JAUNE")
#     calibration = CalibrationManager(tracker)
#     calibration.start_calibration()

#     if calibration.calibrated:
#         while True:
#             pos = calibration.get_mouse_position()
#             if pos:
#                 print("Position souris :", pos)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         tracker.stop_tracking()




# import cv2
# import numpy as np
# import threading
# from tracking import TrackingManager  # ou depuis core.tracking si appelé depuis main
# import pyautogui  # Pour bouger la souris
# import time

# class CalibrationManager:
#     def __init__(self, tracking_manager, screen_size=(1920, 1080), screen_offset=(3840, 0)):
#         self.tracking_manager = tracking_manager
#         self.screen_size = screen_size
#         self.screen_offset = screen_offset  # position du second écran
#         self.screen_points = [
#             (0, 0),                               # coin haut gauche
#             (screen_size[0], 0),                  # coin haut droit
#             (screen_size[0], screen_size[1]),     # coin bas droit
#             (0, screen_size[1])                   # coin bas gauche
#         ]
#         self.camera_points = []
#         self.homography = None
#         self.calibrated = False

#     def show_projection_screen(self):
#         """Affiche les points de calibration en plein écran sur le second écran"""
#         img = np.zeros((self.screen_size[1], self.screen_size[0], 3), dtype=np.uint8)
#         r = 25
#         for pt in self.screen_points:
#             cv2.drawMarker(img, pt, (255, 255, 255), cv2.MARKER_CROSS, markerSize=r, thickness=2)

#         cv2.namedWindow("Projection", cv2.WINDOW_NORMAL)
#         cv2.moveWindow("Projection", self.screen_offset[0], self.screen_offset[1])
#         cv2.setWindowProperty("Projection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#         cv2.imshow("Projection", img)

#     def start_calibration(self):
#         print("Calibration en cours... Suivez les instructions.")
#         self.tracking_manager.start_tracking()
#         # self.show_projection_screen()
#         idx = 0

#         while idx < len(self.screen_points):
#             frame = self.tracking_manager.camera_manager.get_frame()
#             pos = self.tracking_manager.get_position()

#             if frame is not None:
#                 display = frame.copy()
#                 h, w, _ = frame.shape

#                 # Affichage des points cibles à l’échelle de l’image de la caméra (juste pour info visuelle)
#                 for i, pt in enumerate(self.screen_points):
#                     color = (0, 255, 0) if i == idx else (100, 100, 100)
#                     display_x = int(pt[0] * w / self.screen_size[0])
#                     display_y = int(pt[1] * h / self.screen_size[1])
#                     cv2.circle(display, (display_x, display_y), 10, color, -1)

#                 # Affichage de la position détectée
#                 if pos:
#                     x, y, w_rect, h_rect = pos
#                     center = (x + w_rect // 2, y + h_rect // 2)
#                     cv2.circle(display, center, 5, (0, 0, 255), -1)

#                 cv2.putText(display, f"Point {idx + 1}/4 - Appuyez sur Espace", (10, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

#                 cv2.imshow("Calibration", display)

               


#                 key = cv2.waitKey(1) & 0xFF
#                 if key == 27:  # ESC
#                     print("Calibration annulée.")
#                     break
#                 elif key == 32 and pos:  # Espace
#                     center = (pos[0] + pos[2] // 2, pos[1] + pos[3] // 2)
#                     self.camera_points.append(center)
#                     print(f"Point {idx+1} enregistré à {center}")
#                     idx += 1

#         cv2.destroyWindow("Calibration")
#         cv2.destroyWindow("Projection")

#         if len(self.camera_points) == 4:
#             self._compute_homography()
#             self.calibrated = True
#             print("Calibration réussie.")
#         else:
#             print("Calibration incomplète.")

#     def _compute_homography(self):
#         camera_pts = np.array(self.camera_points, dtype=np.float32)
#         screen_pts = np.array(self.screen_points, dtype=np.float32)
#         self.homography, _ = cv2.findHomography(camera_pts, screen_pts)

#     def get_mouse_position(self):
#         if not self.calibrated or self.homography is None:
#             return None

#         pos = self.tracking_manager.get_position()
#         if pos is None:
#             return None

#         center = np.array([[pos[0] + pos[2] // 2, pos[1] + pos[3] // 2]], dtype=np.float32)
#         center = np.array([center])  # Homographie attend (1, 1, 2)
#         transformed = cv2.perspectiveTransform(center, self.homography)
#         return tuple(transformed[0][0])  # (x, y)


# # Exemple d'utilisation
# if __name__ == "__main__":
#     tracker = TrackingManager(camera_index=0, color_mode="JAUNE")
#     calibration = CalibrationManager(tracker, screen_size=(1920, 1080), screen_offset=(3840, 0))
#     calibration.start_calibration()

#     if calibration.calibrated:
#         while True:
#             pos = calibration.get_mouse_position()
#             if pos:
#                 print("Position souris :", pos)
#                 # Déplacement de la souris
#                 # x, y = int(pos[0]), int(pos[1])
#                 # pyautogui.moveTo(x, y, duration=0.05)  # Déplacement fluide
#                 # time.sleep(0.01)  # Fréquence de mise à jour
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         tracker.stop_tracking()

#VERSION FONCTIONNELLE SANS PROJECTION SUR L'ECRAN, A GARDER
import cv2
import numpy as np
import threading
from tracking import TrackingManager  # ou depuis core.tracking si appelé depuis main

class CalibrationManager:
    def __init__(self, tracking_manager, screen_size=(1920, 1080)):
    # def __init__(self, tracking_manager, screen_size=(640, 480)):
        self.tracking_manager = tracking_manager
        self.screen_points = [
            (0, 0),                    # coin haut gauche
            (screen_size[0], 0),       # coin haut droit
            (screen_size[0], screen_size[1]),  # coin bas droit
            (0, screen_size[1])        # coin bas gauche
        ]
        self.camera_points = []
        self.homography = None
        self.calibrated = False

    def start_calibration(self):
        print("Calibration en cours... Suivez les instructions.")
        self.tracking_manager.start_tracking()
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
                    cv2.circle(display, (int(pt[0] * w / 1920), int(pt[1] * h / 1080)), 10, color, -1)

                # Affichage de la position détectée
                if pos:
                    x, y, w_rect, h_rect = pos
                    center = (x + w_rect // 2, y + h_rect // 2)
                    cv2.circle(display, center, 5, (0, 0, 255), -1)

                cv2.putText(display, f"Point {idx + 1}/4 - Appuyez sur Espace", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.imshow("Calibration", display)

                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    print("Calibration annulée.")
                    break
                elif key == 32 and pos:  # Espace
                    center = (pos[0] + pos[2] // 2, pos[1] + pos[3] // 2)
                    self.camera_points.append(center)
                    print(f"Point {idx+1} enregistré à {center}")
                    idx += 1


        cv2.destroyWindow("Calibration")

        if len(self.camera_points) == 4:
            self._compute_homography()
            self.calibrated = True
            print("Calibration réussie.")
        else:
            print("Calibration incomplète.")

    def _compute_homography(self):
        camera_pts = np.array(self.camera_points, dtype=np.float32)
        screen_pts = np.array(self.screen_points, dtype=np.float32)
        self.homography, _ = cv2.findHomography(camera_pts, screen_pts)
    
    def get_mouse_position(self):
        """Retourne la position du curseur à afficher, basée sur la position trackée"""
        if not self.calibrated or self.homography is None:
            return None
        
        pos = self.tracking_manager.get_position()
        if pos is None:
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
        center = np.array([center])  # Homographie attend (1, 1, 2)
        transformed = cv2.perspectiveTransform(center, self.homography)
        return tuple(transformed[0][0])  # (x, y)

# Exemple d'utilisation en dehors
if __name__ == "__main__":
    tracker = TrackingManager(camera_index=0, color_mode="JAUNE")
    # calibration = CalibrationManager(tracker, screen_size=(1920, 1080))
    calibration = CalibrationManager(tracker)
    calibration.start_calibration()

    if calibration.calibrated:
        while True:
            pos = calibration.get_mouse_position()
            if pos:
                print("Position souris :", pos)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        tracker.stop_tracking()

