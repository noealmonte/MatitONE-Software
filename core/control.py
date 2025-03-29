# from tracking import TrackingManager
from core.tracking import TrackingManager
#from tracking import TrackingManager # When using the control module directly



class Control:
    def __init__(self):
        pass

    def start_control(self):
        tracking = TrackingManager(camera_index=0,color_mode="JAUNE")
        tracking.start_tracking()
        tracking.debug_display()


    def stop_control(self):
        print("Fin du programme")   

    


if __name__ == "__main__":
    control_app = Control()
    control_app.start_control()




