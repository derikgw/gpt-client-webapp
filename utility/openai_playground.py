# This file contains the OpenAIPlayground class as previously defined in main.py
from flask import jsonify
from openai import OpenAI, OpenAIError


class OpenAIPlayground:
    def __init__(self, api_key, mock_gpt_call=False, mock_response_file=None):
        self.api_key = api_key
        self.engine = "gpt-4-0125-preview"
        self.mock_gpt_call = mock_gpt_call
        self.mock_response_file = mock_response_file
        self.prompt = ""  # Initialize prompt attribute here

    def generate_code(self, prompt):
        try:
            if self.mock_gpt_call:
                # Read the mock response from the markdown file
                with open(self.mock_response_file, 'r') as file:
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

            full_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    # Directly append the content to full_response without stripping colons
                    full_response += chunk.choices[0].delta.content

            # After the loop, strip whitespace and remove the trailing colon if it's there
            full_response = full_response.strip()
            if full_response.endswith(':'):
                full_response = full_response[:-1]

            return full_response

        except OpenAIError as e:
            error_msg = e.args[0]  # Extracting the error message from the exception
            return jsonify({"error": error_msg}), 400  # Return error message and status code
