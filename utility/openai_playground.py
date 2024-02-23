import os
from flask import jsonify
from openai import OpenAI, OpenAIError

class OpenAIPlayground:
    def __init__(self, api_key, mock_gpt_call=False, mock_response_file=None):
        # Initialize the OpenAIPlayground with an API key, and optional mocking behavior
        self.api_key = api_key  # API key for authenticating requests to OpenAI
        self.engine = "gpt-4-0125-preview"  # Specifies the GPT model to use
        self.mock_gpt_call = mock_gpt_call  # Flag to determine if responses should be mocked
        self.mock_response_file = mock_response_file  # File path for mocked responses
        self.prompt = ""  # Placeholder for storing the current prompt

    def generate_code(self, prompt):
        # Generates code based on the given prompt, either by calling OpenAI or using a mock response
        try:
            if self.mock_gpt_call:
                # If mocking is enabled, read the response from the specified file
                with open(self.mock_response_file, 'r') as file:
                    return file.read()

            # Set up the OpenAI client with the provided API key
            client = OpenAI()
            client.api_key = self.api_key
            self.prompt = prompt

            # Prepare and send the request to OpenAI
            completion_prompt = f"{prompt}:"
            completion = client.chat.completions.create(
                model=self.engine,
                messages=[{"role": "user", "content": f"{prompt}: "}],
                stream=True  # Stream responses to process them as they arrive
            )

            # Initialize variables for response processing
            file_path = "debug_chunks.txt"
            if os.path.exists(file_path):
                os.remove(file_path)  # Ensure a clean start by removing any existing file

            buffered_response = ""  # Buffer for accumulating response content
            in_code_block = False  # Flag to track if we're within a code block
            finish_code_block = False  # Flag to indicate the end of a code block

            # Process each chunk of the response
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    buffered_response += chunk.choices[0].delta.content

                    if finish_code_block:
                        finish_code_block = False
                    else:
                        # Toggle in_code_block flag if code block delimiters are found
                        if '``' in chunk.choices[0].delta.content or '```' in chunk.choices[0].delta.content:
                            in_code_block = not in_code_block
                            if '```' not in chunk.choices[0].delta.content:
                                # Handle incomplete code blocks
                                buffered_response += '`'
                                yield buffered_response
                                buffered_response = ""  # Clear buffer after yielding
                                finish_code_block = True

                        # Yield buffered content when outside code blocks and certain conditions are met
                        if not in_code_block:
                            if '\n' in buffered_response or '.' in buffered_response:
                                yield buffered_response
                                buffered_response = ""  # Clear buffer after yielding

            # Yield any remaining content in the buffer
            if buffered_response:
                yield buffered_response

        except OpenAIError as e:
            # Handle errors from the OpenAI API
            error_msg = e.args[0]  # Extract and return the error message
            return jsonify({"error": error_msg}), 400
