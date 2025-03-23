import customtkinter as ctk
import time

class Calibration:
    def __init__(self, tracking, real_width, real_height):
        """
        Initialise la classe Calibration.
        - tracking : instance de la classe Tracking utilisée pour détecter le point à calibrer.
        - real_width : largeur réelle en unité (par exemple, en centimètres).
        - real_height : hauteur réelle en unité (par exemple, en centimètres).
        """
        self.tracking = tracking
        self.real_width = real_width
        self.real_height = real_height
        self.pixel_points = []  # Points calibrés en pixels
        self.real_points = []   # Points calibrés en unités réelles (cm)

    def show_gui(self):
        """
        Affiche la GUI avec 4 croix noires aux coins sur un fond blanc.
        """
        ctk.set_appearance_mode("light")  # Mode clair
        ctk.set_default_color_theme("blue")  # Thème par défaut

        self.root = ctk.CTk()  # Fenêtre principale
        self.root.title("Calibration GUI")
        self.root.geometry("800x600")

        # Canvas pour dessiner
        self.canvas = ctk.CTkCanvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Taille de l'écran en pixels
        screen_width = 800  # À ajuster si nécessaire
        screen_height = 600

        # Positions des croix
        cross_size = 10
        self.cross_positions = [
            (20, 20),  # Coin haut-gauche
            (screen_width - 20, 20),  # Coin haut-droit
            (20, screen_height - 20),  # Coin bas-gauche
            (screen_width - 20, screen_height - 20),  # Coin bas-droit
        ]

        # Dessine les croix noires
        for x, y in self.cross_positions:
            self.canvas.create_line(x - cross_size, y, x + cross_size, y, fill="black", width=2)
            self.canvas.create_line(x, y - cross_size, x, y + cross_size, fill="black", width=2)

        self.root.after(100, self.calibrate)  # Démarre la calibration
        self.root.mainloop()

    def calibrate(self):
        """
        Lance le processus de calibration pour associer les points réels avec les pixels.
        """
        print("Début de la calibration...")
        for idx, (x, y) in enumerate(self.cross_positions):
            print(f"Calibrez le point {idx + 1} situé aux coordonnées ({x}, {y})")
            fixed_position = self._validate_position((x, y))
            if fixed_position:
                self.pixel_points.append(fixed_position)
                self.real_points.append((idx % 2 * self.real_width, idx // 2 * self.real_height))
                print(f"Point calibré : Pixel = {fixed_position}, Réel = {self.real_points[-1]}")

        print("Calibration terminée.")
        self.calculate_transformation_matrix()

    def _validate_position(self, cross_pos, tolerance=20, duration=3):
        """
        Valide la position d'un point s'il reste stable dans une zone pendant `duration` secondes.
        """
        start_time = time.time()
        while True:
            frame = self.tracking.camera.get_frame()
            tracked_position = self.tracking._track_red(frame)  # Remplacez par le filtre actif
            if not tracked_position:
                continue

            # Vérifie si le point est dans la marge de tolérance
            px, py = tracked_position
            if abs(px - cross_pos[0]) <= tolerance and abs(py - cross_pos[1]) <= tolerance:
                if time.time() - start_time >= duration:
                    print(f"Position validée pour la croix en ({cross_pos[0]}, {cross_pos[1]}) : ({px}, {py})")
                    return (px, py)
            else:
                start_time = time.time()  # Réinitialise si le point quitte la zone

    def calculate_transformation_matrix(self):
        """
        Calcule une transformation pour mapper les pixels à des distances réelles (par exemple, cm).
        """
        if len(self.pixel_points) < 4:
            print("Erreur : 4 points sont nécessaires pour effectuer la calibration.")
            return

        # Calcule les échelles en pixels/réel
        pixel_width = abs(self.pixel_points[1][0] - self.pixel_points[0][0])
        pixel_height = abs(self.pixel_points[2][1] - self.pixel_points[0][1])

        self.scale_x = self.real_width / pixel_width
        self.scale_y = self.real_height / pixel_height

        print(f"Calibration complète : Échelle X = {self.scale_x} unités/pixel, Échelle Y = {self.scale_y} unités/pixel.")
