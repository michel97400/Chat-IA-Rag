// Configuration de l'API
const API_BASE_URL = 'http://127.0.0.1:8000';

// Éléments DOM
const welcomeCard = document.getElementById('welcomeCard');
const chatContainer = document.getElementById('chatContainer');
const chatMessages = document.getElementById('chatMessages');
const typingIndicator = document.getElementById('typingIndicator');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const suggestionCards = document.querySelectorAll('.parent');

// État de l'application
let conversationHistory = [];
let isProcessing = false;

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Auto-resize textarea
    userInput.addEventListener('input', autoResizeTextarea);
    
    // Envoyer avec Entrée (Shift+Entrée pour nouvelle ligne)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
    
    // Bouton envoyer
    sendBtn.addEventListener('click', handleSendMessage);
    
    // Bouton clear
    clearBtn.addEventListener('click', handleClearChat);
    
    // Suggestions prédéfinies - modifier pour cibler .parent au lieu de .suggestion-card
    suggestionCards.forEach(parent => {
        parent.addEventListener('click', () => {
            const question = parent.getAttribute('data-question');
            userInput.value = question;
            handleSendMessage();
        });
    });
}

// Auto-resize textarea
function autoResizeTextarea() {
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
}

// Envoyer un message
async function handleSendMessage() {
    const question = userInput.value.trim();
    
    if (!question || isProcessing) return;
    
    // Masquer le welcome card si première question
    if (welcomeCard.style.display !== 'none') {
        welcomeCard.style.display = 'none';
        chatContainer.style.display = 'flex';
    }
    
    // Ajouter le message utilisateur
    addMessage('user', question);
    
    // Réinitialiser l'input
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Désactiver l'input pendant le traitement
    isProcessing = true;
    sendBtn.disabled = true;
    userInput.disabled = true;
    
    // Afficher l'indicateur de frappe
    typingIndicator.style.display = 'flex';
    
    try {
        // Appeler l'API
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
        });
        
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Masquer l'indicateur de frappe
        typingIndicator.style.display = 'none';
        
        // Ajouter la réponse
        addMessage('assistant', data.answer, data.evaluation);
        
        // Sauvegarder dans l'historique
        conversationHistory.push({
            question,
            answer: data.answer,
            evaluation: data.evaluation,
            timestamp: new Date().toISOString()
        });
        
    } catch (error) {
        console.error('Erreur:', error);
        typingIndicator.style.display = 'none';
        
        addMessage('assistant', 
            '❌ Désolé, une erreur est survenue lors de la connexion au serveur. Assurez-vous que le serveur FastAPI est bien lancé sur http://127.0.0.1:8000',
            null,
            true
        );
    } finally {
        // Réactiver l'input
        isProcessing = false;
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

// Ajouter un message au chat
function addMessage(role, text, evaluation = null, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    
    if (isError) {
        bubbleDiv.style.background = '#FEE2E2';
        bubbleDiv.style.color = '#991B1B';
    }
    
    // Formater le texte (remplacer les \n par des <br>)
    bubbleDiv.innerHTML = text.replace(/\n/g, '<br>');
    
    const metaDiv = document.createElement('div');
    metaDiv.className = 'message-meta';
    
    const timeSpan = document.createElement('span');
    timeSpan.textContent = new Date().toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    metaDiv.appendChild(timeSpan);
    
    // Ajouter le score d'évaluation si présent
    if (evaluation && evaluation.global_score !== undefined) {
        const scoreSpan = document.createElement('span');
        scoreSpan.className = 'evaluation-score';
        
        const score = evaluation.global_score;
        if (score >= 0.7) {
            scoreSpan.classList.add('good');
        } else if (score >= 0.4) {
            scoreSpan.classList.add('medium');
        } else {
            scoreSpan.classList.add('low');
        }
        
        scoreSpan.innerHTML = `✓ Score: ${(score * 100).toFixed(0)}%`;
        metaDiv.appendChild(scoreSpan);
    }
    
    contentDiv.appendChild(bubbleDiv);
    contentDiv.appendChild(metaDiv);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll vers le bas
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Effacer la conversation
function handleClearChat() {
    if (conversationHistory.length === 0) return;
    
    // Créer le modal de confirmation
    showConfirmModal();
}

// Créer et afficher le modal de confirmation
function showConfirmModal() {
    // Créer l'overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    
    // Créer le container animé
    const container = document.createElement('div');
    container.className = 'modal-container';
    
    // Créer les spans d'animation
    for (let i = 0; i < 50; i++) {
        const span = document.createElement('span');
        span.style.setProperty('--i', i);
        container.appendChild(span);
    }
    
    // Créer la boîte de dialogue
    const modalBox = document.createElement('div');
    modalBox.className = 'modal-box';
    modalBox.innerHTML = `
        <h2>Confirmation</h2>
        <p class="modal-text">Voulez-vous vraiment effacer cette conversation ?</p>
        <div class="modal-buttons">
            <button class="modal-btn modal-btn-cancel" id="modalCancel">Annuler</button>
            <button class="modal-btn modal-btn-confirm" id="modalConfirm">Confirmer</button>
        </div>
    `;
    
    container.appendChild(modalBox);
    overlay.appendChild(container);
    document.body.appendChild(overlay);
    
    // Gestionnaires d'événements
    document.getElementById('modalCancel').addEventListener('click', closeModal);
    document.getElementById('modalConfirm').addEventListener('click', () => {
        clearConversation();
        closeModal();
    });
    
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModal();
    });
}

// Fermer le modal
function closeModal() {
    const overlay = document.querySelector('.modal-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Effacer la conversation
function clearConversation() {
    chatMessages.innerHTML = '';
    conversationHistory = [];
    
    // Réafficher le welcome card
    chatContainer.style.display = 'none';
    chatContainer.classList.remove('active');
    welcomeCard.style.display = 'block';
    
    // Réinitialiser l'input
    userInput.value = '';
    userInput.style.height = 'auto';
}

// Fonction utilitaire pour formater les timestamps
function formatTimestamp(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Sauvegarder l'historique dans localStorage (optionnel)
function saveHistory() {
    try {
        localStorage.setItem('chatHistory', JSON.stringify(conversationHistory));
    } catch (error) {
        console.warn('Impossible de sauvegarder l\'historique:', error);
    }
}

// Charger l'historique depuis localStorage (optionnel)
function loadHistory() {
    try {
        const saved = localStorage.getItem('chatHistory');
        if (saved) {
            conversationHistory = JSON.parse(saved);
            
            if (conversationHistory.length > 0) {
                welcomeCard.style.display = 'none';
                chatContainer.style.display = 'flex';
                
                conversationHistory.forEach(item => {
                    addMessage('user', item.question);
                    addMessage('assistant', item.answer, item.evaluation);
                });
            }
        }
    } catch (error) {
        console.warn('Impossible de charger l\'historique:', error);
    }
}

// Auto-save toutes les 30 secondes
setInterval(() => {
    if (conversationHistory.length > 0) {
        saveHistory();
    }
}, 30000);

// Sauvegarder avant de quitter
window.addEventListener('beforeunload', () => {
    saveHistory();
});

// Charger l'historique au démarrage (optionnel - décommenter si souhaité)
// loadHistory();
