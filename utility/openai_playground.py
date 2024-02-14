# This file contains the OpenAIPlayground class as previously defined in main.py
import os

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
                messages=[{"role": "user", "content": f"{prompt}: "}],
                stream=True
            )

            file_path = "debug_chunks.txt"
            # Check if the file exists
            if os.path.exists(file_path):
                # Delete the file
                os.remove(file_path)

            buffered_response = ""
            in_code_block = False
            finish_code_block = False
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:

                    # Buffer the response content
                    buffered_response += chunk.choices[0].delta.content

                    if finish_code_block:
                        finish_code_block = False
                    else:
                        if '``' in chunk.choices[0].delta.content or '```' in chunk.choices[0].delta.content:
                            in_code_block = not in_code_block
                            if '```' not in chunk.choices[0].delta.content:
                                buffered_response += '`'
                                yield buffered_response
                                buffered_response = ""  # Reset the buffer after yielding
                                finish_code_block = True

                        if not in_code_block:
                            if '\n' in buffered_response or '.' in buffered_response:
                                yield buffered_response
                                buffered_response = ""  # Reset the buffer after yielding

            # After the loop, yield any remaining buffered content
            if buffered_response:
                yield buffered_response

        except OpenAIError as e:
            error_msg = e.args[0]  # Extracting the error message from the exception
            return jsonify({"error": error_msg}), 400  # Return error message and status code
