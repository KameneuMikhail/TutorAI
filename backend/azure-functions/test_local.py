"""
Local test script to test the function logic without Azure Functions runtime
"""
import sys
import json
from unittest.mock import Mock

# Add the function directory to path
sys.path.insert(0, 'get_subjects')

# Import the function
from __init__ import main

def create_mock_request(lang=None, accept_language=None):
    """Create a mock HTTP request with optional language parameters"""
    mock_request = Mock()
    mock_request.method = "GET"
    mock_request.url = "http://localhost:7071/api/get_subjects"
    mock_request.params = {"lang": lang} if lang else {}
    mock_request.headers = {"Accept-Language": accept_language} if accept_language else {}
    return mock_request

def test_function():
    """Test the get_subjects function locally with localization"""
    print("Testing get_subjects function with localization...")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Default language (Russian)
    print("\n1. Testing default language (Russian)...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request()
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        print(f"Content-Language: {response.headers.get('Content-Language', 'N/A')}")
        
        assert response.status_code == 200
        assert isinstance(response_data, list)
        assert "Математика" in response_data, "Should contain Russian 'Математика'"
        assert "Английский" in response_data, "Should contain Russian 'Английский'"
        assert len(response_data) == 2
        
        print("✅ Default (Russian) test passed!")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 2: English via query parameter
    print("\n2. Testing English via query parameter (lang=en)...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request(lang="en")
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response_data, indent=2)}")
        print(f"Content-Language: {response.headers.get('Content-Language', 'N/A')}")
        
        assert response.status_code == 200
        assert isinstance(response_data, list)
        assert "Math" in response_data
        assert "English" in response_data
        assert len(response_data) == 2
        
        print("✅ English (query param) test passed!")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Russian via query parameter
    print("\n3. Testing Russian via query parameter (lang=ru)...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request(lang="ru")
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        
        assert response.status_code == 200
        assert "Математика" in response_data
        assert "Английский" in response_data
        
        print("✅ Russian (query param) test passed!")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 4: English via Accept-Language header
    print("\n4. Testing English via Accept-Language header...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request(accept_language="en-US,en;q=0.9")
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response_data, indent=2)}")
        
        assert response.status_code == 200
        assert "Math" in response_data
        assert "English" in response_data
        
        print("✅ English (header) test passed!")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    if tests_passed == total_tests:
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

if __name__ == "__main__":
    success = test_function()
    sys.exit(0 if success else 1)
