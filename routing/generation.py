# generation.py
from flask import Blueprint, request, jsonify, flash, redirect, current_app
from utility.safe_urls import get_safe_redirect
from session.governance import requires_login
from markupsafe import escape
import markdown
import markdown.extensions.fenced_code
import re

generation_bp = Blueprint('generation', __name__, template_folder='templates')


def init(app, openai_playground):
    @generation_bp.route('/generate', methods=['POST'])
    @requires_login
    def generate():
        try:
            prompt = escape(request.form.get('prompt'))

            # Initialize an array to hold the contents of each file
            file_contents = []

            # Check if files were uploaded
            files = request.files.getlist('files')
            if files:
                for file in files:
                    if file.filename == '':
                        flash('No selected file')
                        redirect(get_safe_redirect(request.url))
                    if file:  # If there is a file
                        # Read the content of the file
                        file_content = file.read().decode('utf-8')  # Assuming text files encoded in UTF-8
                        file_contents.append(file_content)

            # Possibly concatenate file contents with the original prompt
            files_text = '\n'.join(file_contents)
            full_prompt = f"{prompt}\n\n{files_text}"  # Adjust as needed

            # Send the concatenated prompt to GPT-4 API
            response = openai_playground.generate_code(full_prompt)

            # Process and return the response...
            placeholder = "{TRIPPLETICKS}"
            response_processed = re.sub(r'```', placeholder, response)
            response_processed = response_processed.replace('`', "'")
            response_processed = response_processed.replace(placeholder, "```")
            md_template_string = markdown.markdown(response_processed, extensions=["fenced_code"])

            return jsonify({"prompt": full_prompt, "response": md_template_string})

        except Exception as e:
            current_app.logger.error("An exception occurred: %s", str(e))
            return jsonify({"error": "There was an error generating the response.  Please see application log for "
                                     "details."}), 500

    # Register the blueprint with the app
    app.register_blueprint(generation_bp)
