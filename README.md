# OpenAI Playground Flask App

This Flask-based web application leverages OpenAI's GPT-4 API to generate code snippets based on user inputs, including the desired programming language. It features a simple web interface for seamless interaction.

## Features

- **Code Snippet Generation:** Utilizes GPT-4 to produce code snippets from user prompts.
- **Language Support:** Allows specification of the programming language for generated snippets.
- **Flask Framework:** Employs Flask for an intuitive web interface.

## Technical Requirements

### Python Version
Developed with Python 3.12.1, ensuring compatibility and performance. Please use this version to avoid any issues.

### Prism Syntax Highlighter
For enhanced code readability, this application integrates Prism.js with the Twilight theme, supporting Markup, CSS, C-like, and JavaScript. Customization options are available via the [Prism configuration page](https://prismjs.com/download.html#themes=prism-twilight&languages=markup+css+clike+javascript).

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/derikgw/gpt-client-webapp.git
   ```
2. **Navigate to the project directory:**
   ```
   cd <project-directory>
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Launch the Flask app:
   ```
   python main.py
   ```
2. Visit `http://localhost:5005/` in your browser.
3. Input a prompt and choose a programming language.
4. Submit to receive the GPT-4 generated code snippet.

## API Key Configuration

Store your OpenAI API key in `api_key.txt` at the project's root to enable GPT-4 features.

## Dependencies

- Flask for web serving.
- openai-python for API interactions.
- Markdown for documentation.
- Prism for syntax highlighting.

## Syntax Highlighting with Prism.js

Prism.js enhances the presentation of generated code. Include `prism.css` and `prism.js` in your HTML to enable this feature, wrapping code snippets in `<pre><code>` tags with the correct language class.

## Contributing

Contributions are welcome! Please submit issues and pull requests through GitHub, adhering to the provided contribution guidelines.

## License

Licensed under the Apache License 2.0, offering extensive freedoms and protections. See the LICENSE file or visit the [Apache Foundation](https://www.apache.org/licenses/LICENSE-2.0) for full details.
