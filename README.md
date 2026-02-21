# Know Your Fan (e-Sports CRM)

![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![Twitter API](https://img.shields.io/badge/Integration-Twitter%20API%20v2-1DA1F2?style=for-the-badge&logo=twitter)
![OCR](https://img.shields.io/badge/Identity-Tesseract%20OCR-green?style=for-the-badge)

## 📋 Project Overview

A Full-Stack Customer Relationship Management (CRM) prototype designed for e-Sports organizations. The goal is to collect fan data, validate identities, and enrich profiles using social  media integration.

**Technical Context:**
This project was developed as a **Coding Challenge** to demonstrate proficiency in connecting a modern Frontend (React) with a high-performance Python Backend (FastAPI). The challenge required building a system to validate user identity via image processing and fetch real-time social data.

## 🤖 Development Methodology: AI-Assisted Prototyping

This project was built leveraging modern **AI-Driven Development** workflows. Since the coding challenge explicitly encouraged the use of AI tools, my focus shifted from manual syntax typing to **Architecture, Product Engineering, and Prompt Orchestration**.

Instead of simply generating code, I utilized a continuous, iterative loop to build the full-stack application:
1. **Architectural Prompts:** I defined the separation of concerns between the React frontend and the Python (FastAPI) backend.
2. **The Iterative Loop (Prompt, Analyze, Refine):** I instructed the AI to implement complex logic, such as the computer vision pipeline using Tesseract OCR and the Twitter API integration. 
3. **Manual Debugging & Curation:** Once the AI provided the base structure, I analyzed the code for edge cases and errors. For example, when the raw OCR extraction failed to match user inputs, I manually rewrote the Python logic to clean and sanitize the data (removing formatting like dots and hyphens) before validation. I then used these manual corrections as context for my next prompts to the AI, maintaining a cycle of continuous improvement.

This methodology allowed me to act as a Technical Lead over the AI, ensuring the final identity validation pipeline was secure, accurate, and ready for production.


## 🚀 Key Features

* **Automated Identity Validation (OCR):** Uses **Tesseract OCR** (`pytesseract`) to scan uploaded ID cards and programmatically verify if the printed CPF matches the user input.
* **Social Intelligence:** Integrates with **Twitter API v2** (via `tweepy`) to fetch the fan's profile metrics and analyze their engagement (tweets) in real-time.
* **Hashtag Tracking:** Automatically tracks specific e-sports tags (e.g., `#FURIA`) to display trending community discussions.
* **Full-Stack Architecture:**
    * **Frontend:** React (Vite) with `react-dropzone` for file handling.
    * **Backend:** FastAPI (Python) serving REST endpoints.
    * **Data Handling:** JSON/FormData communication and Identity Document processing.

## 🛠️ Tech Stack

### Frontend
* **Framework:** React 18 (Vite)
* **Styling:** CSS Modules
* **Networking:** Fetch API

### Backend
* **Framework:** FastAPI (Python 3.9+)
* **Server:** Uvicorn
* **Integrations:** Tweepy (Twitter), Pytesseract (OCR), Python-Multipart (File Uploads)

## 💻 How to Run

### Prerequisites
* Node.js (v16+)
* Python 3.9+
* Tesseract OCR installed on your system.
* Twitter Developer Account (Bearer Token).

### 1. Automatic Start (Windows)
Simply run the `start.bat` file in the root directory.

### 2. Manual Start
**Backend:**
```bash
cd backend
pip install -r ../requirements.txt
# Create .env file with TWITTER_BEARER_TOKEN=your_token
uvicorn main:app --reload 