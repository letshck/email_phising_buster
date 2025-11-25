from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_cors import CORS
import joblib
import os
import logging
import requests
from functools import wraps

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
CORS(app, supports_credentials=True)  # Enable CORS for all routes

# Microsoft Auth Config
CLIENT_ID = '58672c424f8144a5b30d19cb483e611d'
CLIENT_SECRET = 'your-client-secret'
TENANT_ID = 'common'
REDIRECT_URI = 'http://localhost:5000/callback'
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPE = ['User.Read']

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

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    if model is None or vectorizer is None:
        return "❌ Model not loaded properly. Check server logs.", 500
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = f"{AUTHORITY}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=User.Read&response_mode=query"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No authorization code'}), 400
    
    token_url = f"{AUTHORITY}/oauth2/v2.0/token"
    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    
    if 'access_token' in token_json:
        # Get user info
        headers = {'Authorization': f"Bearer {token_json['access_token']}"}
        user_response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        user_info = user_response.json()
        
        session['user'] = user_info
        return jsonify({'message': 'Login successful', 'user': user_info})
    
    return jsonify({'error': 'Authentication failed'}), 400

@app.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out'})

@app.route('/user')
@require_auth
def get_user():
    return jsonify(session['user'])

@app.route('/predict', methods=['POST'])
@require_auth
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

        logger.info(f"User {session['user']['displayName']} processed text: '{email_text[:50]}...' - Result: {result['prediction']} ({result['confidence']}%)")
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
