import tkinter as tk
import threading
import time
import math
import json
import os

class Calibration:
    def __init__(self, tracking_manager, real_width=100, real_height=100):
        """
        Initialise la calibration avec un gestionnaire de tracking.
        
        Args:
            tracking_manager: Instance de TrackingManager pour suivre l'objet
            real_width: Largeur réelle en millimètres entre les croix (par défaut 100mm)
            real_height: Hauteur réelle en millimètres entre les croix (par défaut 100mm)
        """
        self.tracking_manager = tracking_manager
        self.real_width = real_width
        self.real_height = real_height
        
        self.calibration_points = []
        self.current_point_idx = 0
        self.total_points = 4
        self.scale_factor = None
        self.calibration_complete = False
        
        self.stability_duration = 1.0 # Durée de stabilité requise en secondes
        self.stability_threshold = 5
        
        self.root = None
        self.canvas = None
        self.calibration_thread = None

    def start_calibration(self):
        """Démarre le processus de calibration."""
        self.calibration_points = []
        self.current_point_idx = 0
        self.calibration_complete = False
        
        if not self.tracking_manager.running:
            self.tracking_manager.start_tracking()
        
        self.calibration_thread = threading.Thread(target=self._calibration_loop, daemon=True)
        self.calibration_thread.start()
        
        self._show_ui()

    def _show_ui(self):
        """Affiche une interface graphique simple avec 4 croix."""
        self.root = tk.Tk()
        self.root.title("Calibration")
        self.root.geometry("800x600")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(fill="both", expand=True)
        
        self._draw_crosses()
        
        self.root.protocol("WM_DELETE_WINDOW", self.stop_calibration)
        self.root.mainloop()

    def _draw_crosses(self):
        """Dessine les 4 croix sur le canvas."""
        positions = [
            (100, 100),  # Haut gauche
            (700, 100),  # Haut droite
            (700, 500),  # Bas droite
            (100, 500)   # Bas gauche
        ]
        
        for i, (x, y) in enumerate(positions):
            color = "red" if i == self.current_point_idx else "black"
            self.canvas.create_line(x - 10, y, x + 10, y, fill=color, width=2)
            self.canvas.create_line(x, y - 10, x, y + 10, fill=color, width=2)

    def _calibration_loop(self):
        """Boucle principale pour détecter les points stables."""
        positions = [
            (100, 100),  # Haut gauche
            (700, 100),  # Haut droite
            (700, 500),  # Bas droite
            (100, 500)   # Bas gauche
        ]
        print("je suis dans la boucle de calibration")
        while self.current_point_idx < self.total_points:
            ref_x, ref_y = positions[self.current_point_idx]
            if self._check_stability_at((ref_x, ref_y)):
                self.current_point_idx += 1
                self._update_ui()
        
        self._calculate_scale()
        self.calibration_complete = True
        print("Calibration terminée!")

    def _check_stability_at(self, reference_point):
        """Vérifie si l'objet reste stable à proximité d'un point de référence."""
        start_time = None
        ref_x, ref_y = reference_point
      
        while True:
            position = self.tracking_manager.get_position()
            if position:
                x, y, w, h = position
                center_x = x + w // 2
                center_y = y + h // 2
                print("Coordonnées à atteindre:", ref_x, ref_y)
                print("Coordonnées détectées:", center_x, center_y)
                time.sleep(0.5)
                distance = math.sqrt((center_x - ref_x)**2 + (center_y - ref_y)**2)
                if distance < 500: # Sensibilité de 500 pixels d'écalage
                    if start_time is None:
                        start_time = time.time()
                    elif time.time() - start_time >= self.stability_duration:
                        self.calibration_points.append((center_x, center_y))
                        return True
                else:
                    start_time = None
            time.sleep(0.1)

    def _update_ui(self):
        """Met à jour l'interface graphique pour refléter l'état actuel."""
        if self.root and self.canvas:
            self.canvas.delete("all")
            self._draw_crosses()

    def _calculate_scale(self):
        """Calcule le facteur d'échelle basé sur les points collectés."""
        if len(self.calibration_points) != 4:
            print("Erreur: Nombre de points de calibration incorrect")
            return
        
        width_px = abs(self.calibration_points[1][0] - self.calibration_points[0][0])
        height_px = abs(self.calibration_points[3][1] - self.calibration_points[0][1])
        
        scale_x = width_px / self.real_width
        scale_y = height_px / self.real_height
        self.scale_factor = (scale_x + scale_y) / 2
        
        calibration_data = {
            'scale_factor': self.scale_factor,
            'calibration_points': self.calibration_points,
            'real_width_mm': self.real_width,
            'real_height_mm': self.real_height,
            'calibration_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        os.makedirs('config', exist_ok=True)
        with open('config/calibration.json', 'w') as f:
            json.dump(calibration_data, f, indent=4)
        
        print(f"Facteur d'échelle: {self.scale_factor:.4f} pixels/mm")

    def stop_calibration(self):
        """Arrête la calibration et ferme l'interface graphique."""
        if self.root:
            self.root.destroy()

    def get_scale_factor(self):
        """Renvoie le facteur d'échelle calculé."""
        return self.scale_factor

if __name__ == "__main__":
    
    # from tracking import TrackingManager  # Remplacer par l'import correct
    # control_app = TrackingManager()
    # control_thread = threading.Thread(target=control_app.start_control, daemon=True)
    # control_thread.start()  
    # tracking_manager = TrackingManager(camera_index=0, color_mode="JAUNE")
    # tracking_manager.start_tracking()
    # tracking_manager.debug_display()
    # calibration = Calibration(tracking_manager)
    # calibration.start_calibration()
    from tracking import TrackingManager  # Remplacer par l'import correct
    tracking_manager = TrackingManager(camera_index=0, color_mode="JAUNE")
    track_thread = threading.Thread(target=tracking_manager.start_tracking, daemon=True)
    display_thread = threading.Thread(target=tracking_manager.debug_display, daemon=True)
    track_thread.start()
    display_thread.start()
    # tracking_manager.debug_display()
    calibration = Calibration(tracking_manager)
    calibration.start_calibration()

