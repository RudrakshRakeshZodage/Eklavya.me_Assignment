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
        workflow.append(AgentStep(
            agent="Reviewer",
            status=review_result["status"],
            output=review_result,
            feedback=review_result["feedback"]
        ))
        
        final_content = initial_content
        
        # Step 3: Refinement (if failed)
        if review_result["status"] == "fail":
            feedback_str = "\n".join(review_result["feedback"])
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
