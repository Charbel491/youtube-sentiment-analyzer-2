// Retourne les commentaires visibles (texte brut)
function extractComments() {
  const spans = document.querySelectorAll('#content-text');
  return Array.from(spans)
              .map(s => s.innerText.trim())
              .filter(t => t.length > 0);
}

// Écoute message depuis popup
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "getComments") {
    const comments = extractComments();
    sendResponse({ comments });
  }
});