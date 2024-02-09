document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("promptForm").addEventListener("submit", function (e) {
        e.preventDefault();  // Prevent the default form submission
        const prompt = document.getElementById("promptInput").value; // Get the prompt from the form

        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'prompt=' + encodeURIComponent(prompt)
        })
        .then(response => response.json())
        .then(data => {
            // Assuming you update the page with the response here
            const historyContainer = document.querySelector(".conversation-history");
            const newPrompt = document.createElement("div");
            newPrompt.className = "prompt-box";
            newPrompt.textContent = `<strong>Prompt:</strong><pre><code>${data.prompt}</code></pre>`; // Use backticks for template literals
            const newResponse = document.createElement("div");
            newResponse.className = "response-box";
            newResponse.textContent = `<strong>Response:</strong><pre>${data.response}</pre><button class="copy-button">Copy</button>`; // Use backticks for template literals

            // Corrected logic to store history
            let history = JSON.parse(sessionStorage.getItem('history')) || [];
            history.push({prompt: data.prompt, response: data.response}); // Correct variable names
            sessionStorage.setItem('history', JSON.stringify(history));

            // Append new elements to the history container
            historyContainer.appendChild(newPrompt);
            historyContainer.appendChild(newResponse);

            // Clear input field after submission
            document.getElementById("promptInput").value = "";
            window.scrollTo(0, document.body.scrollHeight);
        })
        .catch(error => console.error('Error:', error));
    });
});


