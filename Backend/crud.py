import model
import numpy as np

# Instance globale du modèle RAG
rag_model = None

def init_rag_model():
    global rag_model
    if rag_model is None:
        rag_model = model.RAGModel()
    return rag_model

def query_rag(question: str):
    if rag_model is None:
        raise ValueError("Modèle RAG non initialisé")
    response = rag_model.query_engine.query(question)
    return str(response)

def evaluate_rag(question: str, answer: str, contexts: list):
    if rag_model is None or rag_model.evaluator is None:
        raise ValueError("Évaluateur non initialisé")
    scores = rag_model.evaluator.evaluate(question, answer, contexts)
    global_score = np.mean([
        scores.get('answer_relevancy', 0),
        scores.get('context_precision', 0),
        scores.get('context_recall', 0)
    ])
    return scores, float(global_score)