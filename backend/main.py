from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit")
async def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    interests: str = Form(...),
    file: UploadFile = File(None),
):
    try:
        logger.info(f"Requisição recebida - POST /submit")
        logger.info(f"Dados: name={name}, email={email}, cpf={cpf}, interests={interests}")
        
        if file:
            logger.info(f"Arquivo recebido: {file.filename}")
        else:
            logger.info("Nenhum arquivo recebido.")
        
        return {
            "status": "success",
            "message": "Dados recebidos com sucesso!",
            "received_data": {
                "name": name,
                "email": email,
                "cpf": cpf,
                "interests": interests,
                "file": file.filename if file else None
            }
        }
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"status": "Backend está rodando!"}
