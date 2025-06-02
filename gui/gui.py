import customtkinter as ctk
from typing import Any
import threading
from core.control import Control


class MainGUI:
    """Main GUI application class built with CustomTkinter."""

    def __init__(self, control_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Logic class instance (Control)
        self.control_app: Control = control_app
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

        # ------ Bouton Start/Stop control  ------
        self.startbutton = ctk.CTkButton(
            self.main_frame,
            text="Start",
            command=self.toggle_start_stop,
        )
        self.startbutton.pack(pady=10)

        self.delete_profile_button = ctk.CTkButton(
            self.main_frame,
            text="Delete Calibration",
            command=self.control_app.delete_calibration
        )
        self.delete_profile_button.pack(pady=10)

        # ------ Bouton Pen connection control  ------
        if not self._connection_status:
            self.connect_button = ctk.CTkButton(
                self.main_frame,
                text="Connect Pen",
                command=self._connect_pen,
            )
            self.connect_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Mode: {self._current_mode} | Connected: {
                self._is_connected()}"
        )
        self.status_label.pack(pady=20)

    def _connect_pen(self):
        self.control_app.connect_to_pen()
        self.status_label.configure(
            text=f"Mode: {self._current_mode} | Connected: {
                self._is_connected()}"
        )

    def _is_connected(self):
        try:
            # Check if self.control_app.pen_logic is valid
            if not (
                hasattr(self.control_app, "pen_logic")
                and self.control_app.pen_logic is not None
            ):
                return "N/A"

            # Check if self.control_app.pen_logic.pen.client is valid
            # This implies pen_logic.pen must also exist and not be None.
            if not (
                hasattr(self.control_app.pen_logic, "pen")
                and self.control_app.pen_logic.pen is not None
                and hasattr(self.control_app.pen_logic.pen, "client")
                and self.control_app.pen_logic.pen.client is not None
            ):
                return "N/A"

            # If both conditions met, access 'connected' attribute
            client = self.control_app.pen_logic.pen.client
            if hasattr(client, "connected"):
                return str(client.connected)
            else:
                return "Attr Missing"  # 'connected' attribute not on client
        except Exception:
            # print(f"Error getting connection status: {e}") # For debugging
            return "Error"

    def toggle_start_stop(self):
        """Alterner entre Start et Stop."""
        if self.is_running:
            # Appel de stop_calibration() et mise à jour de l'interface
            print("Stop_control...")
            if hasattr(self.control_app, "stop_control"):
                self.control_app.stop_control()
            else:
                print("Warning: stop_calibration() method not found in control_app")

            self.startbutton.configure(text="Start")
        else:
            # Appel de start_control() et mise à jour de l'interface
            print("Starting control...")
            # Lancer la calibration dans un thread séparé
            threading.Thread(
                target=self._start_control_and_calibration, daemon=True).start()
            self.startbutton.configure(text="Stop")

        # Inversion de l'état
        self.is_running = not self.is_running

    def _start_control_and_calibration(self):
        # Ici, tu peux passer screen_size si besoin
        self.control_app.start_calibration()

    def run(self) -> None:
        """Start the main application loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainGUI()
    app.run()


# # Exemple de classe de contrôle
# class ControlApp:
#     def start_control(self):
#         print("Starting control...")

#     def stop_calibration(self):
#         print("Stopping calibration...")


# if __name__ == "__main__":
#     control = ControlApp()  # Instance de contrôle
#     app = MainGUI(control)  # Passage de l'instance à l'interface graphique
#     app.run()


# import customtkinter as ctk
# from typing import Any, Optional

# class MainGUI:
#     """Main GUI application class built with CustomTkinter."""

#     def __init__(self, control_app, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.control_app = control_app  # Logic class instance (Control)
#         # Initialize the main application window
#         self.root = ctk.CTk()
#         self.root.title("MatitONE Software")
#         self.root.geometry("800x600")

#         # Theme settings
#         ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
#         ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

#         # Private attributes for demonstration of getters and setters
#         self._current_mode = "Normal"
#         self._user_settings = {}
#         self._connection_status = False

#         # Initialize UI components
#         self._init_ui()

#     def _init_ui(self):
#         """Initialize all UI components."""
#         # Create a frame for the main content
#         self.main_frame = ctk.CTkFrame(self.root)
#         self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

#         # Add a sample label
#         self.title_label = ctk.CTkLabel(
#             self.main_frame,
#             text="MatitONE Software",
#             font=("Arial", 24)
#         )
#         self.title_label.pack(pady=20)

#         # Add a sample button
#         self.startbutton = ctk.CTkButton(
#             self.main_frame,
#             text="start button",
#             command=self.startbutton_function,
#         )
#         self.startbutton.pack(pady=10)

#         # Status label to demonstrate property changes
#         self.status_label = ctk.CTkLabel(
#             self.main_frame,
#             text=f"Mode: {self._current_mode} | Connected: {self._connection_status}"
#         )
#         self.status_label.pack(pady=20)

#     def startbutton_function(self):
#         """Example method for button command."""
#         print("start button pressed")
#         self.control_app.start_control()  # Call the control app method
#         # Toggle connection status when button is pressed
#         self.connection_status = not self.connection_status


#     # Example getters and setters using properties

#     @property
#     def current_mode(self) -> str:
#         """Get the current application mode."""
#         return self._current_mode

#     @current_mode.setter
#     def current_mode(self, value: str) -> None:
#         """Set the current application mode."""
#         self._current_mode = value
#         # Update UI when mode changes
#         self.update_status_display()

#     @property
#     def user_settings(self) -> dict:
#         """Get user settings dictionary."""
#         return self._user_settings.copy()  # Return a copy to prevent direct modification

#     def update_user_setting(self, key: str, value: Any) -> None:
#         """Set a specific user setting."""
#         self._user_settings[key] = value
#         print(f"Updated setting: {key} = {value}")

#     @property
#     def connection_status(self) -> bool:
#         """Get the connection status."""
#         return self._connection_status

#     @connection_status.setter
#     def connection_status(self, status: bool) -> None:
#         """Set the connection status."""
#         self._connection_status = status
#         # Update UI when status changes
#         self.update_status_display()

#     def update_status_display(self) -> None:
#         """Update the status display in the UI."""
#         self.status_label.configure(
#             text=f"Mode: {self._current_mode} | Connected: {self._connection_status}"
#         )

#     def run(self) -> None:
#         """Start the main application loop."""
#         self.root.mainloop()


# if __name__ == "__main__":
#     app = MainGUI()
#     app.run()
