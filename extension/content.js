// Content script to extract email content from web pages
function extractEmailContent() {
  // Gmail
  if (window.location.hostname.includes('mail.google.com')) {
    const emailBody = document.querySelector('[data-message-id] .ii.gt div');
    return emailBody ? emailBody.innerText : null;
  }
  
  // Outlook
  if (window.location.hostname.includes('outlook.')) {
    const emailBody = document.querySelector('[role="main"] [aria-label*="message"]');
    return emailBody ? emailBody.innerText : null;
  }
  
  // Yahoo Mail
  if (window.location.hostname.includes('mail.yahoo.com')) {
    const emailBody = document.querySelector('[data-test-id="message-view-body-content"]');
    return emailBody ? emailBody.innerText : null;
  }
  
  return null;
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'extractEmail') {
    const emailContent = extractEmailContent();
    sendResponse({ content: emailContent });
  }
});