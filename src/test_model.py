import joblib

# Load saved model and vectorizer
model = joblib.load('../models/phishing_model.pkl')
vectorizer = joblib.load('../models/vectorizer.pkl')

# Example test email
sample_email = ["Your account is blocked! Click here to verify immediately."]

# Convert text to vector
features = vectorizer.transform(sample_email)

# Predict
prediction = model.predict(features)

print("Prediction:", "Spam" if prediction[0] == 1 else "Not Spam")
