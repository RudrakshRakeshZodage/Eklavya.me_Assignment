import json
import re

def extract_json(text: str):
    """
    Extracts a JSON object from a string that might contain other text.
    """
    try:
        # Try finding the first '{' and last '}'
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            return json.loads(json_str)
        return json.loads(text)
    except Exception as e:
        print(f"JSON Parsing Error: {e}")
        print(f"Original Text: {text}")
        raise e
