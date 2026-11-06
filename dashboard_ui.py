import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import database as db

# Dynamic state tracking metrics
current_user = None
root_win = None
btn_auth_ref = None
lbl_welcome_ref = None
tree_offres = None
tree_mes_offres = None
tree_suivi = None

def lancer_interface_principal():
    global root_win, tree_offres, btn_auth_ref, lbl_welcome_ref
    root_win = tk.Tk()
    root_win.title("LinkedIn Morocco - Espace Emploi")
    root_win.geometry("850x650")
    root_win.configure(bg="white")

    # Header Bar Custom Layout 
    header = tk.Frame(root_win, bg="#1B4F72", height=60)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(header, text="Linked in", font=("Arial", 20, "bold"), fg="white", bg="#0A66C2").pack(side="left", padx=20, pady=10)
    
    #Authentication control module switch hook inside top strip
    btn_auth_ref = tk.Button(header, text="Se connecter / S'inscrire", bg="#E9F5FB", fg="#0A66C2", font=("Arial", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=declencher_login_portal)
    btn_auth_ref.pack(side="right", padx=20, pady=15)

    lbl_welcome_ref = tk.Label(header, text="Mode Invité", fg="white", bg="#1B4F72", font=("Arial", 11, "italic"))
    lbl_welcome_ref.pack(side="right", padx=10, pady=18)

    tk.Label(root_win, text="Offres d'Emploi Disponibles au Maroc", font=("Arial", 16, "bold"), fg="#1B4F72", bg="white").pack(pady=20)

    # Treeview setup layout structure container
    columns = ("id", "entreprise", "poste", "contrat", "salaire")
    tree_offres = ttk.Treeview(root_win, columns=columns, show="headings", height=15)
    tree_offres.pack(fill="both", expand=True, padx=25, pady=10)

    tree_offres.heading("id", text="ID Offre")
    tree_offres.heading("entreprise", text="Entreprise")
    tree_offres.heading("poste", text="Intitulé du Poste")
    tree_offres.heading("contrat", text="Type de Contrat")
    tree_offres.heading("salaire", text="Salaire (DH)")

    tree_offres.column("id", width=70, anchor="center")
    tree_offres.column("contrat", width=100, anchor="center")
    
    charger_offres_visiteur()

    # Apply Action Control Button
    tk.Button(root_win, text="Postuler à l'offre sélectionnée", bg="#0A66C2", fg="white", font=("Arial", 13, "bold"), bd=0, cursor="hand2", padx=25, pady=10, command=action_postuler_verification).pack(pady=25)

    root_win.mainloop()

def charger_offres_visiteur():
    if tree_offres is None:
        return
    for item in tree_offres.get_children():
        tree_offres.delete(item)
    for row in db.get_tous_les_offres():
        tree_offres.insert("", "end", values=(row['id'], row['entreprise'], row['titre_poste'], row['type_contrat'], row['salaire']))

def declencher_login_portal():
    import login
    login.ouvrir_fenetre_login(root_win)

def action_postuler_verification():
    global current_user
    # VALIDATION CHECKS FOR SYSTEM AUTH SESSION CODES
    if current_user is None:
        messagebox.showwarning("Connexion Requise", "Désolé! Tu doit faire login ou créer un compte afin que tu peux postuler.")
        declencher_login_portal()
        return

    if current_user['role'] == 'Entreprise':
        messagebox.showerror("Action Impossible", "Les comptes Entreprise peuvent pas postuler!")
        return

    selected = tree_offres.selection()
    if not selected:
        messagebox.showwarning("Attention", "Veuillez sélectionner une offre dans le tableau.")
        return
    
    values = tree_offres.item(selected, "values")
    id_offre = int(values[0])
    date_ajrd = datetime.today().strftime('%Y-%m-%d')

    db.ajouter_candidature(id_offre, current_user['id'], date_ajrd)
    messagebox.showinfo("Succès", "Votre candidature a été envoyée avec succès !")

def rafraichir_interface_apres_login(user):
    global current_user, btn_auth_ref, lbl_welcome_ref, root_win
    current_user = user
    
    # Update Header Metadata values
    lbl_welcome_ref.config(text=f"Connecté: {current_user['nom']} ({current_user['role']})", font=("Arial", 11, "bold"))
    btn_auth_ref.config(text="Se Déconnecter", bg="#E74C3C", fg="white", command=action_logout)

    # If the user logged in as an Enterprise manager, switch workflow to the workspace panel dashboard directly
    if current_user['role'] == 'Entreprise':
        ouvrir_panel_entreprise_dashboard()

def action_logout():
    global current_user, root_win
    messagebox.showinfo("Déconnexion", "Vous avez été déconnecté.")
    root_win.destroy()
    # Restart interface state from zero baseline configuration structures
    lancer_interface_principal()

def ouvrir_panel_entreprise_dashboard():
    global root_win, current_user
    global tree_mes_offres, tree_suivi

    # Open new overlay TopLevel workspace environment window pane
    ent_win = tk.Toplevel(root_win)
    ent_win.title(f"LinkedIn Business - Portal ({current_user['nom']})")
    ent_win.geometry("750x600")
    ent_win.configure(bg="white")
    ent_win.grab_set() # Focus lock on enterprise layout configurations

    notebook = ttk.Notebook(ent_win)
    notebook.pack(fill="both", expand=True, padx=15, pady=15)

    onglet_creer = tk.Frame(notebook, bg="white")
    onglet_mes_offres = tk.Frame(notebook, bg="white")
    onglet_suivi = tk.Frame(notebook, bg="white")

    notebook.add(onglet_creer, text=" PUBLIER UNE ANNONCE ")
    notebook.add(onglet_mes_offres, text=" NOS ANNONCES ")
    notebook.add(onglet_suivi, text=" CANDIDATURES REÇUES ")

    # ---- Form View Component Nodes Setup (Onglet Créer) ----
    tk.Label(onglet_creer, text="Publier une Nouvelle Offre d'Emploi", font=("Arial", 14, "bold"), fg="#0A66C2", bg="white").pack(pady=20)
    form_frame = tk.Frame(onglet_creer, bg="white")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Intitulé du Poste * :", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=0, column=0, sticky="w", pady=10)
    entry_poste = tk.Entry(form_frame, width=35, bd=1, relief="solid")
    entry_poste.grid(row=0, column=1, pady=10, padx=15)

    tk.Label(form_frame, text="Type de Contrat:", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=1, column=0, sticky="w", pady=10)
    entry_contrat = tk.Entry(form_frame, width=35, bd=1, relief="solid")
    entry_contrat.grid(row=1, column=1, pady=10, padx=15)

    tk.Label(form_frame, text="Salaire proposé (DH):", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=2, column=0, sticky="w", pady=10)
    entry_salaire = tk.Entry(form_frame, width=35, bd=1, relief="solid")
    entry_salaire.grid(row=2, column=1, pady=10, padx=15)

    # ---- Setup Table columns for "NOS ANNONCES" ----
    cols_mes_offres = ("id", "poste", "contrat", "salaire")
    tree_mes_offres = ttk.Treeview(onglet_mes_offres, columns=cols_mes_offres, show="headings")
    tree_mes_offres.pack(fill="both", expand=True, padx=15, pady=15)
    tree_mes_offres.heading("id", text="ID")
    tree_mes_offres.heading("poste", text="Poste")
    tree_mes_offres.heading("contrat", text="Contrat")
    tree_mes_offres.heading("salaire", text="Salaire (DH)")
    tree_mes_offres.column("id", width=60, anchor="center")

    # ---- Setup Table columns for "CANDIDATURES REÇUES" ----
    cols_suivi = ("id", "poste", "candidat", "email", "date")
    tree_suivi = ttk.Treeview(onglet_suivi, columns=cols_suivi, show="headings")
    tree_suivi.pack(fill="both", expand=True, padx=15, pady=15)
    tree_suivi.heading("id", text="ID")
    tree_suivi.heading("poste", text="Poste Demandé")
    tree_suivi.heading("candidat", text="Nom Candidat")
    tree_suivi.heading("email", text="Email")
    tree_suivi.heading("date", text="Date Postulation")
    tree_suivi.column("id", width=60, anchor="center")

    # Function to fetch and reload corporate workspaces arrays
    def rafraichir_tables_entreprise():
        for item in tree_mes_offres.get_children(): tree_mes_offres.delete(item)
        for row in db.get_offres_par_entreprise(current_user['id']):
            tree_mes_offres.insert("", "end", values=(row['id'], row['titre_poste'], row['type_contrat'], row['salaire']))
        
        for item in tree_suivi.get_children(): tree_suivi.delete(item)
        for row in db.get_candidatures_pour_entreprise(current_user['id']):
            tree_suivi.insert("", "end", values=(row['id'], row['titre_poste'], row['candidat'], row['candidat_email'], row['date_postulation']))

    def publier_offre_action():
        poste = entry_poste.get().strip()
        contrat = entry_contrat.get().strip()
        salaire = entry_salaire.get().strip()
        if not poste:
            messagebox.showwarning("Attention", "Veuillez remplir l'intitulé du poste.")
            return
        
        db.ajouter_offre(current_user['id'], poste, contrat, salaire)
        messagebox.showinfo("Succès", "Offre d'emploi publiée avec succès !")
        
        entry_poste.delete(0, tk.END)
        entry_contrat.delete(0, tk.END)
        entry_salaire.delete(0, tk.END)
        
        # Reload views dynamically
        rafraichir_tables_entreprise()
        charger_offres_visiteur()

    tk.Button(onglet_creer, text="Diffuser l'Annonce", bg="#0A66C2", fg="white", font=("Arial", 11, "bold"), bd=0, cursor="hand2", padx=15, pady=5, command=publier_offre_action).pack(pady=20)

    # Initial loading when workspace opens up
    rafraichir_tables_entreprise()
