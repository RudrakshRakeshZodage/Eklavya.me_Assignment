import requests

try:
    response = requests.post(
        "http://localhost:8000/generate",
        json={"grade": 4, "topic": "Types of angles"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
