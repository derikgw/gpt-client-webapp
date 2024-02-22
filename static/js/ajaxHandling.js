document.addEventListener("DOMContentLoaded", function () {

    var protocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
    var socket = io.connect(protocol + '//' + document.domain + ':' + location.port, {
        reconnection: true, // Enable auto-reconnection
        reconnectionAttempts: 5, // Number of attempts before giving up
        reconnectionDelay: 2000, // Delay between reconnection attempts
        reconnectionDelayMax: 5000, // Maximum delay between attempts
    });

    // Load conversation history if exists
    const savedHistory = localStorage.getItem('conversationHistory');
    if (savedHistory) {
        document.querySelector(".conversation-history").innerHTML = savedHistory;
    }

    document.getElementById("promptForm").addEventListener("submit", function (e) {
        e.preventDefault();
        const prompt = document.getElementById("promptInput").value;

        // Clear the input after submitting
        document.getElementById("promptInput").value = '';

        const historyContainer = document.querySelector(".conversation-history");
        const uniqueId = `response-${uuidv4()}`; // Generate a unique ID for the pair

        // Create the prompt box div
        const promptBox = document.createElement("div");
        promptBox.className = "prompt-box";
        promptBox.innerHTML = `<strong>Prompt:</strong><p>${prompt}</p>`;

        // Create the response box div
        const responseBox = document.createElement("div");
        responseBox.className = "response-box";
        responseBox.innerHTML = `<strong>Response:</strong><div id="${uniqueId}"></div><button class="copy-button" onclick="copyToClipboard(this)">Copy</button>`;

        historyContainer.appendChild(promptBox)
        historyContainer.appendChild(responseBox)

        // After appending the promptBox and responseBox to the historyContainer
        localStorage.setItem('conversationHistory', historyContainer.innerHTML);

        // Send the prompt to the server using WebSocket
        socket.emit('start_stream', {prompt: prompt, responseId: uniqueId});
        // socket.emit('start_stream', {prompt: null, responseId: uniqueId});
    });

    // Listen for streamed responses from the server
    socket.on('stream_response', function (data) {
        let responseBox = document.getElementById(data.response_id)
        let responseContent = document.createElement("div")
        // Correct use of DOMPurify with template literals
        responseContent.innerHTML = DOMPurify.sanitize(`${data.response}`);

        responseBox.appendChild(responseContent);

        // Now, find all <code> elements within the responseContent and highlight each
        responseContent.querySelectorAll('code').forEach((block) => {
            Prism.highlightElement(block);
        });

        // After appending the promptBox and responseBox to the historyContainer
        const historyContainer = document.querySelector(".conversation-history");
        localStorage.setItem('conversationHistory', historyContainer.innerHTML);
    });

    socket.on('reconnect_attempt', () => {
        console.log(`Reconnect attempt...`);
    });

    // Handle reconnection failure
    socket.on('reconnect_failed', () => {
        console.log(`Reconnection failed. No more attempts will be made.`);
    });
});


// Function to copy response text to clipboard
function copyToClipboard(button) {
    const pre = button.previousElementSibling; // Assuming the <pre> tag is right before the button
    navigator.clipboard.writeText(pre.textContent).then(function () {
        console.log('Copying to clipboard was successful!');
    }, function (err) {
        console.error('Could not copy text: ', err);
    });
}

// Function to clear conversation history
function clearHistory() {
    const historyContainer = document.querySelector(".conversation-history");
    historyContainer.innerHTML = '';
    localStorage.setItem('conversationHistory', historyContainer.innerHTML);
}

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
        .replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
}
