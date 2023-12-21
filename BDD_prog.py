import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import sqlite3
import subprocess


class GestionBaseDeDonneesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Base de Données")

        # Utilisation du thème "clam"
        style = ttk.Style()
        style.configure("Treeview.Heading", anchor="w")
        style.theme_use("clam")
        
        # la bar du menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # juste le menu fichier
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Ouvrir", command=self.parcourir_dossier)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.root.destroy)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)

         # mon menu "Aide"
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Documentation", command=self.open_documentation)
        self.menu_bar.add_cascade(label="Aide", menu=self.help_menu)
        
        # Connexion ou création de la base de données
        self.conn = sqlite3.connect('base_de_donnees.db')
        self.c = self.conn.cursor()

        # Création de la table si elle n'existe pas
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS fichiers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                chemin TEXT,
                date_creation TEXT,
                date_modification TEXT,
                type TEXT,
                taille INTEGER
            )
        ''')
        self.conn.commit()

        # Création de l'interface utilisateur
        self.tree = ttk.Treeview(self.root, columns=('ID','Nom', 'Chemin', 'Date de Création', 'Date de Modification', 'Type', 'Taille'))
        #self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Nom')
        self.tree.heading('#2', text='Chemin')
        self.tree.heading('#3', text='Date de Création')
        self.tree.heading('#4', text='Date de Modification')
        self.tree.heading('#5', text='Type')
        self.tree.heading('#6', text='Taille')
        self.tree.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=10)

        # Option de tri
        tri_options = ['Nom', 'Type', 'Taille', 'Date de Création', 'Date de Modification']
        self.tri_var = tk.StringVar()
        self.tri_var.set(tri_options[0])  # Valeur par défaut
        tri_menu = tk.OptionMenu(self.root, self.tri_var, *tri_options)
        tri_menu.pack(pady=10)

        # Initialisation de colonne_tri_sql dans __init__
        self.colonne_tri_sql = 'nom'

        # Frame pour les boutons
        boutons_frame = tk.Frame(self.root)
        boutons_frame.pack(pady=10)

        # Boutons d'action sans images
        parcourir_button = tk.Button(boutons_frame, text="Parcourir", command=self.parcourir_dossier)
        parcourir_button.pack(side=tk.LEFT, padx=5)

        tri_button = tk.Button(boutons_frame, text="Trier", command=self.tri)
        tri_button.pack(side=tk.LEFT, padx=5)

        suppression_button = tk.Button(boutons_frame, text="Supprimer", command=self.supprimer)
        suppression_button.pack(side=tk.LEFT, padx=5)

        # Bouton basculant pour l'ordre croissant/décroissant
        self.ordre_toggle = tk.BooleanVar(value=True)  # True pour ASC (ordre croissant)
        self.ordre_button = tk.Button(boutons_frame, text="Ordre Croissant", command=self.toggle_ordre)
        self.ordre_button.pack(side=tk.LEFT, padx=5)
        
        # Champ de saisie pour la recherche par nom
        self.recherche_entry = tk.Entry(boutons_frame, width=30)
        self.recherche_entry.pack(side=tk.LEFT, padx=5)

        # Bouton de recherche par nom
        recherche_button = tk.Button(boutons_frame, text="Rechercher par Nom", command=self.rechercher_par_nom)
        recherche_button.pack(side=tk.LEFT, padx=5)

        # Affichage initial des données
        self.afficher_donnees()

    def afficher_donnees(self):
        self.tree.delete(*self.tree.get_children())
        #self.tri()
        for row in self.c.fetchall():
            self.tree.insert('', 'end', values=row[1:])

    def tri(self):
        colonne_tri = self.tri_var.get().lower().replace(' ', '_')
        ordre_tri = 'ASC' if self.ordre_toggle.get() else 'DESC'

        if colonne_tri in ['taille', 'date_creation', 'date_modification']:
            colonne_tri_sql = colonne_tri
        elif colonne_tri == 'nom':
            colonne_tri_sql = 'nom'
        elif colonne_tri == 'type':
            colonne_tri_sql = 'type, nom'
        else:
            # Ajouter les noms de colonnes en minuscules
            colonne_tri_sql = colonne_tri

        query = f'SELECT ID, nom, chemin, date_creation, date_modification, type, taille FROM fichiers ORDER BY {colonne_tri_sql} {ordre_tri}'
        self.c.execute(query)
        self.afficher_donnees()

    def toggle_ordre(self):
        # Basculer entre ordre croissant et décroissant
        self.ordre_toggle.set(not self.ordre_toggle.get())
        ordre_button_text = "Ordre Croissant" if self.ordre_toggle.get() else "Ordre Décroissant"
        self.ordre_button.config(text=ordre_button_text)
        self.tri()

    def supprimer(self):
        try:
            selection = self.tree.selection()[0]
        except IndexError:
            messagebox.showinfo("Information", "Aucun fichier sélectionné.")
            return
        
        nom_fichier = self.tree.item(selection, 'values')[1]
        confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le fichier '{nom_fichier}' ?")
        if confirmation:
            self.c.execute("DELETE FROM fichiers WHERE nom=?", (nom_fichier,))
            self.conn.commit()
            self.tree.delete(selection)

    def parcourir_dossier(self):
        folder_path = filedialog.askdirectory()
        print("Dossier sélectionné:", folder_path)

        fichiers = self.parcourir_dossier_impl(folder_path)

        for fichier in fichiers:
            self.c.execute('''
                INSERT INTO fichiers (nom, chemin, date_creation, date_modification, type, taille)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (fichier['nom'], fichier['chemin'], fichier['date_creation'], fichier['date_modification'], fichier['type'], fichier['taille']))

        self.conn.commit()
        self.afficher_donnees()

    def parcourir_dossier_impl(self, dossier):
        fichiers = []
        for dossier_actuel, sous_dossiers, fichiers_actuels in os.walk(dossier):
            for fichier in fichiers_actuels:
                chemin_complet = os.path.join(dossier_actuel, fichier)
                fichiers.append({
                    'nom': fichier,
                    'chemin': chemin_complet,
                    'date_creation': os.path.getctime(chemin_complet),
                    'date_modification': os.path.getmtime(chemin_complet),
                    'type': os.path.splitext(fichier)[1],
                    'taille': os.path.getsize(chemin_complet)
                })
        return fichiers
    
    def rechercher_par_nom(self):
        nom_recherche = self.recherche_entry.get()
        if nom_recherche:
            nom_recherche = f"%{nom_recherche}%"  # Ajouter des jokers % pour correspondance partielle
            query = "SELECT * FROM fichiers WHERE nom LIKE ?"
            self.c.execute(query, (nom_recherche,))
            self.afficher_donnees()
        else:
            # Si aucun nom n'est saisi, afficher tous les fichiers
            self.c.execute("SELECT * FROM fichiers")
            self.afficher_donnees()
            
    def open_documentation(self):
        documentation_path = "/Users/nawfoelardjoune/M1/script/doc.txt" # a changer si besoin
        subprocess.run(["open", documentation_path], check=True) # comme si je tapais dans mon terminale


if __name__ == "__main__":
    root = tk.Tk()
    app = GestionBaseDeDonneesApp(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)  # Fermer correctement la fenêtre
    root.mainloop()
