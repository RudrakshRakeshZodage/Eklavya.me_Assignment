import json
import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GeneratorAgent:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

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

        response = self.client.chat.completions.create(
            model="google/gemini-flash-1.5",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
