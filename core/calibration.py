import customtkinter as ctk
import cv2
import numpy as np
import threading
import time
import json
import os
import math
from PIL import Image, ImageDraw

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
        
        self.calibration_running = False
        self.calibration_thread = None
        
        self.calibration_points = []  # Points de calibration collectés [(x1, y1), ...]
        self.current_point_idx = 0
        self.total_points = 4  # Total des points à collecter
        
        self.scale_factor = None  # Facteur d'échelle calculé (pixels par mm)
        self.calibration_complete = False
        
        # Paramètres pour la détection de stabilité
        self.stability_duration = 3.0  # Durée de stabilité requise (secondes)
        self.stability_threshold = 5  # Tolérance en pixels
        
        # UI éléments
        self.root = None
        self.canvas = None
        self.ui_thread = None
        self.stop_ui = False

    def start_calibration(self):
        """Lance le processus de calibration"""
        if self.calibration_running:
            return False
            
        self.calibration_running = True
        self.calibration_points = []
        self.current_point_idx = 0
        self.calibration_complete = False
        
        # Assurez-vous que le tracking est actif
        if not self.tracking_manager.running:
            self.tracking_manager.start_tracking()
        
        # Lancer la GUI pour la calibration
        self._show_calibration_ui()
        
        # Lancer la détection des points de calibration
        self.calibration_thread = threading.Thread(target=self._calibration_loop, daemon=True)
        self.calibration_thread.start()
        print("Calibration démarrée")
        
        return True
    
    def _show_calibration_ui(self):
        """Affiche l'interface de calibration avec 4 croix"""
        if self.ui_thread is not None and self.ui_thread.is_alive():
            self.stop_ui = True
            self.ui_thread.join(timeout=1.0)
            
        self.stop_ui = False
        self.ui_thread = threading.Thread(target=self._ui_thread_func, daemon=True)
        self.ui_thread.start()
        print("Interface de calibration affichée")

    def _ui_thread_func(self):
        """Fonction exécutée dans un thread pour gérer l'interface utilisateur"""
        self.root = ctk.CTk()
        self.root.title("Calibration")
        # Configurer la fenêtre
        screen_width = self.root.winfo_screenwidth() // 2
        screen_height = self.root.winfo_screenheight() // 2
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Créer un label pour les instructions
        instruction_label = ctk.CTkLabel(self.root, 
                                        text="Placez l'objet de tracking sur chaque croix pendant 3 secondes.\n"
                                             f"Point actuel: {self.current_point_idx + 1}/{self.total_points}")
        instruction_label.pack(pady=10)
        
        # Créer un canvas pour les croix
        self.canvas = ctk.CTkCanvas(self.root, width=screen_width, height=screen_height - 100)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Dessiner les quatre croix aux coins
        padding = 50
        cross_size = 15
        
        # Croix en haut à gauche (0)
        x1, y1 = padding, padding
        self._draw_cross(x1, y1, cross_size, "Point 1", "red" if self.current_point_idx == 0 else "black")
        
        # Croix en haut à droite (1)
        x2, y2 = screen_width - padding - 40, padding
        self._draw_cross(x2, y2, cross_size, "Point 2", "red" if self.current_point_idx == 1 else "black")
        
        # Croix en bas à droite (2)
        x3, y3 = screen_width - padding - 40, screen_height - padding - 100
        self._draw_cross(x3, y3, cross_size, "Point 3", "red" if self.current_point_idx == 2 else "black")
        
        # Croix en bas à gauche (3)
        x4, y4 = padding, screen_height - padding - 100
        self._draw_cross(x4, y4, cross_size, "Point 4", "red" if self.current_point_idx == 3 else "black")
        
        # Configurer la fermeture de la fenêtre
        def on_close():
            self.stop_ui = True
            self.calibration_running = False
            self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_close)
        
        # Boucle de mise à jour
        while not self.stop_ui:
            # Mettre à jour le texte d'instruction
            instruction_label.configure(text=f"Placez l'objet de tracking sur chaque croix pendant 3 secondes.\n"
                                            f"Point actuel: {self.current_point_idx + 1}/{self.total_points}")
            
            # Mettre à jour la couleur des croix
            self._update_cross_colors()
            
            # Mise à jour de l'interface
            self.root.update()
            time.sleep(0.05)
            
            # Si la calibration est terminée
            if self.calibration_complete:
                instruction_label.configure(text="Calibration terminée! Vous pouvez fermer cette fenêtre.")
                self.root.update()
                time.sleep(2)
                break
                
        # Nettoyer
        if self.root and self.root.winfo_exists():
            self.root.destroy()
        
    
    def _draw_cross(self, x, y, size, label, color="black"):
        """Dessine une croix à la position (x, y) avec une taille donnée"""
        # Lignes horizontales et verticales
        self.canvas.create_line(x-size, y, x+size, y, fill=color, width=2)
        self.canvas.create_line(x, y-size, x, y+size, fill=color, width=2)
        
        # Étiquette
        self.canvas.create_text(x, y+size+10, text=label, fill=color)
        
        return (x, y)  # Retourne les coordonnées du centre
    
    def _update_cross_colors(self):
        """Met à jour les couleurs des croix en fonction du point actuel"""
        self.canvas.delete("all")
        
        padding = 50
        cross_size = 15
        
        screen_width = self.root.winfo_width()
        screen_height = self.root.winfo_height()
        
        # Positions des quatre croix
        positions = [
            (padding, padding),  # Haut gauche
            (screen_width - padding - 40, padding),  # Haut droite
            (screen_width - padding - 40, screen_height - padding - 100),  # Bas droite
            (padding, screen_height - padding - 100)  # Bas gauche
        ]
        
        # Dessiner les quatre croix avec la couleur appropriée
        for i, (x, y) in enumerate(positions):
            color = "red" if i == self.current_point_idx else "black"
            color = "green" if i < self.current_point_idx else color
            self._draw_cross(x, y, cross_size, f"Point {i+1}", color)
    
    def _calibration_loop(self):
        """Boucle principale de calibration pour détecter les points stables"""
        # Points de référence de l'interface (à recalculer en fonction de la taille réelle)
        padding = 50
        
        while self.calibration_running and not self.calibration_complete:
            # Mise à jour des positions de référence à partir de la taille de la fenêtre
            if self.root and hasattr(self, 'canvas') and self.canvas:
                screen_width = self.root.winfo_width()
                screen_height = self.root.winfo_height()
                
                # Définir les positions des croix
                reference_points = [
                    (padding, padding),  # Haut gauche
                    (screen_width - padding - 40, padding),  # Haut droite
                    (screen_width - padding - 40, screen_height - padding - 100),  # Bas droite
                    (padding, screen_height - padding - 100)  # Bas gauche
                ]
                # Vérifier si l'objet est stable sur le point actuel
                if self.current_point_idx < self.total_points:
                    if self._check_stability_at(reference_points[self.current_point_idx]):
                        # Point validé, passer au suivant
                        self.current_point_idx += 1
                        
                        # Vérifie si tous les points ont été collectés
                        if self.current_point_idx >= self.total_points:
                            # Calculer le facteur d'échelle et l'enregistrer
                            self._calculate_scale()
                            self.calibration_complete = True
                            self.calibration_running = False
                            break
           
            time.sleep(0.1)
    
    def _check_stability_at(self, reference_point):
        """
        Vérifie si l'objet trackée reste stable à proximité d'un point de référence
        pendant la durée spécifiée.
        """
        start_time = None
        last_valid_position = None
        
        ref_x, ref_y = reference_point
        
        # Boucle pour vérifier la stabilité
        while self.calibration_running:
            position = self.tracking_manager.get_position()
            
            if position:
                x, y, w, h = position
                center_x = x + w // 2
                center_y = y + h // 2
                
                # Calculer la distance au point de référence (à l'écran)
                distance = math.sqrt((center_x - ref_x)**2 + (center_y - ref_y)**2)
                
                # Si la position est proche du point de référence
                if distance < 100:  # Ajuster selon la sensibilité voulue
                    # Si c'est une nouvelle position valide ou si la position a changé significativement
                    if last_valid_position is None or \
                       abs(center_x - last_valid_position[0]) > self.stability_threshold or \
                       abs(center_y - last_valid_position[1]) > self.stability_threshold:
                        # Réinitialiser le compteur
                        start_time = time.time()
                        last_valid_position = (center_x, center_y)
                    else:
                        # La position est stable, vérifier si la durée est suffisante
                        elapsed_time = time.time() - start_time
                        if elapsed_time >= self.stability_duration:
                            # Point validé, l'ajouter à la liste
                            self.calibration_points.append((center_x, center_y))
                            return True
                else:
                    # Position hors de la cible, réinitialiser
                    start_time = None
                    last_valid_position = None
            
            time.sleep(0.1)
    
    def _calculate_scale(self):
        """
        Calcule le facteur d'échelle entre les distances en pixels et les distances réelles
        et sauvegarde le résultat.
        """
        if len(self.calibration_points) != 4:
            print("Erreur: Nombre de points de calibration incorrect")
            return False
        
        # Calculer les distances en pixels
        # Largeur (moyenne des distances horizontales)
        width_px_top = abs(self.calibration_points[1][0] - self.calibration_points[0][0])
        width_px_bottom = abs(self.calibration_points[2][0] - self.calibration_points[3][0])
        avg_width_px = (width_px_top + width_px_bottom) / 2
        
        # Hauteur (moyenne des distances verticales)
        height_px_left = abs(self.calibration_points[3][1] - self.calibration_points[0][1])
        height_px_right = abs(self.calibration_points[2][1] - self.calibration_points[1][1])
        avg_height_px = (height_px_left + height_px_right) / 2
        
        # Calculer les facteurs d'échelle (pixels par mm)
        scale_x = avg_width_px / self.real_width
        scale_y = avg_height_px / self.real_height
        
        # Moyenne des deux facteurs pour un facteur d'échelle unique
        self.scale_factor = (scale_x + scale_y) / 2
        
        # Enregistrer les résultats dans un fichier
        calibration_data = {
            'scale_factor': self.scale_factor,  # pixels par mm
            'calibration_points': self.calibration_points,
            'real_width_mm': self.real_width,
            'real_height_mm': self.real_height,
            'calibration_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Créer le dossier config s'il n'existe pas
        os.makedirs('config', exist_ok=True)
        
        # Sauvegarder les données dans un fichier JSON
        with open('config/calibration.json', 'w') as f:
            json.dump(calibration_data, f, indent=4)
        
        print(f"Calibration terminée! Facteur d'échelle: {self.scale_factor:.4f} pixels/mm")
        return True
    
    def stop_calibration(self):
        """Arrête le processus de calibration"""
        self.calibration_running = False
        self.stop_ui = True
        
        if self.ui_thread and self.ui_thread.is_alive():
            self.ui_thread.join(timeout=1.0)
    
    def is_calibration_done(self):
        """Vérifie si la calibration est terminée"""
        return self.calibration_complete
    
    @staticmethod
    def load_calibration():
        """Charge les données de calibration depuis le fichier"""
        try:
            with open('config/calibration.json', 'r') as f:
                data = json.load(f)
            return data['scale_factor']
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            print("Aucune calibration trouvée ou fichier corrompu")
            return None
    
    def get_scale_factor(self):
        """Renvoie le facteur d'échelle actuel"""
        return self.scale_factor or Calibration.load_calibration()
    
    def convert_pixels_to_mm(self, pixels):
        """Convertit une distance en pixels en millimètres"""
        scale = self.get_scale_factor()
        if scale:
            return pixels / scale
        return None
    
    def convert_mm_to_pixels(self, mm):
        """Convertit une distance en millimètres en pixels"""
        scale = self.get_scale_factor()
        if scale:
            return mm * scale
        return None