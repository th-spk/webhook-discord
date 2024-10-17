import tkinter as tk
from tkinter import messagebox, ttk
import requests
import threading

# Fonction pour envoyer le message à tous les webhooks
def send_webhook():
    webhook_urls = url_entry.get("1.0", tk.END).strip().splitlines()  # Récupère les URLs du Webhook
    message_content = message_entry.get("1.0", tk.END).strip()  # Récupère le contenu du message
    username = username_entry.get()  # Récupère le nom d'utilisateur
    avatar_url = avatar_entry.get()  # Récupère l'URL de l'avatar
    embed_title = embed_title_entry.get()  # Récupère le titre de l'embed
    embed_description = embed_desc_entry.get("1.0", tk.END).strip()  # Récupère la description de l'embed
    image_url = image_entry.get()  # Récupère l'URL de l'image
    spam_count = int(spam_count_entry.get())  # Récupère le nombre de fois à envoyer le message

    if not webhook_urls or not message_content:
        messagebox.showwarning("Erreur", "Les URLs du webhook et le message ne peuvent pas être vides.")
        return

    def send_requests():
        for _ in range(spam_count):
            for webhook_url in webhook_urls:
                if webhook_url.strip():
                    data = {
                        "content": message_content,
                        "username": username,
                        "avatar_url": avatar_url,
                    }

                    # Ajouter un embed s'il y a un titre ou une description d'embed
                    if embed_title or embed_description or image_url:
                        embed = {
                            "title": embed_title,
                            "description": embed_description,
                            "image": {"url": image_url} if image_url else {},
                        }
                        data["embeds"] = [embed]

                    try:
                        response = requests.post(webhook_url.strip(), json=data)
                        response.raise_for_status()  # Vérifie si la requête est réussie
                        print(f"Message envoyé à {webhook_url}")
                    except requests.exceptions.HTTPError as err:
                        print(f"Erreur lors de l'envoi au {webhook_url} : {err}")

        messagebox.showinfo("Succès", "Messages envoyés avec succès !")

    # Crée un thread pour exécuter l'envoi de messages sans bloquer l'interface
    threading.Thread(target=send_requests).start()

# Création de la fenêtre principale
window = tk.Tk()
window.title("Webhook Discord Manager")
window.geometry("700x700")
window.config(bg="#2e2e2e")  # Couleur de fond sombre pour un design moderne

# Style
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', foreground="white", background="#2e2e2e", font=('Helvetica', 11))

# Titre principal
title_label = tk.Label(window, text="Webhook Discord Manager", font=("Helvetica", 20, "bold"), bg="#2e2e2e", fg="white")
title_label.pack(pady=20)

# Section URLs des Webhooks
url_frame = tk.LabelFrame(window, text="URLs des Webhooks Discord", bg="#2e2e2e", fg="white", font=("Helvetica", 14))
url_frame.pack(fill="both", padx=20, pady=10)

url_entry = tk.Text(url_frame, height=5, width=80, bg="#444", fg="white", font=("Helvetica", 10))
url_entry.pack(pady=5)

# Section Message à envoyer
message_frame = tk.LabelFrame(window, text="Message à envoyer", bg="#2e2e2e", fg="white", font=("Helvetica", 14))
message_frame.pack(fill="both", padx=20, pady=10)

message_entry = tk.Text(message_frame, height=5, width=80, bg="#444", fg="white", font=("Helvetica", 10))
message_entry.pack(pady=5)

# Section Personnalisation
custom_frame = tk.LabelFrame(window, text="Personnalisation", bg="#2e2e2e", fg="white", font=("Helvetica", 14))
custom_frame.pack(fill="both", padx=20, pady=10)

username_label = ttk.Label(custom_frame, text="Nom d'utilisateur du bot  :")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
username_entry = tk.Entry(custom_frame, width=40, bg="#444", fg="white")
username_entry.grid(row=0, column=1, padx=5, pady=5)

avatar_label = ttk.Label(custom_frame, text="URL de l'avatar du bot (facultatif) :")
avatar_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
avatar_entry = tk.Entry(custom_frame, width=40, bg="#444", fg="white")
avatar_entry.grid(row=1, column=1, padx=5, pady=5)

# Section Embed
embed_frame = tk.LabelFrame(window, text="Embed (facultatif)", bg="#2e2e2e", fg="white", font=("Helvetica", 14))
embed_frame.pack(fill="both", padx=20, pady=10)

embed_title_label = ttk.Label(embed_frame, text="Titre de l'embed :")
embed_title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
embed_title_entry = tk.Entry(embed_frame, width=40, bg="#444", fg="white")
embed_title_entry.grid(row=0, column=1, padx=5, pady=5)

embed_desc_label = ttk.Label(embed_frame, text="Description de l'embed :")
embed_desc_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
embed_desc_entry = tk.Text(embed_frame, height=3, width=60, bg="#444", fg="white")
embed_desc_entry.grid(row=1, column=1, padx=5, pady=5)

image_label = ttk.Label(embed_frame, text="URL de l'image :")
image_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
image_entry = tk.Entry(embed_frame, width=40, bg="#444", fg="white")
image_entry.grid(row=2, column=1, padx=5, pady=5)

# Section Spamming
spam_frame = tk.LabelFrame(window, text="Paramètres de Spam", bg="#2e2e2e", fg="white", font=("Helvetica", 14))
spam_frame.pack(fill="both", padx=20, pady=10)

spam_count_label = ttk.Label(spam_frame, text="Nombre de fois à envoyer :")
spam_count_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
spam_count_entry = tk.Entry(spam_frame, width=10, bg="#444", fg="white")
spam_count_entry.grid(row=0, column=1, padx=5, pady=5)
spam_count_entry.insert(0, "1")

# Bouton pour envoyer le message
send_button = ttk.Button(window, text="Envoyer", command=send_webhook)
send_button.pack(pady=20)

# Boucle principale de l'interface Tkinter
window.mainloop()
