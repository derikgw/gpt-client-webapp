function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}

window.onload = function() {
    // Existing onload functionality to load history
    let history = JSON.parse(sessionStorage.getItem('history')) || [];
    let historyContainer = document.querySelector('.conversation-history');

    history.forEach(item => {
        let promptDiv = document.createElement('div');
        promptDiv.className = 'prompt-box';
        promptDiv.innerHTML = `<strong>Prompt:</strong><p>${item.prompt}</p>`;

        let responseDiv = document.createElement('div');
        responseDiv.className = 'response-box';
        responseDiv.innerHTML = `<strong>Response:</strong><pre>${item.response}</pre>`;

        historyContainer.appendChild(promptDiv);
        historyContainer.appendChild(responseDiv);
    });

    // Call Prism to highlight all after the history is loaded
    Prism.highlightAll();

    // Call scrollToBottom after the history is loaded and highlighted
    scrollToBottom();
};

function clearHistory() {
    // Clear the session storage
    sessionStorage.removeItem('history');

    // Clear the history from the page
    const historyContainer = document.querySelector('.conversation-history');
    historyContainer.innerHTML = '';

    // Add any additional logic if you need to notify the user or handle other elements
}
