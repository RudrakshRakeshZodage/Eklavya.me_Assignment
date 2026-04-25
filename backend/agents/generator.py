import os
import json
import google.generativeai as genai
from typing import Dict, Any, Optional
from openai import OpenAI

class GeneratorAgent:
    def __init__(self, api_key: str, or_key: Optional[str] = None):
        if or_key:
            self.use_openrouter = True
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
            # Use the verified model name from list_gemini_models.py
            for model_name in ['models/gemini-flash-latest', 'gemini-1.5-flash', 'gemini-pro']:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    break
                except:
                    continue

    def generate(self, grade: int, topic: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        prompt = f"""
        Generate educational content for Grade {grade} on the topic: {topic}.
        
        {f"Incorporate this feedback: {feedback}" if feedback else ""}
        
        Return your response in EXACTLY this JSON format:
        {{
            "title": "Title of the content",
            "explanation": "Brief explanation (100-200 words)",
            "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
            "quiz": [
                {{
                    "question": "Question text",
                    "options": ["A", "B", "C", "D"],
                    "answer": "Correct Option Text"
                }}
            ]
        }}
        """
        
        try:
            if self.use_openrouter:
                response = self.client.chat.completions.create(
                    model="google/gemini-flash-1.5",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            else:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                    )
                )
                # Clean the output
                content = response.text
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                try:
                    return json.loads(content)
                except Exception as e:
                    print(f"DEBUG: Raw Generator Output: {response.text}")
                    print(f"ERROR: Failed to parse generator JSON: {str(e)}")
                    raise e
        except Exception as e:
            print(f"ERROR in GeneratorAgent: {e}")
            raise e
