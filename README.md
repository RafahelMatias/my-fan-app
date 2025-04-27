# Know Your Fan

Aplicação **Know Your Fan**: um protótipo full-stack (React + Vite no front-end e FastAPI no back-end) que permite:

- 📋 Coleta de dados pessoais (nome, e-mail, CPF e interesses em e-sports) com validação de formulário e máscara de CPF  
- 📂 Upload e processamento de documentos (RG/CPF) via OCR (AWS Rekognition ou Tesseract) para confirmação automática dos dados  
- 🔗 Autenticação social (Firebase Auth) e integração com APIs de redes sociais (Twitter, Facebook, Steam) para extrair e classificar postagens e interações relevantes  
- 🚀 Deploy rápido em Vercel (frontend) e Render.com (backend), usando SQLite para MVP e fácil migração para PostgreSQL e Redis  
 

> Protótipo de POC para conhecer cada fã de e-sports e oferecer experiências personalizadas.

---



# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
