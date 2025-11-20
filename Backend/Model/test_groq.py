import json
import os
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.groq import Groq
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API key (utilise la variable d'environnement si disponible)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")




def load_scraped_data(json_file='data/scraped_data.json'):
    """
    Charge les données scrapées depuis le fichier JSON.
    """
    if not os.path.exists(json_file):
        print(f"Fichier {json_file} non trouvé.")
        return []
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def create_documents(data):
    """
    Crée des objets Document à partir des données scrapées.
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

def main():
    print("🤖 llama-3.3-70b-versatile avec LlamaIndex RAG - Version Simplifiée")
    print("="*60)

    # Vérifier la clé API
    if not GROQ_API_KEY:
        print("❌ Erreur : GROQ_API_KEY non trouvée dans les variables d'environnement")
        return

    # Configurer les modèles
    embed_model = OllamaEmbedding(model_name="bge-m3")
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    Settings.chunk_overlap = 20

    print("✅ Modèles configurés !")

    # Chargement des documents
    print("📄 Chargement des documents...")
    data = load_scraped_data()
    if not data:
        print("❌ Aucun document trouvé. Assurez-vous que scraped_data.json existe.")
        return

    documents = create_documents(data)
    print(f"✅ {len(documents)} documents chargés !")

    # Création de l'index
    print("🔍 Création de l'index...")
    index = VectorStoreIndex.from_documents(documents)
    print("✅ Index créé !")

    # Récupérateur de documents
    retriever = index.as_retriever(similarity_top_k=3)

    # Initialiser le LLM Groq
    llm = Groq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

    # Chat interactif avec RAG
    print("\n" + "="*60)
    print("💬 CHAT RAG - Posez vos questions sur le diabète !")
    print("="*60)
    print("• Tapez votre question et appuyez sur Entrée")
    print("• Tapez 'quit' pour quitter")
    print("-"*60)

    while True:
        try:
            user_question = input("\n🧑 Question: ").strip()

            if user_question.lower() in ['quit', 'exit']:
                print("👋 Au revoir !")
                break

            if not user_question:
                continue

            print("\n🔍 Recherche dans les documents...")

            # Récupération des documents pertinents
            retrieved_docs = retriever.retrieve(user_question)

            # Construction du contexte
            context_text = ""
            for doc in retrieved_docs:
                context_text += f"{doc.text[:500]}...\n\n"  # Limiter la longueur

            # Construction du prompt
            prompt = f"""Contexte: Voici des informations pertinentes trouvées dans la documentation :

{context_text}

Question: {user_question}

Réponse: En me basant sur les informations du contexte ci-dessus, """

            print("🤖 Génération de la réponse...")

            response = llm.complete(prompt)

            # Nettoyer la réponse
            if "Réponse:" in response:
                response = response.split("Réponse:")[-1].strip()

            print(f"\n🤖 Réponse: {response}")

        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"\n❌ Erreur : {e}")


if __name__ == "__main__":
    main()