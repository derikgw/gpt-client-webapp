// Function to create and append the copy button
function appendCopyButton(codeBlock) {
    var copyBtn = document.createElement('button');
    copyBtn.className = 'copy-button';
    copyBtn.textContent = 'Copy';

    // Event listener for the copy button
    copyBtn.addEventListener('click', function () {
        var range = document.createRange();
        range.selectNodeContents(codeBlock);
        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);

        // Execute the copy command
        try {
            var successful = document.execCommand('copy');
            if (successful) {
                // Change button text to 'Copied!'
                this.innerText = 'Copied!';
                // Revert button text back to 'Copy' after 2 seconds
                setTimeout(() => this.innerText = 'Copy', 2000);
            } else {
                alert('Failed to copy code.');
            }
        } catch (err) {
            console.log('Oops, unable to copy');
        }

        // Remove the selection range (deselect)
        selection.removeAllRanges();
    });

    // Append the copy button just before the code element
    codeBlock.parentNode.insertBefore(copyBtn, codeBlock);
}

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