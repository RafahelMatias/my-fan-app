from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import logging
import re
from PIL import Image  # New import for image processing with Pillow
import pytesseract

# Se o Windows não encontrar o executável do Tesseract, aponte aqui:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configurar logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# → Imports para o SQLite/SQLModel
from typing import List, Optional
from sqlmodel import SQLModel, Field, Session, create_engine

app = FastAPI()

# CORS para desenvolvimento local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure o engine e a pasta de uploads
engine = create_engine("sqlite:///data.db")
os.makedirs("uploads", exist_ok=True)

# Modelo SQLModel
class Fan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    cpf: str
    interests: str      # JSON serializado
    address: str        # Endereço
    activities: str     # Atividades/Eventos/Compras

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

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
    address: str = Form(...),
    activities: str = Form(...),
    file: UploadFile = File(...),
):
    logger.info(f"Recebendo dados: name={name}, email={email}")

    # Converte interests de volta para lista Python
    try:
        if interests.startswith("[") and interests.endswith("]"):
            interests_list: List[str] = json.loads(interests)
        else:
            interests_list: List[str] = [interests]
    except Exception:
        raise HTTPException(status_code=400, detail="Interesses inválidos, envie JSON ou string")

    # Salva o upload em disco
    dest_path = f"uploads/{file.filename}"
    with open(dest_path, "wb") as f:
        f.write(await file.read())

    # --- OCR e validação de CPF ---
    # lê a imagem e faz OCR usando Pillow
    try:
        image = Image.open(dest_path)
    except Exception:
        raise HTTPException(status_code=400, detail="Falha ao ler a imagem enviada")
    ocr_text = pytesseract.image_to_string(image)

    # tenta extrair um padrão de CPF (000.000.000-00 ou 11 dígitos seguidos)
    m = re.search(r'(\d{3}\.?\d{3}\.?\d{3}-?\d{2})', ocr_text)
    if not m:
        raise HTTPException(status_code=400, detail="CPF não encontrado no documento via OCR")
    extracted_cpf = re.sub(r'\D', '', m.group(1))
    cleaned_form_cpf = re.sub(r'\D', '', cpf)

    if extracted_cpf != cleaned_form_cpf:
        raise HTTPException(
            status_code=400,
            detail="O CPF extraído do documento não corresponde ao CPF do formulário"
        )
    # ------------------------------------

    # Persiste no SQLite
    with Session(engine) as session:
        fan = Fan(
            name=name,
            email=email,
            cpf=cleaned_form_cpf,
            interests=json.dumps(interests_list),
            address=address,
            activities=activities,
        )
        session.add(fan)
        session.commit()

    return {
        "message": "Recebido e salvo com sucesso!",
        "data": {
            "name": name,
            "email": email,
            "cpf": cleaned_form_cpf,
            "address": address,
            "activities": activities,
            "interests": interests_list,
            "file_saved_as": dest_path,
        },
    }
