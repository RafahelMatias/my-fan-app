# Know Your Fan

**Know Your Fan**

> Objetivo: Desenvolver uma solução full-stack que colete o máximo de informações sobre você mesmo como fã de e-sports, incluindo:
> 1. Dados básicos (nome, e-mail, CPF, endereço).  
> 2. Interesses, atividades, eventos e compras do último ano.  
> 3. Upload de documento (RG/CPF) com validação de identidade via OCR.  
> 4. Vinculação de redes sociais (Twitter) e leitura de interações (seguidores, tweets).  

---

## 📦 Tech Stack

- **Frontend**  
  - React & Vite  
  - react-dropzone (upload)  
  - Fetch API para comunicação JSON/FormData  

- **Backend**  
  - Python 3.9+  
  - FastAPI + Uvicorn  
  - SQLModel (SQLite)  
  - python-dotenv (variáveis de ambiente)  
  - OCR: Tesseract via `pytesseract` + Pillow  
  - Social: Twitter API v2 via Tweepy  

- **Storage**  
  - SQLite (`data.db`)  
  - Pasta `uploads/` para imagens de documentos  

---

## 🚀 Pré-requisitos

1. **Node.js** (v16+)  
2. **Python 3.9+**  
3. **Tesseract OCR**  
   - Windows: baixe o instalador no repositório UB-Mannheim e garanta que `tesseract --version` funcione.  
   - macOS/Linux: `brew install tesseract` ou `apt install tesseract-ocr`.  
4. **Conta de Desenvolvedor Twitter** para gerar um **Bearer Token**.


---


## ⚙️ Uso

1. Preencha o formulário com seus dados  
2. Faça upload da foto do RG/CPF  
3. (Opcional) Informe seu handle do Twitter  
4. Clique em **Enviar**

O backend:
- salva os dados no SQLite;
- executa OCR no documento para validar o CPF;
- consulta o Twitter (perfil + últimos tweets).

O frontend exibe uma confirmação e os dados extraídos.


---


# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
