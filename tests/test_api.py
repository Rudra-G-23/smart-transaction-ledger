import requests

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    # Test Root
    res = requests.get(f"{BASE_URL}/")
    print(f"Root: {res.json()}")

    # Test Chat
    res = requests.post(f"{BASE_URL}/chat", json={"question": "Total users & Total Spending?"})
    print(f"Chat: {res.json()}")

if __name__ == "__main__":
    test_api()