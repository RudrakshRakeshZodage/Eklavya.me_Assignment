import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent

load_dotenv()

app = FastAPI(title="Eklavya.me Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize Agents with BOTH keys for fallback
generator = GeneratorAgent(api_key=GEMINI_API_KEY, or_key=OPENROUTER_API_KEY)
reviewer = ReviewerAgent(api_key=GEMINI_API_KEY, or_key=OPENROUTER_API_KEY)

class GenerationRequest(BaseModel):
    grade: int
    topic: str

@app.post("/generate")
async def generate_content(request: GenerationRequest):
    try:
        print(f"Generation Request: Grade {request.grade}, Topic: {request.topic}")
        
        # Phase 1: Generation
        content = generator.generate(request.grade, request.topic)
        
        # Phase 2: Review
        review_result = reviewer.review(content, request.grade)
        
        # Phase 3: Final Output
        return {
            "status": review_result.get("status", "APPROVED"),
            "feedback": review_result.get("feedback", "Looks good!"),
            "data": review_result.get("reviewed_content", content)
        }
        
    except Exception as e:
        print(f"BACKEND ERROR: {str(e)}")
        # If both fail, return the error
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Use PORT from environment (Render requirement)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
