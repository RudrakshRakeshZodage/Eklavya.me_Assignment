import json
import os
from typing import Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ReviewerAgent:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://eklavya.me",
                "X-Title": "Eklavya.me Assignment"
            }
        )

    def review(self, content: Dict[str, Any], grade: int) -> Dict[str, Any]:
        content_str = json.dumps(content, indent=2)
        
        prompt = f"""
        You are an educational content Reviewer Agent.
        Your task is to evaluate content generated for a Grade {grade} student.

        Evaluation Criteria:
        1. Age appropriateness: Is the language and complexity right for Grade {grade}?
        2. Conceptual correctness: Are the facts and explanations accurate?
        3. Clarity: Is the content easy to understand?

        Input Content:
        {content_str}

        The output must be a valid JSON object with the following structure:
        {{
            "status": "pass" or "fail",
            "feedback": ["List of specific issues or 'Content looks great'"]
        }}

        Be strict. If even one sentence is too complex or a fact is slightly off, mark it as "fail" and provide specific feedback.
        """

        response = self.client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct:free",
            messages=[
                {"role": "system", "content": "You are a critical reviewer that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
