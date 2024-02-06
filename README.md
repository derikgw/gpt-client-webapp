# OpenAI Playground Flask App

This project is a Flask-based web application designed to generate code snippets using OpenAI's GPT-4 API. It allows users to input a prompt and a programming language, and returns a code snippet generated by GPT-4 that matches the input criteria.

## Features

- Generate code snippets using GPT-4 based on user input.
- Supports specifying the programming language for the code snippet.
- Utilizes Flask for a simple web interface.

## Installation

Before installing, ensure you have Python 3.6+ and pip installed.

1. Clone this repository.
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory.
   ```
   cd <project-directory>
   ```
3. Install the required dependencies.
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the application, follow these steps:

1. Start the Flask app.
   ```
   python main.py
   ```
2. Open a web browser and go to `http://localhost:5005/`.
3. Enter a prompt and select a programming language.
4. Submit the form to receive a generated code snippet.

## API Key Configuration

This application requires an OpenAI API key. Place your API key in a file named `api_key.txt` in the root directory of the project.

Ensure you have an OpenAI API key to use the GPT-4 features.

## Dependencies

- Flask
- openai-python
- markdown
- Prism

## Syntax Highlighting with Prism.js

This application uses Prism.js for syntax highlighting in the generated code snippets, enhancing readability and user experience. To integrate Prism.js:

1. Include Prism.css in your HTML to style the code snippets:
   ```html
   <link href="static/css/prism.css" rel="stylesheet" />
   ```
2. Include Prism.js before the closing `</body>` tag to enable highlighting:
   ```html
   <script src="static/js/prism.js"></script>
   ```
3. Ensure your code snippets are within `<pre><code class="language-xxx">...</code></pre>` tags, replacing `xxx` with the appropriate programming language identifier.

For more information on Prism.js and its usage, visit the [Prism.js website](https://prismjs.com/).

## License

This project is licensed under the Apache License 2.0. This license grants you broad permissions to use, modify, and distribute this software, provided that you include proper attribution to the original authors and an explicit grant of patent rights from contributors. It's a permissive license that comes with a few requirements to ensure the freedom of use and distribution is maintained, encouraging both commercial and non-commercial use. For more details on the Apache License 2.0, please visit the official Apache Foundation website or review the LICENSE file included in this repository.

