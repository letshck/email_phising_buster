import joblib
import os

# Define correct paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "phishing_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

# Load model and vectorizer
print("🔄 Loading model and vectorizer...")
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
print("✅ Model and vectorizer loaded successfully!\n")

def predict_email(email_text: str) -> str:
    """
    Predict whether an email text is phishing or legitimate.
    """
    if not email_text.strip():
        return "error: empty email text"

    # Convert text to features
    features = vectorizer.transform([email_text])
    
    return "phishing" if prediction == 1 else "legit"


# CLI Test
if __name__ == "__main__":
    while True:
        text = input("\nEnter email text (or 'q' to quit):\n> ")
        if text.lower() == 'q':
            break
        print(f"🔍 Prediction: {predict_email(text).upper()}")
