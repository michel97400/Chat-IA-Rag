#!/usr/bin/env python3
"""
Serveur HTTP simple pour servir le frontend
Lance le serveur sur http://localhost:3001
"""

import http.server
import socketserver
import os
import socket

# Configuration
PORT = 3001

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

def find_free_port(start_port=3001, max_tries=10):
    """Trouve un port libre à partir de start_port"""
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

if __name__ == "__main__":
    # Trouver un port disponible
    available_port = find_free_port(PORT)
    if available_port is None:
        print(f"❌ Aucun port disponible entre {PORT} et {PORT + 10}")
        exit(1)
    
    if available_port != PORT:
        print(f"⚠️  Port {PORT} occupé, utilisation du port {available_port}")
        PORT = available_port
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"\n🚀 Serveur Frontend démarré!")
        print(f"📍 URL: http://localhost:{PORT}")
        print(f"\n✅ Ouvrez votre navigateur à: http://localhost:{PORT}/index.html")
        print(f"\n⏹️  Appuyez sur Ctrl+C pour arrêter le serveur\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Serveur arrêté")
