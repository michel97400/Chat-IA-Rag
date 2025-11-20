# Chat-IA-Rag - Assistant IA sur le Diabète

Un système RAG (Retrieval-Augmented Generation) avec API FastAPI pour répondre aux questions sur le diabète en utilisant des sources officielles françaises et internationales.

## 📋 Description

Ce projet combine :
- **Scraping** de données médicales depuis des sources officielles
- **RAG (Retrieval-Augmented Generation)** avec LlamaIndex et Groq
- **API REST** avec FastAPI pour interroger le système
- **Évaluation** de la qualité des réponses

## 🏗️ Architecture

```
Chat-IA-Rag/
├── Backend/
│   ├── main.py                 # API FastAPI
│   ├── controller.py           # Contrôleurs de l'API
│   ├── crud.py                 # Logique RAG
│   ├── schema.py               # Schémas Pydantic
│   ├── model.py                # Modèles de données
│   ├── Scrapping/
│   │   └── Scrapping.py        # Script de collecte des données
│   ├── Test_Model/
│   │   └── groq_rag.py         # Tests RAG en ligne de commande
│   └── data/
│       └── scraped_data.json   # Données collectées
├── Frontend/
│   ├── index.html              # Interface utilisateur
│   ├── css/
│   │   └── style.css           # Styles Neo-brutalism
│   ├── js/
│   │   └── app.js              # Logique JavaScript
│   └── serve.py                # Serveur HTTP Python
├── data/                       # Dossier data alternatif
├── .env                        # Configuration (API keys)
├── requirements.txt            # Dépendances Python
└── README.md
```

## 🔧 Installation

### Prérequis

- Python 3.8+
- Ollama installé localement (pour les embeddings)
- Compte Groq (pour le LLM)

### Étapes

1. **Cloner le projet**
```bash
git clone https://github.com/michel97400/Chat-IA-Rag.git
cd Chat-IA-Rag
```

2. **Créer l'environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Installer et configurer Ollama**
```bash
# Télécharger Ollama depuis https://ollama.ai
# Puis télécharger le modèle d'embeddings
ollama pull bge-m3
```

6. **Configurer les variables d'environnement**

Créer un fichier `.env` à la racine :
```env
GROQ_API_KEY=votre_clé_api_groq
```

Pour obtenir une clé API Groq : https://console.groq.com

## 🚀 Utilisation

### 1. Collecter les données (première fois uniquement)

```bash
cd Backend/Scrapping
python Scrapping.py
```

⏱️ *Temps estimé : 5-10 minutes*

Les données seront sauvegardées dans `Backend/data/scraped_data.json`

### 2. Lancer l'API FastAPI

```bash
cd Backend
uvicorn main:app --reload
```

L'API sera accessible sur : http://localhost:8000

📖 Documentation interactive : http://localhost:8000/docs

### 3. Lancer le Frontend

Le frontend dispose d'un serveur Python intégré pour faciliter le développement.

```bash
cd Frontend
python serve.py
```

Le frontend sera accessible sur : http://localhost:8080

**Ou utilisez le chemin absolu :**
```bash
python "c:\Users\flavi\OneDrive\Documents\Simplon\Projet\Rag_Diabète\Chat-IA-Rag\Frontend\serve.py"
```

**Alternative avec Live Server (VS Code) :**
- Installez l'extension "Live Server" dans VS Code
- Clic droit sur `Frontend/index.html`
- Sélectionnez "Open with Live Server"

### 4. Tester le RAG en ligne de commande (optionnel)

```bash
cd Backend/Test_Model
python groq_rag.py
```

## 📡 Endpoints de l'API

### GET `/`
Vérifier le statut de l'API
```bash
curl http://localhost:8000/
```

### POST `/query`
Poser une question au RAG

**Corps de la requête :**
```json
{
  "question": "Quels sont les symptômes du diabète de type 2 ?"
}
```

