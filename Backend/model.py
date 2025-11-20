import json
import os
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.groq import Groq
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration des API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class RAGModel:
    def __init__(self):
        self.embed_model = None
        self.query_engine = None
        self.evaluator = None
        self.initialize()

    def load_scraped_data(self, json_file=None):
        """
        Charge les données scrapées depuis le fichier JSON.
        """
        if json_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_file = os.path.join(script_dir, 'data/scraped_data.json')
        if not os.path.exists(json_file):
            print(f"Fichier {json_file} non trouvé.")
            return []
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def create_documents(self, data):
        """
        Crée des documents LlamaIndex à partir des données scrapées.
        """
        documents = []
        for item in data:
            doc = Document(
                text=item['content'],
                metadata={
                    'url': item['url'],
                    'timestamp': item['timestamp']
                }
            )
            documents.append(doc)
        return documents

    def initialize(self):
        print("Initialisation du modèle RAG...")

        # Vérifier la clé API Groq
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY non trouvée dans les variables d'environnement")

        # Configurer les modèles LlamaIndex
        self.embed_model = OllamaEmbedding(model_name="bge-m3")
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 512
        Settings.chunk_overlap = 20
        Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
        print("✅ Modèles configurés !")

        # Créer l'évaluateur personnalisé
        self.evaluator = CustomEvaluator(self.embed_model)
        print("✅ Évaluateur créé !")

        # Chargement des documents
        print("📄 Chargement des documents...")
        data = self.load_scraped_data()
        if not data:
            raise ValueError("Aucun document trouvé. Assurez-vous que scraped_data.json existe.")

        documents = self.create_documents(data)
        print(f"✅ {len(documents)} documents chargés !")

        # Création ou chargement de l'index persistant
        print("🔍 Création/Chargement de l'index...")
        index_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/vector_index')
        if os.path.exists(index_dir):
            from llama_index.core import StorageContext, load_index_from_storage
            storage_context = StorageContext.from_defaults(persist_dir=index_dir)
            index = load_index_from_storage(storage_context)
            print("✅ Index chargé depuis le disque !")
        else:
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist(persist_dir=index_dir)
            print("✅ Index créé et sauvegardé !")

        # Créer le query engine
        self.query_engine = index.as_query_engine(similarity_top_k=3)
        print("✅ Query engine prêt !")

class CustomEvaluator:
    """
    Classe d'évaluation personnalisée pour évaluer le RAG.
    """
    def __init__(self, embed_model):
        self.embed_model = embed_model
    
    def get_embedding(self, text):
        """Obtient l'embedding d'un texte."""
        try:
            embedding = self.embed_model.get_text_embedding(text)
            return np.array(embedding)
        except Exception as e:
            print(f"Erreur lors de l'embedding : {e}")
            return None
    
    def answer_relevancy(self, question, answer):
        """
        Mesure la pertinence de la réponse par rapport à la question.
        Score entre 0 et 1 (plus proche de 1 = plus pertinent).
        """
        try:
            q_embedding = self.get_embedding(question)
            a_embedding = self.get_embedding(answer)
            
            if q_embedding is None or a_embedding is None:
                return 0.0
            
            # Calcul de similarité cosinus
            similarity = cosine_similarity(
                [q_embedding],
                [a_embedding]
            )[0][0]
            
            # Normaliser entre 0 et 1
            score = (similarity + 1) / 2
            return float(score)
        except Exception as e:
            print(f"Erreur dans answer_relevancy : {e}")
            return 0.0
    
    def context_precision(self, question, contexts):
        """
        Mesure la précision du contexte.
        Évalue si les contextes sont pertinents par rapport à la question.
        Score entre 0 et 1.
        """
        try:
            if not contexts:
                return 0.0
            
            q_embedding = self.get_embedding(question)
            if q_embedding is None:
                return 0.0
            
            scores = []
            for context in contexts:
                c_embedding = self.get_embedding(context)
                if c_embedding is not None:
                    similarity = cosine_similarity(
                        [q_embedding],
                        [c_embedding]
                    )[0][0]
                    scores.append((similarity + 1) / 2)
            
            # Retourner la moyenne des scores
            if scores:
                return float(np.mean(scores))
            return 0.0
        except Exception as e:
            print(f"Erreur dans context_precision : {e}")
            return 0.0
    
    def context_recall(self, answer, contexts):
        """
        Mesure le rappel du contexte.
        Évalue si la réponse couvre les informations des contextes.
        Score entre 0 et 1.
        """
        try:
            if not contexts:
                return 0.0
            
            a_embedding = self.get_embedding(answer)
            if a_embedding is None:
                return 0.0
            
            scores = []
            for context in contexts:
                c_embedding = self.get_embedding(context)
                if c_embedding is not None:
                    similarity = cosine_similarity(
                        [a_embedding],
                        [c_embedding]
                    )[0][0]
                    scores.append((similarity + 1) / 2)
            
            # Retourner la moyenne des scores
            if scores:
                return float(np.mean(scores))
            return 0.0
        except Exception as e:
            print(f"Erreur dans context_recall : {e}")
            return 0.0
    
    def evaluate(self, question, answer, contexts):
        """
        Effectue une évaluation complète.
        Retourne un dictionnaire avec tous les scores.
        """
        return {
            "answer_relevancy": self.answer_relevancy(question, answer),
            "context_precision": self.context_precision(question, contexts),
            "context_recall": self.context_recall(answer, contexts)
        }