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

# Use OpenRouter Key only
OR_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize Agents
generator = GeneratorAgent(api_key=OR_KEY)
reviewer = ReviewerAgent(api_key=OR_KEY)

class GenerationRequest(BaseModel):
    grade: int
    topic: str

@app.post("/generate")
async def generate_content(request: GenerationRequest):
    try:
        print(f"Pipeline: Grade {request.grade} - {request.topic}")
        
        # Phase 1: Generation
        content = generator.generate(request.grade, request.topic)
        
        # Phase 2: Review
        review_result = reviewer.review(content, request.grade)
        
        # Phase 3: Final Output
        response_data = {
            "workflow": [
                {
                    "agent": "Architect",
                    "status": "success"
                },
                {
                    "agent": "Reviewer",
                    "status": "pass" if review_result.get("status") == "APPROVED" else "fail",
                    "feedback": [review_result.get("feedback", "Looks good!")]
                }
            ],
            "final_content": review_result.get("reviewed_content", content)
        }
        
        return response_data
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
