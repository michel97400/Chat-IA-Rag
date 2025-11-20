import json
import os
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Charger les variables d'environnement
load_dotenv()

# Configuration des API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def load_scraped_data(json_file=None):
    """
    Charge les données scrapées depuis le fichier JSON.
    """
    if json_file is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(script_dir, '../data/scraped_data.json')
    if not os.path.exists(json_file):
        print(f"Fichier {json_file} non trouvé.")
        return []
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def create_documents(data):
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

def main():
    print("🤖 llama-3.3-70b-versatile avec LlamaIndex RAG - Évaluation Robuste")
    print("="*60)

    # Vérifier la clé API Groq
    if not GROQ_API_KEY:
        print("❌ Erreur : GROQ_API_KEY non trouvée dans les variables d'environnement")
        return

    # Configurer les modèles LlamaIndex
    embed_model = OllamaEmbedding(model_name="bge-m3")
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    Settings.chunk_overlap = 20
    Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
    print("✅ Modèles configurés !")

    # Créer l'évaluateur personnalisé
    evaluator = CustomEvaluator(embed_model)
    print("✅ Évaluateur créé !")

    # Chargement des documents
    print("📄 Chargement des documents...")
    data = load_scraped_data()
    if not data:
        print("❌ Aucun document trouvé. Assurez-vous que scraped_data.json existe.")
        return

    documents = create_documents(data)
    print(f"✅ {len(documents)} documents chargés !")

    # Création ou chargement de l'index persistant
    print("🔍 Création/Chargement de l'index...")
    index_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/vector_index')
    if os.path.exists(index_dir):
        from llama_index.core import StorageContext, load_index_from_storage
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(storage_context)
        print("✅ Index chargé depuis le disque !")
    else:
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=index_dir)
        print("✅ Index créé et sauvegardé !")

    # Créer le query engine et retriever
    query_engine = index.as_query_engine(similarity_top_k=3)
    retriever = index.as_retriever(similarity_top_k=3)

    # Chat interactif avec RAG + évaluation personnalisée
    print("\n" + "="*60)
    print("💬 CHAT RAG - Posez vos questions sur le diabète !")
    print("="*60)
    print("• Tapez votre question et appuyez sur Entrée")
    print("• Tapez 'quit' pour quitter")
    print("-"*60)

    evaluation_results = []

    while True:
        try:
            user_question = input("\n🧑 Question: ").strip()

            if user_question.lower() in ['quit', 'exit']:
                print("👋 Au revoir !")
                break

            if not user_question:
                continue

            print("\n🔍 Recherche dans les documents...")
            
            # Récupérer la réponse
            print("🤖 Génération de la réponse...")
            response = query_engine.query(user_question)
            response_text = str(response)
            
            print(f"\n🤖 Réponse: {response_text}")

            # Récupérer les contextes pour l'évaluation
            retrieved_docs = retriever.retrieve(user_question)
            contexts = [doc.text for doc in retrieved_docs]

            # Évaluation personnalisée - RAPIDE ET FIABLE
            print("\n📊 Évaluation en cours...")
            scores = evaluator.evaluate(user_question, response_text, contexts)
            
            # Afficher les résultats
            print(f"\n✅ Résultats d'évaluation:")
            print(f"   • Answer Relevancy (Pertinence) : {scores.get('answer_relevancy', 0):.2f}")
            print(f"   • Context Precision (Précision contexte) : {scores.get('context_precision', 0):.2f}")
            print(f"   • Context Recall (Rappel contexte) : {scores.get('context_recall', 0):.2f}")
            
            # Score global
            global_score = np.mean([
                scores.get('answer_relevancy', 0),
                scores.get('context_precision', 0),
                scores.get('context_recall', 0)
            ])
            print(f"📈 Score global : {global_score:.2f}")
            
            # Sauvegarder les résultats
            evaluation_results.append({
                "question": user_question,
                "scores": scores,
                "global_score": global_score
            })

        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            import traceback
            traceback.print_exc()

    # Afficher un résumé des évaluations
    if evaluation_results:
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DES ÉVALUATIONS")
        print("="*60)
        avg_relevancy = np.mean([r['scores']['answer_relevancy'] for r in evaluation_results])
        avg_precision = np.mean([r['scores']['context_precision'] for r in evaluation_results])
        avg_recall = np.mean([r['scores']['context_recall'] for r in evaluation_results])
        
        print(f"Moyenne Answer Relevancy : {avg_relevancy:.2f}")
        print(f"Moyenne Context Precision : {avg_precision:.2f}")
        print(f"Moyenne Context Recall : {avg_recall:.2f}")
        print(f"Score global moyen : {np.mean([r['global_score'] for r in evaluation_results]):.2f}")


if __name__ == "__main__":
    main()