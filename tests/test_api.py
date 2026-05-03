import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    print("--- Testing Root Endpoint ---")
    response = requests.get(f"{BASE_URL}/")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    print("Root check passed!\n")

def test_chat():
    print("--- Testing Chat Endpoint ---")
    payload = {"question": "Which merchant has highest fraud?"}  # ✅ Works!
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(response.text)
    
    if response.status_code == 200:
        result = response.json()
        if "response" in result:
            print("✅ Response from Chatbot:")
            print(result["response"])
        else:
            print("Unexpected format:", result)
    else:
        print(f"❌ Error {response.status_code}:", response.text)

if __name__ == "__main__":
    try:
        test_root()
        test_chat()
    except requests.exceptions.ConnectionError:
        print("Server not running. Start: uvicorn main:app --reload")