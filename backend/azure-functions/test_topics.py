"""
Test script for get_topics function
"""
import sys
import json
from unittest.mock import Mock

# Add the function directory to path
sys.path.insert(0, 'get_topics')

# Import the function
from __init__ import main

def create_mock_request(subject=None, lang=None, method="GET", body=None):
    """Create a mock HTTP request"""
    mock_request = Mock()
    mock_request.method = method
    mock_request.url = f"http://localhost:7071/api/get_topics?subject={subject}" if subject else "http://localhost:7071/api/get_topics"
    mock_request.params = {"subject": subject, "lang": lang} if subject and lang else ({"subject": subject} if subject else {})
    mock_request.headers = {"Accept-Language": lang} if lang else {}
    
    if body:
        mock_request.get_json = Mock(return_value=body)
    else:
        mock_request.get_json = Mock(side_effect=ValueError("No JSON body"))
    
    return mock_request

def test_topics():
    """Test the get_topics function"""
    print("Testing get_topics function...")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Math topics in Russian (default)
    print("\n1. Testing Math topics in Russian (default)...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request(subject="Math")
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        print(f"Number of topics: {len(response_data)}")
        print(f"First topic: {response_data[0] if response_data else 'N/A'}")
        
        assert response.status_code == 200
        assert isinstance(response_data, list)
        assert len(response_data) > 0
        
        print("✅ Math topics (Russian) test passed!")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 2: English topics in Russian
    print("\n2. Testing English topics in Russian...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request(subject="English")
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        print(f"Number of topics: {len(response_data)}")
        
        assert response.status_code == 200
        assert isinstance(response_data, list)
        assert len(response_data) > 0
        
        print("✅ English topics (Russian) test passed!")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Math topics in English
    print("\n3. Testing Math topics in English (lang=en)...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request(subject="Math", lang="en")
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        print(f"First topic: {response_data[0] if response_data else 'N/A'}")
        
        assert response.status_code == 200
        assert isinstance(response_data, list)
        assert len(response_data) > 0
        
        print("✅ Math topics (English) test passed!")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Missing subject parameter
    print("\n4. Testing missing subject parameter...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request()
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        print(f"Error message: {response_data.get('error', 'N/A')}")
        
        assert response.status_code == 400
        assert "error" in response_data
        
        print("✅ Missing subject test passed!")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 5: POST request with JSON body
    print("\n5. Testing POST request with JSON body...")
    print("-" * 60)
    total_tests += 1
    try:
        mock_request = create_mock_request(method="POST", body={"subject": "Math"})
        response = main(mock_request)
        response_data = json.loads(response.get_body().decode('utf-8'))
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        assert isinstance(response_data, list)
        
        print("✅ POST with JSON body test passed!")
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
    success = test_topics()
    sys.exit(0 if success else 1)
