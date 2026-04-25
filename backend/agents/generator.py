import json
import os
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeneratorAgent:
    def __init__(self, api_key: str = None):
        if api_key:
            genai.configure(api_key=api_key)
        else:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, grade: int, topic: str, feedback: str = None) -> Dict[str, Any]:
        prompt = f"""
        You are an educational content Generator Agent.
        Your task is to generate educational content for a student in Grade {grade} on the topic: "{topic}".

        The output must be a valid JSON object with the following structure:
        {{
            "explanation": "A clear, age-appropriate explanation of the topic.",
            "mcqs": [
                {{
                    "question": "A question about the topic.",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "The correct option (A, B, C, or D)"
                }}
            ]
        }}

        Guidelines:
        - Use language suitable for a Grade {grade} student.
        - Ensure conceptual correctness.
        - Generate 3 MCQs.
        """

        if feedback:
            prompt += f"\n\nRefinement Request:\nPrevious output was rejected with the following feedback:\n{feedback}\nPlease regenerate the content addressing this feedback."

        response = self.model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)
