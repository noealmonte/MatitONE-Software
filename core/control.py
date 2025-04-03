# from tracking import TrackingManager
from core.tracking import TrackingManager
from core.calibration import Calibration
#from tracking import TrackingManager # When using the control module directly



class Control:
    def __init__(self):
        pass

    def start_control(self):
        tracking = TrackingManager(camera_index=0,color_mode="JAUNE")
        calibration = Calibration(tracking_manager=tracking)
        # input("Press 's' and Enter to start the calibration thread...")        
        # calibration.calibration_thread.start()  # Démarre le thread de calibration
        tracking.start_tracking()
        tracking.debug_display()


    def start_calibration(self, tracking):
        calibration = Calibration(tracking_manager=tracking)
        # calibration.calibration_thread.start()

    def stop_control(self):
        print("Fin du programme")   

    


if __name__ == "__main__":
    control_app = Control()
    control_app.start_control()

    




