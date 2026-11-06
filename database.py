import sqlite3

def connexion():
    db = sqlite3.connect("emploi.db")
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db

def creer_tables():
    db = connexion()
    a = db.cursor()
    
    a.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Candidat', 'Entreprise'))
        )
    """)
    
    a.execute("""
        CREATE TABLE IF NOT EXISTS offres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_entreprise INTEGER NOT NULL,
            titre_poste TEXT NOT NULL,
            type_contrat TEXT,
            salaire TEXT,
            FOREIGN KEY (id_entreprise) REFERENCES utilisateurs(id) ON DELETE CASCADE
        )
    """)
    
    a.execute("""
        CREATE TABLE IF NOT EXISTS candidatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_offre INTEGER NOT NULL,
            id_candidat INTEGER NOT NULL,
            date_postulation TEXT NOT NULL,
            FOREIGN KEY (id_offre) REFERENCES offres(id) ON DELETE CASCADE,
            FOREIGN KEY (id_candidat) REFERENCES utilisateurs(id) ON DELETE CASCADE
        )
    """)
    db.commit()
    db.close()

def inscription(nom, email, password, role):
    db = connexion()
    c = db.cursor()
    try:
        c.execute("INSERT INTO utilisateurs (nom, email, password, role) VALUES (?, ?, ?, ?)", (nom, email, password, role))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()

def verifier_login(email, password):
    db = connexion()
    c = db.cursor()
    c.execute("SELECT * FROM utilisateurs WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone() #recuperer une seule ligne de ca
    db.close()
    return user

def ajouter_offre(id_entreprise, titre_poste, type_contrat, salaire):
    db = connexion()
    c = db.cursor()
    c.execute("INSERT INTO offres (id_entreprise, titre_poste, type_contrat, salaire) VALUES (?, ?, ?, ?)", (id_entreprise, titre_poste, type_contrat, salaire))
    db.commit()
    db.close()

def ajouter_candidature(id_offre, id_candidat, date_postulation):
    db = connexion()
    c = db.cursor()
    c.execute("INSERT INTO candidatures (id_offre, id_candidat, date_postulation) VALUES (?, ?, ?)", (id_offre, id_candidat, date_postulation))
    db.commit()
    db.close()

def get_tous_les_offres():
    db = connexion()
    c = db.cursor()
    c.execute("""
        SELECT offres.id, utilisateurs.nom AS entreprise, offres.titre_poste, offres.type_contrat, offres.salaire 
        FROM offres 
        JOIN utilisateurs ON offres.id_entreprise = utilisateurs.id
    """)
    offres = c.fetchall() #recuperer toutes les lignes
    db.close()
    return offres

def get_offres_par_entreprise(id_entreprise):
    db = connexion()
    c = db.cursor()
    c.execute("SELECT * FROM offres WHERE id_entreprise = ?", (id_entreprise,))
    offres = c.fetchall()
    db.close()
    return offres

def get_candidatures_pour_entreprise(id_entreprise):
    db = connexion()
    c = db.cursor()
    c.execute("""
        SELECT candidatures.id, offres.titre_poste, utilisateurs.nom AS candidat, utilisateurs.email AS candidat_email, candidatures.date_postulation
        FROM candidatures
        JOIN offres ON candidatures.id_offre = offres.id
        JOIN utilisateurs ON candidatures.id_candidat = utilisateurs.id
        WHERE offres.id_entreprise = ?
    """, (id_entreprise,))
    candidatures = c.fetchall()
    db.close()
    return candidatures

