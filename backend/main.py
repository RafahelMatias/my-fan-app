from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, logging, json, tweepy
from tweepy.errors import TooManyRequests
from typing import Optional

# Configuração inicial
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twitter client
client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

@app.get("/")
async def root():
    return {"status": "Backend está rodando!"}

@app.post("/submit")
async def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    address: str = Form(...),
    activities: str = Form(...),
    interests: str = Form(...),
    twitter: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        logger.info(f"Recebendo dados: name={name}, email={email}")
        
        # Converte interests para lista
        interests_list = json.loads(interests) if interests.startswith("[") else [interests]
        
        return {
            "status": "success",
            "message": "Dados recebidos com sucesso!",
            "data": {
                "name": name,
                "email": email,
                "cpf": cpf,
                "address": address,
                "activities": activities,
                "interests": interests_list,
                "twitter": twitter,
                "file": file.filename if file else None
            }
        }
    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/twitter/{handle}")
async def get_twitter(handle: str):
    try:
        # Remove @ se presente
        username = handle.lstrip('@')
        
        # Busca usuário
        user = client.get_user(
            username=username,
            user_fields=["public_metrics"]
        )
        if not user.data:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
        # Busca tweets
        tweets = client.get_users_tweets(
            user.data.id,
            max_results=5,
            tweet_fields=["text"]
        )
        
        return {
            "profile": {
                "name": username,
                "public_metrics": user.data.public_metrics
            },
            "recent_tweets": [t.text for t in (tweets.data or [])]
        }
        
    except TooManyRequests:
        raise HTTPException(
            status_code=429,
            detail="Limite de requisições excedido"
        )
    except Exception as e:
        logger.error(f"Erro ao buscar dados do Twitter: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/twitter/furia")  # Removido /tweets do path
async def get_furia_tweets():
    try:
        tweets = client.search_recent_tweets(
            query="#FURIA",
            max_results=10,
            tweet_fields=["text"]
        )
        return {
            "recent_tweets": [t.text for t in (tweets.data or [])]  
        }
    except TooManyRequests:
        raise HTTPException(
            status_code=429,
            detail="Limite de requisições excedido"
        )
    except Exception as e:
        logger.error(f"Erro ao buscar tweets da FURIA: {e}")
        raise HTTPException(status_code=500, detail=str(e))
