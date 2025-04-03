import customtkinter as ctk
from typing import Any

# # from tracking import TrackingManager
# from core.tracking import TrackingManager
# from core.calibration import Calibration
# #from tracking import TrackingManager # When using the control module directly
# import time



class MainGUI:
    """Main GUI application class built with CustomTkinter."""

    def __init__(self, control_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.control_app = control_app  # Logic class instance (Control)
        self.root = ctk.CTk()
        self.root.title("MatitONE Software")
        self.root.geometry("800x600")

        # Theme settings
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Private attributes
        self._current_mode = "Normal"
        self._user_settings = {}
        self._connection_status = False
        self.is_running = False  # Ajout d'un état pour alterner entre start et stop

        # Initialize UI components
        self._init_ui()

    def _init_ui(self):
        """Initialize all UI components."""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="MatitONE Software",
            font=("Arial", 24)
        )
        self.title_label.pack(pady=20)

        # Bouton Start/Stop
        self.startbutton = ctk.CTkButton(
            self.main_frame,
            text="Start",
            command=self.toggle_start_stop,
        )
        self.startbutton.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Mode: {self._current_mode} | Connected: {self._connection_status}"
        )
        self.status_label.pack(pady=20)

    def toggle_start_stop(self):
        """Alterner entre Start et Stop."""
        if self.is_running:
            # Appel de stop_calibration() et mise à jour de l'interface
            print("Stopping calibration...")
            if hasattr(self.control_app, "stop_calibration"):
                self.control_app.stop_calibration()
            else:
                print("Warning: stop_calibration() method not found in control_app")

            self.startbutton.configure(text="Start")
        else:
            # Appel de start_control() et mise à jour de l'interface
            print("Starting control...")
            self.control_app.start_control()

            self.startbutton.configure(text="Stop")

        # Inversion de l'état
        self.is_running = not self.is_running

    def run(self) -> None:
        """Start the main application loop."""
        self.root.mainloop()


# Exemple de classe de contrôle
class ControlApp:
    def start_control(self):
        print("Starting control...")

    def stop_calibration(self):
        print("Stopping calibration...")


if __name__ == "__main__":
    control = ControlApp()  # Instance de contrôle
    app = MainGUI(control)  # Passage de l'instance à l'interface graphique
    app.run()


# # from tracking import TrackingManager
# from core.tracking import TrackingManager
# from core.calibration import Calibration
# #from tracking import TrackingManager # When using the control module directly
# import time


# class Control:
#     def __init__(self):
#         pass
#         self.tracking = None
#         self.calibration = None

#     def start_control(self):
#         self.tracking = TrackingManager(camera_index=0,color_mode="JAUNE")
#         calibration = Calibration(tracking_manager=self.tracking)
#         self.tracking.start_tracking()
#         self.tracking.debug_display()
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

    




