from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager
import controller
import schema
import crud

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    crud.init_rag_model()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "API RAG avec FastAPI", "status": "running"}

@app.post("/query")
def query_rag_endpoint(request: schema.QueryRequest):
    return controller.query_controller(request)

@app.post("/evaluate")
def evaluate_rag_endpoint(request: schema.EvaluationRequest):
    return controller.evaluate_controller(request)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}