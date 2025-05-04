from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import json
import os
import logging
import re
import tweepy
from PIL import Image  # New import for image processing with Pillow
import pytesseract
from tweepy.errors import TooManyRequests
from fastapi import HTTPException
from time import time

# Se o Windows não encontrar o executável do Tesseract, aponte aqui:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configurar logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# → Imports para o SQLite/SQLModel
from typing import List, Optional
from sqlmodel import SQLModel, Field, Session, create_engine

# Load environment variables and initialize Twitter client
load_dotenv()
client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

app = FastAPI()

# CORS para desenvolvimento local
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
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
    interests: str      
    address: str       
    activities: str     
    twitter: Optional[str] = Field(default=None)

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
    twitter: Optional[str] = Form(None),
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
            twitter=twitter,
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
            "twitter": twitter,
            "interests": interests_list,
            "file_saved_as": dest_path,
        },
    }

# Cache setup
twitter_cache = {
    'furia_tweets': {'data': None, 'timestamp': 0},
    'user_tweets': {},
}
CACHE_DURATION = 60  # Cache duration in seconds

@app.get("/twitter/furia")
async def get_furia_highlight():
    # Check cache first
    cache = twitter_cache['furia_tweets']
    if cache['data'] and time() - cache['timestamp'] < CACHE_DURATION:
        return cache['data']

    try:
        resp = client.search_recent_tweets(
            query="#FURIA",
            max_results=10,
            tweet_fields=["text"]
        )
        data = {"recent_tweets": [t.text for t in (resp.data or [])]}
        
        # Update cache
        twitter_cache['furia_tweets'] = {
            'data': data,
            'timestamp': time()
        }
        return data

    except TooManyRequests:
        # Return cached data if available, even if expired
        if cache['data']:
            logger.warning("Rate limited, returning cached data")
            return cache['data']
        logger.error("Rate limited, no cached data available")
        return {"recent_tweets": ["Temporariamente indisponível devido ao limite de requisições"]}

    except Exception as e:
        logger.error(f"Erro ao buscar tweets da FURIA: {str(e)}")
        # Try to return cached data on error
        if cache['data']:
            return cache['data']
        return {"recent_tweets": ["Não foi possível carregar tweets no momento"]}

@app.get("/twitter/{handle}")
async def get_twitter(handle: str):
    if handle.lower() == "furia":
        return await get_furia_highlight()

    # Check cache
    cache = twitter_cache['user_tweets'].get(handle, {'data': None, 'timestamp': 0})
    if cache['data'] and time() - cache['timestamp'] < CACHE_DURATION:
        return cache['data']

    try:
        user = client.get_user(
            username=handle,
            user_fields=["name", "public_metrics"]
        )
        if not user.data:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
        tweets = client.get_users_tweets(user.data.id, max_results=5)
        
        response_data = {
            "profile": {
                "name": user.data.name,
                "public_metrics": user.data.public_metrics
            },
            "recent_tweets": [t.text for t in (tweets.data or [])]
        }

        # Cache the successful response
        twitter_cache['user_tweets'][handle] = {
            'data': response_data,
            'timestamp': time()
        }
        return response_data

    except TooManyRequests:
        if cache['data']:
            logger.warning(f"Rate limited for {handle}, returning cached data")
            return cache['data']
        return {
            "profile": {"name": handle.replace("@", ""), "public_metrics": {"followers_count": 0}},
            "recent_tweets": []
        }

    except Exception as e:
        logger.error(f"Erro ao buscar dados do Twitter: {str(e)}")
        # Try to return cached data on error
        if cache['data']:
            return cache['data']
        return {
            "profile": {"name": handle.replace("@", ""), "public_metrics": {"followers_count": 0}},
            "recent_tweets": []
        }