**Exemple avec curl :**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Quels sont les symptômes du diabète de type 2 ?"}'
```

**Réponse :**
```json
{
  "question": "Quels sont les symptômes du diabète de type 2 ?",
  "response": "Les symptômes du diabète de type 2 incluent...",
  "retrieved_docs": [
    {
      "url": "https://...",
      "content": "..."
    }
  ]
}
```

### POST `/evaluate`
Évaluer la qualité du RAG

**Corps de la requête :**
```json
{
  "question": "Quels sont les symptômes du diabète ?",
  "expected_answer": "Soif intense, fatigue, vision floue..."
}
```

**Réponse :**
```json
{
  "question": "...",
  "generated_answer": "...",
  "expected_answer": "...",
  "similarity_score": 0.85,
  "evaluation": "Bonne réponse"
}
```

## 🧪 Tests rapides

### Tester l'API avec Python

```python
import requests

# Poser une question
response = requests.post(
    "http://localhost:8000/query",
    json={"question": "Quelle est la prévalence du diabète en France ?"}
)
print(response.json())
```

### Tester avec PowerShell

```powershell
$body = @{
    question = "Quels sont les facteurs de risque du diabète ?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/query" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## 📊 Sources de données

Le système collecte des informations depuis :

- **Santé Publique France** : Données épidémiologiques
- **Haute Autorité de Santé (HAS)** : Recommandations cliniques
- **INSERM** : Recherche médicale
- **OMS** : Statistiques mondiales
- **Fédération Française des Diabétiques** : Information patients
- Et 25+ autres sources officielles

## 🛠️ Technologies utilisées

- **FastAPI** : Framework web moderne
- **LlamaIndex** : Framework RAG
- **Groq** : LLM (Llama 3.3 70B)
- **Ollama** : Embeddings locaux (BGE-M3)
- **Trafilatura** : Scraping web
- **scikit-learn** : Évaluation des réponses

## 📝 Structure de l'API

### Fichiers principaux

- **main.py** : Point d'entrée de l'API FastAPI
- **controller.py** : Gestion des endpoints
- **crud.py** : Logique RAG (création index, recherche, génération)
- **schema.py** : Schémas de validation des requêtes/réponses
- **model.py** : Modèles de données

## 🔍 Dépannage

### Erreur "GROQ_API_KEY non trouvée"
- Vérifiez que le fichier `.env` existe à la racine
- Vérifiez que la clé API est correcte

### Erreur "Ollama not found"
- Assurez-vous qu'Ollama est installé et en cours d'exécution
- Lancez `ollama serve` dans un terminal séparé

### Erreur "scraped_data.json non trouvé"
- Lancez d'abord le script de scraping
- Vérifiez que le fichier est dans `Backend/data/`

### L'API ne démarre pas
```bash
# Vérifier que le port 8000 est libre
netstat -ano | findstr :8000

# Ou utiliser un autre port
uvicorn main:app --port 8080
```

## 🚀 Commandes utiles

### Backend (API)
```bash
# Lancer l'API en mode développement
cd Backend
uvicorn main:app --reload

# Lancer l'API en production
uvicorn main:app --host 0.0.0.0 --port 8000

# Voir les logs détaillés
uvicorn main:app --log-level debug

# Lancer le scraping
cd Backend/Scrapping
python Scrapping.py

# Tester le RAG en CLI
cd Backend/Test_Model
python groq_rag.py
```

### Frontend
```bash
# Lancer le serveur Frontend (port 8080)
cd Frontend
python serve.py

# Ou avec chemin absolu
python "c:\...\Chat-IA-Rag\Frontend\serve.py"
```

### Utilisation complète
1. **Terminal 1** : Lancer l'API Backend
   ```bash
   cd Backend
   uvicorn main:app --reload
   ```

2. **Terminal 2** : Lancer le Frontend
   ```bash
   cd Frontend
   python serve.py
   ```

3. **Navigateur** : Ouvrir http://localhost:8080

## 📚 Documentation

- Documentation API : http://localhost:8000/docs
- Documentation alternative : http://localhost:8000/redoc
- Groq API : https://console.groq.com/docs
- LlamaIndex : https://docs.llamaindex.ai/

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## ⚠️ Avertissement

Ce système est un outil d'information uniquement. Il ne remplace pas l'avis d'un professionnel de santé. Consultez toujours un médecin pour toute question médicale.