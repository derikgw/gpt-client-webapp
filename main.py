import os
import re
from openai import OpenAI
import markdown
from flask import Flask, request, url_for, render_template
import markdown.extensions.fenced_code

os.environ['FLASK_DEBUG'] = "1"

# Flag for mocking GPT calls
MOCK_GPT_CALL = True  # Set to False to use the real API
MOCK_RESPONSE_FILE = "data/mock_response.md"  # Path to your mock response markdown file

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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        # programming_language = request.form.get('programming_language')
        # code = openai_playground.generate_code(prompt, programming_language)
        code = openai_playground.generate_code(prompt)

        # Placeholder for triple backticks
        placeholder = "#TRIPLEBACKTICK#"

        # Substitute triple backticks with the placeholder
        code = re.sub(r'```', placeholder, code)

        # Convert remaining single backticks to an apostrophe
        code = code.replace('`', "'")
        code = code.replace(f"{placeholder}", "```")

        md_template_string = markdown.markdown(
            code, extensions=["fenced_code"]
        )

        return render_template('index.html', code=md_template_string, prompt=prompt)

    return render_template('index.html', prompt=openai_playground.prompt)


if __name__ == '__main__':
    # debug = os.environ.get("FLASK_DEBUG") == "1"
    # app.run(debug=debug, use_reloader=not (debug and os.environ.get("PYCHARM_DEBUG") == "1"))
    app.run(debug=True, port=5005)
