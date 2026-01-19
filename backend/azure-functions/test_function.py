"""
Simple test script to test the Azure Function locally.
Run this after starting the function with: func start
"""
import requests
import json

def test_get_subjects():
    """Test the get_subjects function"""
    url = "http://localhost:7071/api/get_subjects"
    
    try:
        print("Testing GET request...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"
        assert "Math" in response.json(), "Math should be in the list"
        assert "English" in response.json(), "English should be in the list"
        
        print("✅ All tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to function. Make sure it's running with 'func start'")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_get_subjects()
