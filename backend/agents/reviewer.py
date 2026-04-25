import os
import json
import google.generativeai as genai
from typing import Dict, Any, Optional
from openai import OpenAI

class ReviewerAgent:
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
        
        try:
            if self.use_openrouter:
                response = self.client.chat.completions.create(
                    model="google/gemini-flash-1.5",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                resp_text = json.loads(response.choices[0].message.content)
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
                    resp_text = json.loads(content)
                except Exception as e:
                    print(f"DEBUG: Raw Reviewer Output: {response.text}")
                    print(f"ERROR: Failed to parse reviewer JSON: {str(e)}")
                    raise e
        except Exception as e:
            print(f"ERROR in ReviewerAgent: {e}")
            raise e
            
        return resp_text

def extract_json(text: str) -> Dict[str, Any]:
    try:
        # Basic JSON extraction
        if "{" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        return json.loads(text)
    except:
        return {{"error": "Failed to extract JSON"}}
