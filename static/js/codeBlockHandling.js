document.addEventListener('DOMContentLoaded', function() {
    // Function to create Copy buttons
    function addCopyButtons() {
        const preCodeBlocks = document.querySelectorAll('pre code');

        preCodeBlocks.forEach(block => {
            const button = document.createElement('button');
            button.textContent = 'Copy';
            button.className = 'copy-code-button';
            button.addEventListener('click', function() {
                navigator.clipboard.writeText(block.innerText).then(() => {
                    button.textContent = 'Copied!';
                    setTimeout(() => button.textContent = 'Copy', 2000);
                }).catch(err => console.error('Copy failed', err));
            });

            const pre = block.parentNode;
            pre.insertBefore(button, pre.firstChild);
        });
    }

    addCopyButtons();
});


document.addEventListener('DOMContentLoaded', function () {
    // Highlight all code blocks with Prism
    Prism.highlightAll();

    // Select all code blocks
    var codeBlocks = document.querySelectorAll('pre code');

    // Loop through each code block and append the copy button
    codeBlocks.forEach(appendCopyButton);
});

document.querySelector('.generate-button').addEventListener('click', function () {
    var prompt = document.querySelector('.prompt-input').value;
    var form = document.createElement('form');
    form.method = 'post';
    form.action = '/';
    var promptInput = document.createElement('input');
    promptInput.type = 'hidden';
    promptInput.name = 'prompt';
    promptInput.value = prompt;
    var languageInput = document.createElement('input');
    languageInput.type = 'hidden';
    form.appendChild(promptInput);
    form.appendChild(languageInput);
    document.body.appendChild(form);
    form.submit();
});