from core.camera import CameraManager
from core.tracking import TrackingManager
from core.calibration import Calibration

camera = CameraManager()
tracking = TrackingManager(camera, color_mode="JAUNE")
calibration = Calibration(tracking)

camera.start_camera()
tracking.start_tracking()
tracking.debug_display()
#calibration.start_calibration()
calibration._ui_thread_func()


# Mode debug pour voir l'affichage en temps réel

print("Fin du programme")
