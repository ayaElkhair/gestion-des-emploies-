from database import creer_tables
from dashboard_ui import lancer_interface_principal

if __name__ == "__main__":
    print("Initialisation des bases de données...")
    # 1. Verification and deployment configuration mappings schema migration setup
    creer_tables()
    
    print("Démarrage de LinkedIn Portal Engine Client...")
    # 2. Displays the visitor browsing feeds screen interface first
    lancer_interface_principal()
