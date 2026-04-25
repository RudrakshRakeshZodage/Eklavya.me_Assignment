import os
import json
import google.generativeai as genai
from typing import Dict, Any, Optional
from openai import OpenAI

class ReviewerAgent:
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

    def review(self, content: Dict[str, Any], grade: int) -> Dict[str, Any]:
        content_str = json.dumps(content, indent=2)
        
        prompt = f"""
        Review the following educational content for Grade {grade}.
        
        Content:
        {content_str}
        
        Check for:
        1. Accuracy of information.
        2. Appropriate language for Grade {grade}.
        3. Quality of the quiz question.
        
        If it's good, return it as is. If not, provide feedback for improvement.
        Return your response in EXACTLY this JSON format:
        {{
            "status": "APPROVED" or "REJECTED",
            "feedback": "Your detailed feedback if REJECTED, or 'Looks good!' if APPROVED",
            "reviewed_content": {{ ... same structure as input ... }}
        }}
        """
        
        # Try Gemini First
        try:
            print("Reviewer: Trying Gemini...")
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            resp_text = response.text
            if "```json" in resp_text:
                resp_text = resp_text.split("```json")[1].split("```")[0].strip()
            return json.loads(resp_text)
            
        except Exception as e:
            print(f"Reviewer: Gemini failed or hit quota: {e}")
            
            # Fallback to OpenRouter
            if self.or_client:
                print("Reviewer: Falling back to OpenRouter...")
                try:
                    response = self.or_client.chat.completions.create(
                        model="google/gemini-flash-1.5",
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )
                    return json.loads(response.choices[0].message.content)
                except Exception as or_e:
                    print(f"Reviewer: OpenRouter also failed: {or_e}")
                    raise e
            else:
                raise e
