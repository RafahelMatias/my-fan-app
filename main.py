from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

app = FastAPI()

# Configura CORS para permitir chamadas do seu front-end em http://localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Garante que a pasta uploads/ exista
os.makedirs("uploads", exist_ok=True)

@app.post("/submit")
async def submit(
    name: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    interests: str = Form(...),           # virá como JSON string
    file: UploadFile = File(...),
):
    # Converte interests de volta para lista Python
    try:
        interests_list: List[str] = json.loads(interests)
    except json.JSONDecodeError:
        return {"error": "Interesses inválidos, envie um JSON de lista"}

    # Salva o upload em disco
    dest_path = f"uploads/{file.filename}"
    with open(dest_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Recebido com sucesso!",
        "data": {
            "name": name,
            "email": email,
            "cpf": cpf,
            "interests": interests_list,
            "file_saved_as": dest_path
        }
    }
