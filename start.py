#!/usr/bin/env python3
"""
Script pour lancer les serveurs Backend et Frontend dans des terminaux separés
"""

import subprocess
import os
import sys
import time

# Chemins
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(SCRIPT_DIR, "Backend")
FRONTEND_DIR = os.path.join(SCRIPT_DIR, "Frontend")

print("=" * 50)
print("   Lancement Chat IA Diabète")
print("=" * 50)
print()
print("🚀 Démarrage des serveurs...")
print()

try:
    # Lancer le Backend dans un nouveau terminal
    print("📍 Lancement du Backend...")
    backend_cmd = ['cmd', '/c', 'start', 'cmd', '/k', 'python -m uvicorn main:app --reload --port 8000']
    subprocess.Popen(
        backend_cmd,
        cwd=BACKEND_DIR
    )
    
    # Attendre 3 secondes
    time.sleep(3)
    
    # Lancer le Frontend dans un nouveau terminal
    print("📍 Lancement du Frontend...")
    frontend_cmd = ['cmd', '/c', 'start', 'cmd', '/k', 'python serve.py']
    subprocess.Popen(
        frontend_cmd,
        cwd=FRONTEND_DIR
    )
    
    print()
    print("✅ Les deux serveurs sont en cours de lancement !")
    print()
    print("📍 Terminal 1 : Backend FastAPI sur http://localhost:8000")
    print("📍 Terminal 2 : Frontend sur http://localhost:3001")
    print()
    print("🌐 Ouvrez votre navigateur à : http://localhost:3001/index.html")
    print()
    print("Pour arrêter les serveurs, fermez les deux fenêtres de terminal.")
    print()
    
except Exception as e:
    print(f"❌ Erreur : {e}")
    sys.exit(1)
