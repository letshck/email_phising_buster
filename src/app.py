from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import logging

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained model and vectorizer
try:
    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    model = joblib.load(os.path.join(model_dir, 'phishing_model.pkl'))
    vectorizer = joblib.load(os.path.join(model_dir, 'vectorizer.pkl'))
    logger.info("✅ Model and vectorizer loaded successfully!")
except Exception as e:
    logger.error(f"❌ Error loading model: {str(e)}")
    model = None
    vectorizer = None

@app.route('/')
def home():
    if model is None or vectorizer is None:
        return "❌ Model not loaded properly. Check server logs.", 500
    return """
    ✅ Phishing Detection API is running!
    
    POST /predict
    {
        "text": "Your email text here"
    }
    """

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        return jsonify({
            'error': 'Model not loaded properly. Please check server logs.'
        }), 500

    try:
        # Receive text data from POST request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400
            
        email_text = data.get('text', '').strip()
        
        if not email_text:
            return jsonify({
                'error': 'No email text provided'
            }), 400

        # Transform text using the vectorizer
        features = vectorizer.transform([email_text])

        # Get prediction and probability
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        # Get confidence score
        confidence = max(probability) * 100

        # Prepare response
        result = {
            'prediction': 'phishing' if prediction == 1 else 'legitimate',
            'confidence': round(confidence, 2),
            'probability': {
                'legitimate': round(probability[0] * 100, 2),
                'phishing': round(probability[1] * 100, 2)
            }
        }

        logger.info(f"Processed text: '{email_text[:50]}...' - Result: {result['prediction']} ({result['confidence']}%)")
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Error processing request',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    # Make the server accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
