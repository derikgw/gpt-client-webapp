import os
import re
from openai import OpenAI
import markdown
from flask import Flask, request, url_for, jsonify, render_template
import markdown.extensions.fenced_code

os.environ['FLASK_DEBUG'] = "1"

# Flag for mocking GPT calls
MOCK_GPT_CALL = False  # Set to False to use the real API
MOCK_RESPONSE_FILE = "data/mock_response.md"  # Path to your mock response markdown file

# Store the conversation history
conversation_history = []


class OpenAIPlayground:
    def __init__(self, api_key):
        self.api_key = api_key
        self.engine = "gpt-4-0125-preview"
        self.prompt = ''
        # self.programming_language = ''

    # def generate_code(self, prompt, programming_language):
    def generate_code(self, prompt):

        if MOCK_GPT_CALL:
            # Read the mock response from the markdown file
            with open(MOCK_RESPONSE_FILE, 'r') as file:
                return file.read()

        client = OpenAI()
        client.api_key = self.api_key
        self.prompt = prompt

        completion_prompt = f"{prompt}:"
        completion = client.chat.completions.create(
            model=self.engine,
            messages=[{"role": "user", "content": f"{completion_prompt}"}],
            stream=True
        )

        fullResponse = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                # Directly append the content to fullResponse without stripping colons
                fullResponse += chunk.choices[0].delta.content

        # After the loop, strip whitespace and remove the trailing colon if it's there
        fullResponse = fullResponse.strip()
        if fullResponse.endswith(':'):
            fullResponse = fullResponse[:-1]

        return fullResponse

        # return "Code generation failed"


def read_api_key():
    with open('api_key.txt', 'r') as file:
        return file.read().strip()


app = Flask(__name__)
api_key = read_api_key()
os.environ['OPENAI_API_KEY'] = api_key
openai_playground = OpenAIPlayground(api_key)


@app.route('/generate', methods=['POST'])
def generate():

    prompt = request.form.get('prompt')
    response = openai_playground.generate_code(prompt)

    # Process the response as before
    placeholder = "#TRIPLEBACKTICK#"
    response_processed = re.sub(r'```', placeholder, response)
    response_processed = response_processed.replace('`', "'")
    response_processed = response_processed.replace(placeholder, "```")
    md_template_string = markdown.markdown(response_processed, extensions=["fenced_code"])

    # Optionally, append the new prompt and response to the conversation history
    conversation_history.append({"prompt": prompt, "response": md_template_string})

    # Return just the processed response for AJAX to insert into the page
    return jsonify({"prompt": prompt, "response": md_template_string})


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        code = openai_playground.generate_code(prompt)

        # Placeholder for triple backticks
        placeholder = "#TRIPLEBACKTICK#"

        # Process the response
        code = re.sub(r'```', placeholder, code)
        code = code.replace('`', "'")
        code = code.replace(placeholder, "```")

        md_template_string = markdown.markdown(
            code, extensions=["fenced_code"]
        )

        # Pass the conversation history to the template
        htmlString = render_template('index.html',
                                     code=md_template_string,
                                     prompt=prompt,
                                     conversation_history=conversation_history)

        # Append the new prompt and response to the conversation history
        conversation_history.append({"prompt": prompt, "response": md_template_string})
        return htmlString

    # Also pass the conversation history when rendering the GET request
    htmlString = render_template('index.html',
                                 prompt=openai_playground.prompt,
                                 conversation_history=conversation_history)

    return htmlString


if __name__ == '__main__':
    # debug = os.environ.get("FLASK_DEBUG") == "1"
    # app.run(debug=debug, use_reloader=not (debug and os.environ.get("PYCHARM_DEBUG") == "1"))
    app.run(debug=True, port=5005)
