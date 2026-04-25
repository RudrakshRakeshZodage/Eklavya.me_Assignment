import os
import json
import google.generativeai as genai
from typing import Dict, Any, Optional
from openai import OpenAI

class GeneratorAgent:
    def __init__(self, api_key: str, or_key: Optional[str] = None):
        self.api_key = api_key
        self.or_key = or_key
        
        # Initialize Gemini
        genai.configure(api_key=api_key)
        self.gemini_model = None
        for model_name in ['models/gemini-flash-latest', 'gemini-1.5-flash', 'gemini-pro']:
            try:
                self.gemini_model = genai.GenerativeModel(model_name)
                break
            except:
                continue
                
        # Initialize OpenRouter
        if or_key:
            self.or_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=or_key,
                default_headers={
                    "HTTP-Referer": "https://eklavya.me",
                    "X-Title": "Eklavya.me Assignment"
                }
            )
        else:
            self.or_client = None

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
        
        # Try Gemini First
        try:
            print("Generator: Trying Gemini...")
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            content = response.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            return json.loads(content)
            
        except Exception as e:
            print(f"Generator: Gemini failed or hit quota: {e}")
            
            # Fallback to OpenRouter
            if self.or_client:
                print("Generator: Falling back to OpenRouter...")
                try:
                    response = self.or_client.chat.completions.create(
                        model="google/gemini-flash-1.5",
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )
                    return json.loads(response.choices[0].message.content)
                except Exception as or_e:
                    print(f"Generator: OpenRouter also failed: {or_e}")
                    raise e
            else:
                raise e
