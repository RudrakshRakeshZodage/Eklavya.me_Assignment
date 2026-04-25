import json
import os
from typing import Dict, Any, List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ReviewerAgent:
    def __init__(self, api_key: str = None):
        if api_key:
            genai.configure(api_key=api_key)
        else:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')

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

        response = self.model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)
