import cv2
import numpy as np
import threading
import time
from tracking import TrackingManager

class Calibration:
    def __init__(self, tracking_manager, real_points=None):
        """
        Initialise la calibration avec le gestionnaire de tracking et les points réels de calibration.
        
        Args:
            tracking_manager (TrackingManager): Instance du gestionnaire de tracking.
            real_points (list): Liste des points réels correspondants aux points de calibration dans l'image.
        """
        self.tracking_manager = tracking_manager
        self.real_points = real_points if real_points else [(0, 0), (100, 0), (100, 100), (0, 100)]  # Points en mm
        self.image_points = []  # Points collectés via le tracking
        self.homography_matrix = None  # Matrice d'homographie
        self.calibration_complete = False
        self.collecting_points = True
        self.lock = threading.Lock()
        
        # On démarre le thread de calibration
        self.calibration_thread = threading.Thread(target=self._calibration_loop, daemon=True)
        self.calibration_thread.start()

    def _calibration_loop(self):
        """Boucle pour collecter les points de calibration et calculer l'homographie."""
        while self.collecting_points:
            # On récupère la position de l'objet via le tracking manager
            position = self.tracking_manager.get_position()
            if position:
                x, y, w, h = position
                # Calculer le centre de l'objet
                center_x = x + w // 2
                center_y = y + h // 2
                self._collect_point((center_x, center_y))
            time.sleep(0.1)

    def _collect_point(self, detected_point):
        """Collecte un point et l'ajoute à la liste des points collectés."""
        with self.lock:
            if len(self.image_points) < len(self.real_points):
                self.image_points.append(detected_point)
                print(f"Point collecté : {detected_point}, Points collectés : {len(self.image_points)}")
            
            # Si on a collecté tous les points, on effectue la calibration
            if len(self.image_points) == len(self.real_points):
                self._calculate_homography()
    
    def _calculate_homography(self):
        """Calcule la matrice d'homographie à partir des points collectés."""
        if len(self.image_points) == len(self.real_points):
            print("Calcul de l'homographie en cours...")
            # Conversion des points en numpy arrays pour OpenCV
            image_pts = np.array(self.image_points, dtype=np.float32)
            real_pts = np.array(self.real_points, dtype=np.float32)
            
            # Calcul de la matrice d'homographie
            self.homography_matrix, _ = cv2.findHomography(image_pts, real_pts)
            self.calibration_complete = True
            print("Calibration terminée!")

    def apply_homography(self, point):
        """Applique la matrice d'homographie à un point donné."""
        if self.homography_matrix is not None:
            point_array = np.array([point[0], point[1], 1.0], dtype=np.float32).reshape(3, 1)
            transformed_point = np.dot(self.homography_matrix, point_array)
            # Normaliser pour obtenir les coordonnées en 2D
            transformed_point = transformed_point / transformed_point[2]
            return transformed_point[0], transformed_point[1]
        return None
    
    def stop_calibration(self):
        """Arrête la collecte de points et ferme le processus de calibration."""
        self.collecting_points = False
        print("Calibration arrêtée.")

    def get_homography_matrix(self):
        """Renvoie la matrice d'homographie calculée."""
        return self.homography_matrix

    def is_calibration_complete(self):
        """Vérifie si la calibration est terminée."""
        return self.calibration_complete

if __name__ == "__main__":
     # Initialisation du TrackingManager
    tracking_manager = TrackingManager(camera_index=0, color_mode="JAUNE")
    tracking_manager.start_tracking()

    # Initialisation de la calibration
    calibration = Calibration(tracking_manager)
    
    # Attendre la fin de la calibration
    while not calibration.is_calibration_complete():
        time.sleep(1)
    
    # Une fois la calibration terminée, obtenir la matrice d'homographie
    homography_matrix = calibration.get_homography_matrix()
    print("Matrice d'Homographie calculée:", homography_matrix)

    # Appliquer l'homographie à un point détecté
    point = (150, 200)  # Exemple de point à transformer
    real_coords = calibration.apply_homography(point)
    print(f"Point transformé : {real_coords}")