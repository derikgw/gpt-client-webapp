document.addEventListener("DOMContentLoaded", function () {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    document.getElementById("promptForm").addEventListener("submit", function (e) {
        e.preventDefault();
        const prompt = document.getElementById("promptInput").value;

        // Clear the input after submitting
        document.getElementById("promptInput").value = '';

        // Send the prompt to the server using WebSocket
        socket.emit('start_stream', {prompt: prompt});
    });

    // Listen for streamed responses from the server
    socket.on('stream_response', function(data) {
        const historyContainer = document.querySelector(".conversation-history");

        // Create the prompt box div
        const promptBox = document.createElement("div");
        promptBox.className = "prompt-box";
        promptBox.innerHTML = `<strong>Prompt:</strong><p>${data.prompt}</p>`;

        // Create the response box div
        const responseBox = document.createElement("div");
        responseBox.className = "response-box";
        responseBox.innerHTML = `<strong>Response:</strong><pre>${data.response}</pre><button class="copy-button" onclick="copyToClipboard(this)">Copy</button>`;

        // Append the new prompt and response to the conversation history
        historyContainer.appendChild(promptBox);
        historyContainer.appendChild(responseBox);
    });
});

// Function to copy response text to clipboard
function copyToClipboard(button) {
    const pre = button.previousElementSibling; // Assuming the <pre> tag is right before the button
    navigator.clipboard.writeText(pre.textContent).then(function() {
        console.log('Copying to clipboard was successful!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

// Function to clear conversation history
function clearHistory() {
    const historyContainer = document.querySelector(".conversation-history");
    historyContainer.innerHTML = '';
}
