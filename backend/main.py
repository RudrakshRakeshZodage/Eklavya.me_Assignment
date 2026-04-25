from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Educational Agent Pipeline")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    grade: int
    topic: str

class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class Content(BaseModel):
    explanation: str
    mcqs: List[MCQ]

class AgentStep(BaseModel):
    agent: str
    status: str
    output: Any
    feedback: Optional[List[str]] = None

class FinalResponse(BaseModel):
    workflow: List[AgentStep]
    final_content: Content

@app.post("/generate", response_model=FinalResponse)
async def generate_content(request: GenerationRequest):
    try:
        print(f"DEBUG: Generating content for Grade {request.grade}, Topic: {request.topic}")
        or_key = os.getenv("OPENROUTER_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if gemini_key:
            print(f"DEBUG: Gemini Key found (starts with {gemini_key[:10]}...)")
        elif or_key:
            print(f"DEBUG: Falling back to OpenRouter (starts with {or_key[:10]}...)")
        else:
            print("DEBUG: NO API KEYS FOUND!")
            
        generator = GeneratorAgent()
        reviewer = ReviewerAgent()
        
        workflow = []
        
        # Step 1: Initial Generation
        initial_content = generator.generate(request.grade, request.topic)
        workflow.append(AgentStep(
            agent="Generator",
            status="success",
            output=initial_content
        ))
        
        # Step 2: Review
        review_result = reviewer.review(initial_content, request.grade)
        status = review_result.get("status", "pass")
        feedback = review_result.get("feedback", [])
        
        workflow.append(AgentStep(
            agent="Reviewer",
            status=status,
            output=review_result,
            feedback=feedback
        ))
        
        final_content = initial_content
        
        # Step 3: Refinement (if failed)
        if status == "fail":
            feedback_str = "\n".join(feedback)
            refined_content = generator.generate(request.grade, request.topic, feedback=feedback_str)
            
            # Final Review of Refined Content (Simplified: we trust the refinement for the 1-pass limit)
            workflow.append(AgentStep(
                agent="Generator (Refinement)",
                status="success",
                output=refined_content
            ))
            final_content = refined_content

        return FinalResponse(
            workflow=workflow,
            final_content=final_content
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
