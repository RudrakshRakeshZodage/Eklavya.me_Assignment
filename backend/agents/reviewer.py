import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI

class ReviewerAgent:
    def __init__(self, api_key: str, or_key: Optional[str] = None):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=or_key or api_key,
            default_headers={
                "HTTP-Referer": "https://eklavya.me",
                "X-Title": "Eklavya.me Assignment"
            }
        )

    def review(self, content: Dict[str, Any], grade: int) -> Dict[str, Any]:
        content_str = json.dumps(content, indent=2)
        
        prompt = f"""
        Review this educational content for Grade {grade}:
        {content_str}
        
        Return exactly this JSON:
        {{
            "status": "APPROVED",
            "feedback": "Your feedback",
            "reviewed_content": {{ ... same as input ... }}
        }}
        """
        
        print("Reviewer: Calling OpenRouter Reviewer...")
        
        response = self.client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
