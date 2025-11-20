# 🎨 Frontend - Assistant Diabète

Interface web moderne et responsive pour l'assistant IA sur le diabète.

## 📁 Structure

```
Frontend/
├── index.html          # Page principale
├── css/
│   └── style.css      # Styles modernes avec animations
└── js/
    └── app.js         # Logique de l'application
```

## ✨ Fonctionnalités

### 🎯 Interface Utilisateur
- **Design moderne** avec dégradés et animations fluides
- **Responsive** : s'adapte à tous les écrans (mobile, tablette, desktop)
- **Mode clair** avec palette de couleurs professionnelle
- **Animations** : transitions douces et effets visuels

### 💬 Chat Interactif
- Messages utilisateur et assistant différenciés
- **Indicateur de frappe** pendant le traitement
- **Scroll automatique** vers les nouveaux messages
- **Horodatage** de chaque message
- **Score d'évaluation** affiché pour chaque réponse

### 🚀 Suggestions Rapides
- 4 questions prédéfinies pour démarrer rapidement :
  - Symptômes du diabète
  - Prévention
  - Types de diabète
  - Alimentation

### 🔄 Fonctionnalités Avancées
- **Auto-resize** du champ de saisie
- **Envoi avec Entrée** (Shift+Entrée pour nouvelle ligne)
- **Clear chat** pour recommencer une conversation
- **Sauvegarde automatique** dans localStorage (optionnel)
- **Gestion d'erreurs** avec messages explicites

## 🚀 Lancement

### Option 1 : Live Server (Recommandé)
1. Installez l'extension **Live Server** dans VS Code
2. Clic droit sur `index.html` → "Open with Live Server"
3. Le navigateur s'ouvre automatiquement sur `http://127.0.0.1:5500/Frontend/index.html`

### Option 2 : Python HTTP Server
```bash
# Depuis le dossier Frontend
python -m http.server 8080

# Ouvrir dans le navigateur
# http://localhost:8080/index.html
```

### Option 3 : Ouvrir directement
Double-cliquez sur `index.html` (peut avoir des limitations CORS)

## ⚙️ Configuration

### URL de l'API
Par défaut, l'application se connecte à `http://127.0.0.1:8000`

Pour modifier l'URL, éditez `js/app.js` :
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

### CORS
Le backend doit avoir CORS activé (déjà configuré dans `Backend/main.py`)

## 🎨 Personnalisation

### Couleurs
Modifiez les variables CSS dans `css/style.css` :
```css
:root {
    --primary: #4F46E5;        /* Couleur principale */
    --secondary: #10B981;      /* Couleur secondaire */
    --bg-primary: #F9FAFB;     /* Fond principal */
    /* ... */
}
```

### Suggestions
Modifiez les suggestions dans `index.html` :
```html
<button class="suggestion-card" data-question="Votre question">
    <div class="suggestion-icon">🔍</div>
    <div class="suggestion-text">Titre</div>
</button>
```

## 🌐 API Endpoints Utilisés

### POST /query
Envoie une question et reçoit une réponse avec évaluation
```javascript
{
  "question": "Quels sont les symptômes du diabète ?"
}
```

Réponse :
```javascript
{
  "question": "...",
  "answer": "...",
  "evaluation": {
    "global_score": 0.85
  }
}
```

## 📱 Responsive Design

- **Desktop** (> 768px) : Layout complet avec toutes les fonctionnalités
- **Tablet** (768px) : Adaptation de l'interface
- **Mobile** (< 480px) : Interface optimisée pour petits écrans

## 🐛 Dépannage

### L'interface ne se charge pas
- Vérifiez que les fichiers CSS et JS sont bien présents
- Ouvrez la console du navigateur (F12) pour voir les erreurs

### Erreur de connexion à l'API
- Assurez-vous que le backend est lancé : `uvicorn main:app --reload`
- Vérifiez l'URL de l'API dans `js/app.js`
- Vérifiez que CORS est activé dans le backend

### Les messages ne s'affichent pas
- Ouvrez la console du navigateur (F12)
- Vérifiez les erreurs réseau dans l'onglet Network
- Testez l'API directement : http://127.0.0.1:8000/docs

## 🎯 Améliorations Futures

- [ ] Mode sombre
- [ ] Export de conversation en PDF
- [ ] Recherche dans l'historique
- [ ] Support du markdown dans les réponses
- [ ] Notification de nouvelles sources
- [ ] Traduction multilingue
- [ ] Synthèse vocale des réponses
- [ ] Upload de documents médicaux

## 📄 Licence

Projet éducatif - Informations médicales à titre informatif uniquement.

## 🤝 Contribution

Pour améliorer l'interface :
1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amélioration`)
3. Commitez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request
