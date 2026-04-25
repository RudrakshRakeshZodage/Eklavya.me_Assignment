import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI

class GeneratorAgent:
    def __init__(self, api_key: str, or_key: Optional[str] = None):
        # We now only use the OpenRouter key (passed as or_key)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=or_key or api_key, # Use whichever is provided
            default_headers={
                "HTTP-Referer": "https://eklavya.me",
                "X-Title": "Eklavya.me Assignment"
            }
        )

    def generate(self, grade: int, topic: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        prompt = f"""
        Generate educational content for Grade {grade} on the topic: {topic}.
        Return your response in EXACTLY this JSON format:
        {{
            "title": "Title of the content",
            "explanation": "Brief explanation (100-200 words)",
            "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
            "mcqs": [
                {{
                    "question": "Question text",
                    "options": ["A", "B", "C", "D"],
                    "answer": "Correct Option Text"
                }}
            ]
        }}
        """
        
        print(f"Generator: Calling OpenRouter for {topic}...")
        
        # Using the model that we know works!
        response = self.client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
