from fastapi import HTTPException
import schema
import crud

def query_controller(request: schema.QueryRequest) -> schema.QueryResponse:
    try:
        answer = crud.query_rag(request.question)
        return schema.QueryResponse(question=request.question, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête : {str(e)}")

def evaluate_controller(request: schema.EvaluationRequest) -> schema.EvaluationResponse:
    try:
        scores, global_score = crud.evaluate_rag(request.question, request.answer, request.contexts)
        return schema.EvaluationResponse(scores=scores, global_score=global_score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'évaluation : {str(e)}")