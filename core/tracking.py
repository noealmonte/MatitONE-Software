import cv2
import numpy as np

class Tracking:
    def __init__(self, camera):
        """
        Initialise la classe Tracking avec une instance de la classe Camera.
        """
        self.camera = camera
        self.tracking_active = False

    def start_tracking(self, filter_type="red"):
        """
        Démarre le suivi d'un point selon le filtre choisi.
        - filter_type : type de filtre utilisé pour le tracking (exemple : "red").
        """
        if not self.camera.cap or not self.camera.cap.isOpened():
            raise RuntimeError("La caméra n'est pas connectée ou active.")
        
        self.tracking_active = True
        print(f"Tracking démarré avec le filtre '{filter_type}'.")

        while self.tracking_active:
            frame = self.camera.get_frame()

            # Applique le filtre choisi
            if filter_type == "red":
                tracked_frame = self._track_red(frame)
            elif filter_type == "yellow":
                tracked_frame = self._track_yellow(frame)
            else:
                print("Type de filtre non pris en charge.")
                break

            cv2.imshow("Tracking", tracked_frame)

            # Quitte le suivi avec la touche 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_tracking()
        
        cv2.destroyAllWindows()

    def stop_tracking(self):
        """
        Arrête le tracking.
        """
        self.tracking_active = False
        print("Tracking arrêté.")

    def _track_red(self, frame):
        """
        Tracking basé sur la couleur rouge, avec détection de la position.
        """
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Définir les plages de couleur pour le rouge (deux plages pour gérer les teintes)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        # Masque pour les deux plages
        mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask = mask1 + mask2

        # Trouver les contours de l'objet rouge
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Ignorer les petits objets
                x, y, w, h = cv2.boundingRect(contour)
                # Dessiner un cadre autour de l'objet
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Calculer la position absolue du centre
                center_x = x + w // 2
                center_y = y + h // 2
                # Afficher la position dans la console
                print(f"Position absolue : ({center_x}, {center_y})")
                # Marquer le centre de l'objet
                cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
        
        return frame

    def _track_yellow(self, frame):
        """
        Exemple de tracking basé sur la couleur jaune.
        """
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Définir les plages de couleur pour le jaune
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

        # Trouver les contours de l'objet jaune (comme pour le rouge, si nécessaire)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Ignorer les petits objets
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame
