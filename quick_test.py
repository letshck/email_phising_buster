import requests

# Test data
test_email = "URGENT: Your account has been locked! Click here to verify: http://suspicious-link.com"

# Make the request
try:
    response = requests.post(
        'http://localhost:5000/predict',
        json={'text': test_email}
    )
    
    print("\nTest Results:")
    print("-" * 50)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Status: Success")
        print(f"Prediction: {result['prediction'].upper()}")
        print(f"Confidence: {result['confidence']}%")
        print("\nProbability Breakdown:")
        print(f"Legitimate: {result['probability']['legitimate']}%")
        print(f"Phishing: {result['probability']['phishing']}%")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Error connecting to server: {str(e)}")