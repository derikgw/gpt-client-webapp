document.addEventListener("DOMContentLoaded", function () {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    document.getElementById("promptForm").addEventListener("submit", function (e) {
        e.preventDefault();
        const prompt = document.getElementById("promptInput").value;

        // Send the prompt to the server using WebSocket
        socket.emit('start_stream', {prompt: prompt});
    });

    // Listen for streamed responses from the server
    socket.on('stream_response', function(data) {
        const historyContainer = document.querySelector(".conversation-history");
        const newResponse = document.createElement("div");
        newResponse.className = "response-box";
        newResponse.innerHTML = `<strong>Response:</strong><pre>${data.response}</pre><button class="copy-button">Copy</button>`;
        historyContainer.appendChild(newResponse);
    });
});


fetch('/generate', {
    method: 'POST',
    body: formData,
})
    .then(response => {
        if (!response.ok) {
            throw response;
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            // Display the error on the webpage
            document.getElementById("responseContainer").innerText = data.error;
        } else {
            // Handle success response
        }
    })
    .catch(errorResponse => {
        // Handle network errors or other non-2xx responses
        errorResponse.json().then(errorData => {
            // Display the error on the webpage
            document.getElementById("responseContainer").innerText = errorData.error;
        });
    });

var eventSource = new EventSource("/generate_stream");
eventSource.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var conversationHistoryDiv = document.querySelector(".conversation-history");

    var entryDiv = document.createElement("div");
    entryDiv.innerHTML = `
        <div class="prompt-box">
            <strong>Prompt:</strong>
            <p>${data.prompt}</p>
        </div>
        <div class="response-box">
            <strong>Response:</strong>
            <pre>${data.response}</pre>
            <button class="copy-button">Copy</button>
        </div>
    `;
    conversationHistoryDiv.appendChild(entryDiv);
};

