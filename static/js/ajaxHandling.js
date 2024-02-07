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
                // your existing code to update response
                const historyContainer = document.querySelector(".conversation-history");
                const newPrompt = document.createElement("div");
                newPrompt.className = "prompt-box";
                newPrompt.innerHTML = '<strong>Prompt:</strong><p>${data.prompt}</p>';
                const newResponse = document.createElement("div");
                newResponse.className = "response-box";
                newResponse.innerHTML = '<strong>Response:</strong><pre>${data.response}</pre><button class="copy-button">Copy</button>';
                historyContainer.appendChild(newPrompt);
                historyContainer.appendChild(newResponse);

                // Clear input field after submission
                document.getElementById("promptInput").value = "";
                window.scrollTo(0, document.body.scrollHeight);
            })
            .catch(error => console.error('Error:', error));
    });
});
