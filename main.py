import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, ttk

def search_games(query):
    search_url = f"https://steamrip.com/?s={query.replace(' ', '+')}"
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('a', class_='all-over-thumb-link')

        game_info = []
        for result in results:
            title = result.find('span').text
            link = 'https://steamrip.com/' + result['href']
            game_info.append((title, link))

        return game_info
    else:
        messagebox.showerror("Erreur", f"Erreur lors de la requête: {response.status_code}")
        return []

def show_game_details(link):
    response = requests.get(link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        download_links = soup.find_all('a', class_='shortc-button')
        details = soup.find('div', class_='plus tie-list-shortcode').text.strip()

        # Mettre à jour la page de détails
        details_text.set(details)

        # Effacer les liens précédents
        for widget in download_links_frame.winfo_children():
            widget.destroy()

        # Ajouter les nouveaux liens de téléchargement
        for dl_link in download_links:
            dl_button = ttk.Button(download_links_frame, text="Télécharger", command=lambda l=dl_link['href']: open_url(l))
            dl_button.pack(side="left", padx=5)

        # Afficher la page de détails
        main_frame.pack_forget()
        details_frame.pack(fill="both", expand=True)
    else:
        messagebox.showerror("Erreur", f"Erreur lors de la requête: {response.status_code}")

def open_url(url):
    import webbrowser
    webbrowser.open(url)

def on_select(event):
    selection = results_listbox.selection()
    if selection:
        item = results_listbox.item(selection[0])
        game_link = item['tags'][0]
        show_game_details(game_link)

def back_to_main():
    details_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Recherche de Jeux SteamRIP")
root.geometry("600x400")

# Style
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), padding=5)
style.configure("TButton", font=("Helvetica", 12), padding=5)
style.configure("Treeview", font=("Helvetica", 10))

# Frame principal
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# Étiquette et champ de recherche
search_label = ttk.Label(main_frame, text="Rechercher un jeu :")
search_label.pack(anchor="w")

search_entry = ttk.Entry(main_frame, width=50)
search_entry.pack(pady=5, fill="x")

# Bouton de recherche
search_button = ttk.Button(main_frame, text="Rechercher", command=lambda: display_results(search_entry.get()))
search_button.pack(pady=5)

# Séparateur
separator = ttk.Separator(main_frame, orient="horizontal")
separator.pack(fill="x", pady=10)

# Liste des résultats avec Treeview pour une meilleure apparence
results_listbox = ttk.Treeview(main_frame, columns=("Title",), show="headings", height=15)
results_listbox.heading("Title", text="Titre")
results_listbox.column("Title", width=500)
results_listbox.pack(pady=10, fill="both", expand=True)
results_listbox.bind('<<TreeviewSelect>>', on_select)

def display_results(query):
    # Effacer les résultats précédents
    for item in results_listbox.get_children():
        results_listbox.delete(item)

    # Effectuer la recherche
    game_info = search_games(query)

    # Afficher les résultats
    for title, link in game_info:
        results_listbox.insert("", "end", values=(title,), tags=(link,))

# Frame de détails
details_frame = ttk.Frame(root, padding="10")

# Texte des détails
details_text = tk.StringVar()
details_label = ttk.Label(details_frame, textvariable=details_text, wraplength=550, justify="left")
details_label.pack(pady=10, fill="both", expand=True)

# Frame pour les liens de téléchargement
download_links_frame = ttk.Frame(details_frame)
download_links_frame.pack(pady=5, fill="x")

# Bouton retour
back_button = ttk.Button(details_frame, text="Retour", command=back_to_main)
back_button.pack(pady=5)

# Lancer la boucle principale
root.mainloop()
