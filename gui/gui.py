import customtkinter as ctk
from typing import Any, Optional

class MainGUI:
    """Main GUI application class built with CustomTkinter."""
    
    def __init__(self, control_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.control_app = control_app  # Logic class instance (Control)
        # Initialize the main application window
        self.root = ctk.CTk()
        self.root.title("MatitONE Software")
        self.root.geometry("800x600")
        
        # Theme settings
        ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
        
        # Private attributes for demonstration of getters and setters
        self._current_mode = "Normal"
        self._user_settings = {}
        self._connection_status = False
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self):
        """Initialize all UI components."""
        # Create a frame for the main content
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add a sample label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="MatitONE Software", 
            font=("Arial", 24)
        )
        self.title_label.pack(pady=20)
        
        # Add a sample button
        self.startbutton = ctk.CTkButton(
            self.main_frame,
            text="start button",
            command=self.startbutton_function,
        )
        self.startbutton.pack(pady=10)
        
        # Status label to demonstrate property changes
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Mode: {self._current_mode} | Connected: {self._connection_status}"
        )
        self.status_label.pack(pady=20)
    
    def startbutton_function(self):
        """Example method for button command."""
        print("start button pressed")
        self.control_app.start_control()  # Call the control app method
        # Toggle connection status when button is pressed
        self.connection_status = not self.connection_status
    



    
    # Example getters and setters using properties
    
    @property
    def current_mode(self) -> str:
        """Get the current application mode."""
        return self._current_mode
    
    @current_mode.setter
    def current_mode(self, value: str) -> None:
        """Set the current application mode."""
        self._current_mode = value
        # Update UI when mode changes
        self.update_status_display()
    
    @property
    def user_settings(self) -> dict:
        """Get user settings dictionary."""
        return self._user_settings.copy()  # Return a copy to prevent direct modification
    
    def update_user_setting(self, key: str, value: Any) -> None:
        """Set a specific user setting."""
        self._user_settings[key] = value
        print(f"Updated setting: {key} = {value}")
    
    @property
    def connection_status(self) -> bool:
        """Get the connection status."""
        return self._connection_status
    
    @connection_status.setter
    def connection_status(self, status: bool) -> None:
        """Set the connection status."""
        self._connection_status = status
        # Update UI when status changes
        self.update_status_display()
    
    def update_status_display(self) -> None:
        """Update the status display in the UI."""
        self.status_label.configure(
            text=f"Mode: {self._current_mode} | Connected: {self._connection_status}"
        )
    
    def run(self) -> None:
        """Start the main application loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainGUI()
    app.run()