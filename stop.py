#!/usr/bin/env python3
"""
Script pour arrêter tous les serveurs et nettoyer les ports
"""

import subprocess
import sys

print("=" * 50)
print("   Nettoyage des serveurs")
print("=" * 50)
print()

try:
    # Tuer tous les processus Python sur les ports 8000 et 3001
    print("🧹 Arrêt des processus sur les ports 8000 et 3001...")
    
    # Commande PowerShell pour tuer les processus
    ps_command = """
    Get-NetTCPConnection -LocalPort 8000,3001 -State Listen -ErrorAction SilentlyContinue | 
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    """
    
    subprocess.run(['powershell', '-Command', ps_command], check=False)
    
    print("✅ Ports nettoyés !")
    print()
    print("Vous pouvez maintenant relancer avec: python start.py")
    
except Exception as e:
    print(f"❌ Erreur : {e}")
    sys.exit(1)
