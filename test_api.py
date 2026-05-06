import requests
import json

BASE_URL = "http://localhost:7003"

def test_spam(message):
    print(f"Testing message: {message[:50]}...")
    try:
        response = requests.post(f"{BASE_URL}/detect-spam", json={"message": message})
        if response.status_code == 200:
            result = response.json()
            print(f"Result: {result['classification']}")
            print(f"Score: {result['spam_score']}%")
            print(f"Reasons: {', '.join(result['reasons'])}")
            print("-" * 30)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}. Is the server running?")

if __name__ == "__main__":
    # Test cases
    test_spam("Congratulations! You've won a free prize. Click here now!")
    test_spam("Hi, how are you doing today? Let's catch up soon.")
    test_spam("URGENT: YOUR ACCOUNT WILL BE CLOSED UNLESS YOU ACT NOW!!!")
