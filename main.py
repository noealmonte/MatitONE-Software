from core.camera import Camera 
from core.tracking import Tracking
from core.calibration import Calibration
# import cv2
import time
    
def main():
    # Initialisation des modules
    camera = Camera()
    tracking = Tracking(camera)
    calibration = Calibration()

    try:
        # Démarrage des threads
        camera.start()
        tracking.start()

        # Phase de calibration
        calibration.start()
        time.sleep(4)  # Attente de la fin de calibration (simulé)
        calibration.stop()

        # Simulation d'utilisation
        for _ in range(10):
            print("Position détectée:", tracking.get_position())
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nArrêt du programme...")

    finally:
        # Arrêt propre des threads
        tracking.stop()
        camera.stop()

if __name__ == "__main__":
    main()  
# def main():
#     # Initialisation de la caméra
#     camera = Camera()
#     tracker = Tracking(camera)
#     calibration = Calibration(tracker, real_width=100, real_height=75)  # Exemple : 100x75 cm


#     try:
#         # Démarrage de la caméra
#         camera.connect_to_webcam(1)  # Exemple : la première webcam
#         print("La caméra fonctionne correctement.")

#         # Affichage d'une frame en direct
#         while True:
#            # tracker.start_tracking(filter_type="yellow")  # Exemple avec le filtre jaune
#             calibration.show_gui()
#             calibration.calibrate()
         
#             # Quitte la boucle si l'utilisateur appuie sur la touche 'q'
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # Capture d'une image

#     except Exception as e:
#         print(f"Erreur : {e}")

#     finally:
#         # Arrêt de la caméra et fermeture des fenêtres
#         camera.release_webcam()
#         cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()
