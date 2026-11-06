import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import database as db
import dashboard_ui

def ouvrir_fenetre_login(parent_win):
    global win_login
    win_login = tk.Toplevel(parent_win) #fenetre secondaire
    win_login.title("LinkedIn - Authentification Portal")
    win_login.geometry("380x420")
    win_login.configure(bg="white")
    win_login.grab_set() # Window focus capture lock execution layer node hook

    tk.Label(win_login, text="Linked in", font=("Arial", 26, "bold"), fg="#0A66C2", bg="white").pack(pady=15)
    
    frame = tk.Frame(win_login, bg="white")
    frame.pack(pady=10)

    tk.Label(frame, text="Email:", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=0, column=0, sticky="w", pady=10)
    global entry_email
    entry_email = tk.Entry(frame, width=28, bd=1, relief="solid")
    entry_email.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame, text="Mot de passe:", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=1, column=0, sticky="w", pady=10)
    global entry_password
    entry_password = tk.Entry(frame, width=28, show="*", bd=1, relief="solid")
    entry_password.grid(row=1, column=1, pady=10, padx=10)

    tk.Button(win_login, text="Se connecter", bg="#0A66C2", fg="white", font=("Arial", 12, "bold"), bd=0, width=22, cursor="hand2", command=action_login_submit).pack(pady=15)
    tk.Button(win_login, text="Créer un nouveau compte", bg="#E9F5FB", fg="#0A66C2", font=("Arial", 10, "bold"), bd=0, width=22, cursor="hand2", command=ouvrir_interface_inscription).pack()

def ouvrir_interface_inscription():
    global win_register
    win_register = tk.Toplevel(win_login)
    win_register.title("Créer un compte")
    win_register.geometry("380x460")
    win_register.configure(bg="white")
    win_register.grab_set()

    tk.Label(win_register, text="Inscription", font=("Arial", 18, "bold"), fg="#0A66C2", bg="white").pack(pady=15)

    frame = tk.Frame(win_register, bg="white")
    frame.pack(pady=10)

    tk.Label(frame, text="Nom complet / Entreprise:", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=0, column=0, sticky="w", pady=10)
    global reg_nom
    reg_nom = tk.Entry(frame, width=22, bd=1, relief="solid")
    reg_nom.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame, text="Email:", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=1, column=0, sticky="w", pady=10)
    global reg_email
    reg_email = tk.Entry(frame, width=22, bd=1, relief="solid")
    reg_email.grid(row=1, column=1, pady=10, padx=10)

    tk.Label(frame, text="Mot de passe:", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=2, column=0, sticky="w", pady=10)
    global reg_password
    reg_password = tk.Entry(frame, width=22, show="*", bd=1, relief="solid")
    reg_password.grid(row=2, column=1, pady=10, padx=10)

    tk.Label(frame, text="Type de compte:", font=("Arial", 10, "bold"), bg="white", fg="#566573").grid(row=3, column=0, sticky="w", pady=10)
    global reg_role
    reg_role = ttk.Combobox(frame, values=["Candidat", "Entreprise"], width=19, state="readonly")
    reg_role.current(0)
    reg_role.grid(row=3, column=1, pady=10, padx=10)

    tk.Button(win_register, text="S'inscrire", bg="#0A66C2", fg="white", font=("Arial", 12, "bold"), bd=0, width=22, command=action_inscription_submit).pack(pady=15)

def action_inscription_submit():
    nom = reg_nom.get()
    email = reg_email.get()
    pwd = reg_password.get()
    role = reg_role.get()

    if not nom or not email or not pwd:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
        return

    if db.inscription(nom, email, pwd, role):
        messagebox.showinfo("Succès", "Compte créé avec succès ! Vous pouvez vous connecter.")
        win_register.destroy()
    else:
        messagebox.showerror("Erreur", "Cet email est déjà utilisé.")

def action_login_submit():
    email = entry_email.get()
    pwd = entry_password.get()

    user = db.verifier_login(email, pwd)
    if user:
        messagebox.showinfo("Succès", f"Bienvenu {user['nom']} !")
        win_login.destroy()
        # Passes the session credentials dictionary mapping keys directly behind dashboard ui display pipelines
        dashboard_ui.rafraichir_interface_apres_login(user)
    else:
        messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
