import os
import json
import google.generativeai as genai
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from utils import extract_json

load_dotenv()

class GeneratorAgent:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            # Fallback to OpenRouter if Gemini key not found
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

    def generate(self, grade: int, topic: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        prompt = f"""
        You are an educational content Generator Agent.
        Target Student: Grade {grade}
        Topic: {topic}
        """
        
        if feedback:
            prompt += f"\nPrevious feedback to incorporate: {feedback}\n"
            
        prompt += """
        Generate:
        1. A clear, age-appropriate explanation of the topic.
        2. 3 Multiple Choice Questions (MCQs) with 4 options and 1 correct answer each.

        The output must be a valid JSON object with the following structure:
        {
            "explanation": "Detailed explanation text...",
            "mcqs": [
                {
                    "question": "Question text?",
                    "options": ["A", "B", "C", "D"],
                    "answer": "Correct option text"
                }
            ]
        }
        """

        try:
            if self.use_openrouter:
                response = self.client.chat.completions.create(
                    model="nvidia/nemotron-3-super-120b-a12b:free",
                    messages=[
                        {"role": "system", "content": "You are a helpful educational assistant that outputs JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
            else:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                    )
                )
                content = response.text
        except Exception as e:
            print(f"ERROR in GeneratorAgent: {e}")
            raise e

        result = extract_json(content)
        
        # Ensure standard structure
        if not isinstance(result, dict):
            result = {"explanation": str(result), "mcqs": []}
        
        if "explanation" not in result:
            result["explanation"] = "No explanation provided."
        if "mcqs" not in result:
            result["mcqs"] = []
            
        return result
