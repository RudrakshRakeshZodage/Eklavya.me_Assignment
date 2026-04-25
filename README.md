# ✦ Eklavya.me | AI Learning Architect

**Live Site:** [https://eklavya-assignment-sepia.vercel.app/](https://eklavya-assignment-sepia.vercel.app/)

Eklavya.me is a state-of-the-art AI-powered platform designed to architect personalized educational content. It uses a collaborative multi-agent system to generate, review, and verify learning materials for students from Grade 1 to 12.

---


## 📸 Screenshots

### 1. Control Center
![Dashboard View](./1.png)
*The main control center where architects choose grades and topics to master.*

### 2. Agent Workflow
![Agent Pulse](./2.png)
*Real-time agent pulse tracking the collaboration between the Curriculum Architect and Quality Reviewer.*

---

## 📂 File Structure

```text
Eklavya.me_Assignment/
├── frontend/               # Next.js Application
│   ├── app/
│   │   ├── api/generate/   # Vercel Bridge (Connects to Render)
│   │   └── page.tsx        # Dashboard UI
│   └── public/             # Static Assets
├── backend/                # FastAPI Application
│   ├── agents/
│   │   ├── generator.py    # AI Content Architect (OpenRouter)
│   │   └── reviewer.py     # AI Quality Reviewer (OpenRouter)
│   ├── main.py             # Server Controller & Entry Point
│   └── requirements.txt    # Python Dependencies
├── README.md               # Documentation
├── 1.png / 2.png           # Screenshots
└── DEMO.mp4                # Product Walkthrough
```

---

## 🔗 API Architecture

### Frontend Bridge
- **Endpoint**: `/api/generate` (Internal Vercel Route)
- **Role**: Proxies requests from the browser to the Render backend to avoid CORS and Mixed Content issues.

### Backend Endpoint
- **URL**: `https://eklavya-me-assignment.onrender.com/generate`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "grade": 10,
    "topic": "Quantum Mechanics"
  }
  ```
- **Response**: Returns a structured `workflow` log and `final_content` object.

---

## 🚀 Core Features
- **Multi-Agent Pipeline**: Uses separate agents for content generation and quality assurance.
- **Dynamic Curriculum**: Tailors vocabulary and complexity based on student grade levels.
- **Resilient Engine**: Powered by OpenRouter (Gemini 2.0 Flash) with automatic fallback systems.
- **Modern UI**: A premium, "Neo-Brutalism" inspired dashboard built with Next.js.

---

## 🛠️ Technology Stack
- **Frontend**: Next.js 15, TypeScript, Vanilla CSS
- **Backend**: FastAPI (Python), Uvicorn
- **AI Engine**: OpenRouter (Gemini 2.0 Flash)
- **Deployment**: Vercel (Frontend), Render (Backend)

---

## 🏃‍♂️ Quick Start

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python main.py`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

---

Built with ❤️ for the future of education.
