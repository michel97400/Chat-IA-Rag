#!/usr/bin/env python3
"""
Serveur HTTP simple pour servir le frontend
Lance le serveur sur http://localhost:3000
"""

import http.server
import socketserver
import os
import sys

# Configuration
PORT = 8080

# S'assurer qu'on est dans le bon dossier
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

print(f"📁 Dossier de travail: {os.getcwd()}")
print(f"📄 Fichiers disponibles: {os.listdir('.')}")

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SCRIPT_DIR, **kwargs)
    
    def end_headers(self):
        # Ajouter les headers CORS pour permettre les requêtes vers l'API
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"\n🚀 Serveur démarré!")
        print(f"📍 URL: http://localhost:{PORT}")
        print(f"\n✅ Ouvrez votre navigateur à: http://localhost:{PORT}/index.html")
        print(f"\n⏹️  Appuyez sur Ctrl+C pour arrêter le serveur\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Serveur arrêté")
