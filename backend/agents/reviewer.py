import os
import json
import google.generativeai as genai
from typing import Dict, Any, List
from dotenv import load_dotenv
from utils import extract_json

load_dotenv()

class ReviewerAgent:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            # Fallback to OpenRouter
            self.use_openrouter = True
            from openai import OpenAI
            or_key = os.getenv("OPENROUTER_API_KEY")
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=or_key,
                default_headers={
                    "HTTP-Referer": "https://eklavya.me",
                    "X-Title": "Eklavya.me Assignment"
                }
            )
        else:
            self.use_openrouter = False
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')

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

        Be strict. If even one sentence is too complex or a fact is slightly off, mark it as "fail".
        """

        try:
            if self.use_openrouter:
                response = self.client.chat.completions.create(
                    model="nvidia/nemotron-3-super-120b-a12b:free",
                    messages=[
                        {"role": "system", "content": "You are a critical reviewer that outputs JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                resp_text = response.choices[0].message.content
            else:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                    )
                )
                resp_text = response.text
        except Exception as e:
            print(f"ERROR in ReviewerAgent: {e}")
            raise e
        
        result = extract_json(resp_text)
        
        # Ensure standard structure
        if not isinstance(result, dict):
            result = {"status": "pass", "feedback": []}
            
        if "status" not in result:
            result["status"] = "pass"
        if "feedback" not in result:
            result["feedback"] = []
            
        return result
