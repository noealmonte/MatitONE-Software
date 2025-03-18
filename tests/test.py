import customtkinter as ctk  # Importation de customtkinter

# Configuration générale
ctk.set_appearance_mode("dark")  # Options: "light" ou "dark"
ctk.set_default_color_theme("blue")  # Choix de thème : "blue", "green", "dark-blue"

# Créer l'application principale
app = ctk.CTk()  # Remplace tk.Tk()
app.title("Exemple customtkinter")
app.geometry("400x300")  # Taille de la fenêtre

# Étiquette
label = ctk.CTkLabel(app, text="Bienvenue sur l'exemple customtkinter !", font=("Helvetica", 16))
label.pack(pady=20)  # Ajoute un espace autour de l'étiquette

# Champ de saisie
entry = ctk.CTkEntry(app, placeholder_text="Entrez votre texte ici")
entry.pack(pady=10)

# Fonction à appeler lors du clic sur le bouton
def on_button_click():
    user_text = entry.get()  # Récupère le texte saisi
    label.configure(text=f"Vous avez saisi : {user_text}")

# Bouton
button = ctk.CTkButton(app, text="Valider", command=on_button_click)
button.pack(pady=10)

# Bouton de sortie
exit_button = ctk.CTkButton(app, text="Quitter", command=app.quit)
exit_button.pack(pady=10)

# Lancer l'application
app.mainloop()
