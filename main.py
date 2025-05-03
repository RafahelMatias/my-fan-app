from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json, os, logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# → Adicione estes imports para o SQLite/SQLModel:
from typing import List, Optional
from sqlmodel import SQLModel, Field, Session, create_engine

app = FastAPI()

# Atualizar CORS para desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure o engine
engine = create_engine("sqlite:///data.db")

# Cria a pasta uploads/ se não existir
os.makedirs("uploads", exist_ok=True)

# → Atualize o modelo Fan
class Fan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    cpf: str
    interests: str  # Armazena a lista como JSON serializado
    address: str         # New field for Address
    activities: str      # New field for Activities

# Criação das tabelas na inicialização do aplicativo
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Adicionar endpoint de teste
@app.get("/")
async def root():
    logger.info("Verificação de status solicitada")
    return {"status": "online", "message": "Server is running"}

@app.post("/submit")
async def submit(
    name: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    interests: str = Form(...),
    address: str = Form(...),      # New Form field for Address
    activities: str = Form(...),   # New Form field for Activities
    file: UploadFile = File(...),
):
    logger.info(f"Recebendo dados: name={name}, email={email}")
    # Converte interests de volta para lista Python
    try:
        if interests.startswith("[") and interests.endswith("]"):
            # Trata como JSON serializado
            interests_list: List[str] = json.loads(interests)
        else:
            # Trata como string simples e converte para lista
            interests_list: List[str] = [interests]
    except Exception:
        return {"error": "Interesses inválidos, envie um JSON de lista ou uma string"}

    # Salva o upload em disco
    dest_path = f"uploads/{file.filename}"
    with open(dest_path, "wb") as f:
        f.write(await file.read())

    # → Aqui você persiste no SQLite:
    with Session(engine) as session:
        fan = Fan(
            name=name,
            email=email,
            cpf=cpf,
            interests=json.dumps(interests_list),  # Serializa para JSON
            address=address,         # Persist Address
            activities=activities,   # Persist Activities
        )
        session.add(fan)
        session.commit()

    return {
        "message": "Recebido e salvo com sucesso!",
        "data": {
            "name": name,
            "email": email,
            "cpf": cpf,
            "address": address,         # Return Address
            "activities": activities,   # Return Activities
            "interests": interests_list,
            "file_saved_as": dest_path,
        },
    }
