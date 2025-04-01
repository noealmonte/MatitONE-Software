import cv2
import numpy as np
import pyautogui

# --- Paramètres de l'écran ---
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()  # Dimensions de l'écran PC

# --- Points de calibration sur l'image projetée ---
PROJECTED_POINTS = np.array([
    [100, 100],  # Haut-gauche
    [500, 100],  # Haut-droit
    [500, 400],  # Bas-droit
    [100, 400]   # Bas-gauche
], dtype=np.float32)

# --- Variables pour stocker les points capturés ---
captured_points = []

# --- Ouvrir la webcam ---
cap = cv2.VideoCapture(0)  # Change à 1 ou 2 si mauvaise caméra détectée

def get_yellow_position(frame):
    """Détecte la zone de couleur jaune et retourne ses coordonnées."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convertir en HSV
    lower_yellow = np.array([20, 100, 100])  # Seuil bas pour le jaune
    upper_yellow = np.array([30, 255, 255])  # Seuil haut pour le jaune

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)  # Masque de détection du jaune
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)  # Prendre le plus gros contour
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])  # Coordonnée X
            cy = int(M["m01"] / M["m00"])  # Coordonnée Y
            return (cx, cy)
    return None

def get_red_position(frame):
    """Détecte la zone de couleur rouge et retourne ses coordonnées."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convertir en HSV
    lower_red = np.array([0, 100, 100])  # Seuil bas pour le rouge
    upper_red = np.array([10, 255, 255])  # Seuil haut pour le rouge

    mask = cv2.inRange(hsv, lower_red, upper_red)  # Masque de détection du rouge
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)  # Prendre le plus gros contour
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])  # Coordonnée X
            cy = int(M["m01"] / M["m00"])  # Coordonnée Y
            return (cx, cy)
    return None

# --- Étape 1 : Calibration (L'utilisateur place son stylo sur les points projetés) ---
print("Calibration : placez votre stylo jaune sur chaque point affiché sur l'image projetée.")
for i, point in enumerate(PROJECTED_POINTS):
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Afficher l'instruction
        cv2.putText(frame, f"Placez le stylo ici [{i+1}/4]", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.circle(frame, (int(point[0]), int(point[1])), 10, (255, 0, 0), -1)  # Afficher les points projetés

        # Détection du stylo jaune
        # yellow_position = get_yellow_position(frame)
        yellow_position = get_red_position(frame)  # Détection du stylo rouge
        if yellow_position:
            cv2.circle(frame, yellow_position, 10, (0, 0, 255), -1)  # Marquer le point détecté

        cv2.imshow("Calibration", frame)
        key = cv2.waitKey(1) & 0xFF

        # Si 'espace' est pressé, enregistrer la position détectée
        if key == ord(" "):
            if yellow_position:
                print(f"Point {i+1} enregistré :", yellow_position)
                captured_points.append(yellow_position)
                break

# Convertir en array NumPy
captured_points = np.array(captured_points, dtype=np.float32)

# --- Étape 2 : Calcul de l’homographie ---
homography_matrix, _ = cv2.findHomography(captured_points, PROJECTED_POINTS)

print("Calibration terminée. Déplacez le stylo, la souris suivra.")

# --- Étape 3 : Suivi en temps réel du stylo et contrôle de la souris ---
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    yellow_position = get_yellow_position(frame)
    if yellow_position:
        # Appliquer la transformation d'homographie
        transformed_point = cv2.perspectiveTransform(
            np.array([[yellow_position]], dtype=np.float32), homography_matrix
        )[0][0]

        # Convertir en coordonnées écran (PC)
        screen_x = int((transformed_point[0] / 500) * SCREEN_WIDTH)
        screen_y = int((transformed_point[1] / 400) * SCREEN_HEIGHT)

        # Déplacer la souris
        pyautogui.moveTo(screen_x, screen_y)

    cv2.imshow("Suivi du stylo", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
