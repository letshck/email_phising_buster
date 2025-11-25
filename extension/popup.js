document.addEventListener('DOMContentLoaded', async function() {
  const loginBtn = document.getElementById('login-btn');
  const logoutBtn = document.getElementById('logout-btn');
  const analyzeBtn = document.getElementById('analyze-btn');
  const extractBtn = document.getElementById('extract-btn');
  const emailText = document.getElementById('email-text');
  const resultDiv = document.getElementById('result');
  const authSection = document.getElementById('auth-section');
  const analysisSection = document.getElementById('analysis-section');
  const userInfo = document.getElementById('user-info');

  // Check if user is logged in
  await checkAuthStatus();

  async function checkAuthStatus() {
    try {
      const response = await fetch('http://localhost:5000/user', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const user = await response.json();
        showLoggedInState(user);
      } else {
        showLoggedOutState();
      }
    } catch (error) {
      showLoggedOutState();
    }
  }

  function showLoggedInState(user) {
    authSection.style.display = 'none';
    analysisSection.style.display = 'block';
    userInfo.innerHTML = `Welcome, ${user.displayName}`;
  }

  function showLoggedOutState() {
    authSection.style.display = 'block';
    analysisSection.style.display = 'none';
    userInfo.innerHTML = '';
  }

  loginBtn.addEventListener('click', function() {
    chrome.tabs.create({ url: 'http://localhost:5000/login' });
  });

  logoutBtn.addEventListener('click', async function() {
    await fetch('http://localhost:5000/logout', { credentials: 'include' });
    showLoggedOutState();
  });

  analyzeBtn.addEventListener('click', async function() {
    const text = emailText.value.trim();
    
    if (!text) {
      resultDiv.innerHTML = '<div class="result">Please enter email text to analyze</div>';
      return;
    }

    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.disabled = true;

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ text: text })
      });

      const result = await response.json();

      if (response.ok) {
        const isPhishing = result.prediction === 'phishing';
        const className = isPhishing ? 'phishing' : 'legitimate';
        const icon = isPhishing ? '⚠️' : '✅';
        
        resultDiv.innerHTML = `
          <div class="result ${className}">
            ${icon} <strong>${result.prediction.toUpperCase()}</strong><br>
            Confidence: ${result.confidence}%<br>
            Phishing: ${result.probability.phishing}%<br>
            Legitimate: ${result.probability.legitimate}%
          </div>
        `;
      } else {
        resultDiv.innerHTML = `<div class="result">Error: ${result.error}</div>`;
      }
    } catch (error) {
      resultDiv.innerHTML = `<div class="result">Connection error. Make sure the API is running on localhost:5000</div>`;
    }

    analyzeBtn.textContent = 'Analyze Email';
    analyzeBtn.disabled = false;
  });

  extractBtn.addEventListener('click', async function() {
    extractBtn.textContent = 'Extracting...';
    extractBtn.disabled = true;

    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractEmail' });
      
      if (response && response.content) {
        emailText.value = response.content;
        resultDiv.innerHTML = '<div class="result">Email content extracted! Click "Analyze Email" to check for phishing.</div>';
      } else {
        resultDiv.innerHTML = '<div class="result">No email content found. Make sure you\'re on Gmail, Outlook, or Yahoo Mail with an email open.</div>';
      }
    } catch (error) {
      resultDiv.innerHTML = '<div class="result">Error extracting email. Make sure you\'re on a supported email provider.</div>';
    }

    extractBtn.textContent = 'Analyze Current Email';
    extractBtn.disabled = false;
  });
});