function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}

// Call scrollToBottom when the window finishes loading
window.onload = scrollToBottom;