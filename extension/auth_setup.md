# Microsoft Authentication Setup

## 1. Register App in Azure Portal

1. Go to https://portal.azure.com
2. Navigate to "Azure Active Directory" > "App registrations"
3. Click "New registration"
4. Set:
   - Name: "Email Phishing Detector"
   - Redirect URI: `http://localhost:5000/callback`
5. Copy the Application (client) ID

## 2. Create Client Secret

1. Go to "Certificates & secrets"
2. Click "New client secret"
3. Copy the secret value

## 3. Update Configuration

In `src/app.py`, replace:
```python
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
```

## 4. Test Authentication

1. Start Flask app: `python src/app.py`
2. Load extension in Chrome
3. Click "Login with Microsoft"
4. Complete authentication
5. Extension will now require login before analysis