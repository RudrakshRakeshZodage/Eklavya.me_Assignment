# ⚡ Eklavya.me: AI Learning Architect

A premium, dual-agent educational content generator built with **Neo-Brutalism** aesthetics and **Google Gemini** intelligence.

![Neo-Brutalism Dashboard](https://raw.githubusercontent.com/RudrakshRakeshZodage/Eklavya.me_Assignment/main/frontend/public/preview.png) *(Placeholder - Upload your dashboard screenshot here)*

## 🚀 Live Demo
- **Frontend (Vercel):** [eklavya-assignment-1.vercel.app](https://eklavya-assignment-1.vercel.app) *(Link may vary based on your final choice)*
- **Backend (AWS EC2):** [http://13.217.105.1](http://13.217.105.1)

---

## 🧠 The Architecture
Eklavya uses a **Multi-Agent Workflow** to ensure high-quality educational content:

1.  **The Generator Agent**: Crafted with Gemini 1.5 Flash, it creates age-appropriate explanations and MCQs based on specific grade levels (1-12).
2.  **The Reviewer Agent**: A critical second eye that evaluates the generated content for factual accuracy and grade-level readability. It provides feedback and triggers refinements if the content isn't perfect.

## 🛠️ Tech Stack
- **Frontend**: Next.js 14, TypeScript, CSS Modules (Neo-Brutalism Design System).
- **Backend**: FastAPI (Python 3.10), Gunicorn, Docker.
- **AI Engine**: Google Gemini 1.5 Flash (Latency < 5s).
- **Infrastructure**: AWS (EC2 + ECR) & Vercel.

---

## 📂 Project Structure
```text
.
├── backend/            # FastAPI Server
│   ├── agents/         # AI Agent Logic (Generator/Reviewer)
│   ├── Dockerfile      # Container Configuration
│   └── main.py         # API Endpoints
├── frontend/           # Next.js Application
│   ├── app/            # Pages & Layouts
│   └── components/     # UI Components
└── .gitignore          # Security rules
```

## ⚙️ Setup & Installation

### Backend (Dockerized)
1. Navigate to `backend/`.
2. Add your `GEMINI_API_KEY` to `.env`.
3. Build and Run:
   ```bash
   docker build -t eklavya-backend .
   docker run -p 8000:8000 eklavya-backend
   ```

### Frontend
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Start development: `npm run dev`.

---

## ☁️ Deployment Guide

### AWS EC2 (Backend)
- Image stored in **AWS ECR**.
- Running on **t3.micro** instance with **Port 80** exposed.
- IAM Role attached for ECR Read permissions.

### Vercel (Frontend)
- Continuous Deployment from GitHub.
- Environment Variable: `NEXT_PUBLIC_API_URL` pointing to the AWS IP.

---

## 🎨 Design Philosophy
The UI follows a **Neo-Brutalism** approach:
- **Bold Borders**: 3px - 4px solid black borders.
- **Hard Shadows**: Offset shadows for depth without gradients.
- **Vibrant Accents**: High-contrast colors (Amber, Indigo, Emerald).
- **Dot-Grid Background**: Professional blueprint texture.

---

Created with ⚡ by **Rudraksh Rakesh Zodage**
