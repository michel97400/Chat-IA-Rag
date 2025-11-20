from typing import Union
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# Configuration CORS plus permissive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permet tous les headers
    expose_headers=["*"]  # Expose tous les headers
)

# Middleware de debug pour voir les requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"🔍 Requête reçue: {request.method} {request.url}")
    print(f"📍 Origin: {request.headers.get('origin', 'N/A')}")
    print(f"📍 Headers: {dict(request.headers)}")
    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return JSONResponse(
        content={"message": "API RAG avec FastAPI", "status": "running"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.options("/query")
async def options_query():
    """Handle preflight CORS requests"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.post("/query")
def query_rag_endpoint(request: schema.QueryRequest):
    return controller.query_controller(request)

@app.post("/evaluate")
def evaluate_rag_endpoint(request: schema.EvaluationRequest):
    return controller.evaluate_controller(request)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}