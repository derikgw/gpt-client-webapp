import markdown
import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify

from session.governance import requires_login
from markupsafe import escape

prompt_bp = Blueprint('prompt', __name__, template_folder='templates')


def init(app, openai_playground):
    @prompt_bp.route('/prompt', methods=['GET', 'POST'])
    @requires_login
    def prompt():
        if request.method == 'POST':
            prompt_content = request.form.get('prompt')
            prompt_content = escape(prompt_content)
            # code = openai_playground.generate_code(prompt_content)

            # Placeholder for triple backticks
            placeholder = "#TRIPLEBACKTICK#"

            # Process the response
            code = ''.join(openai_playground.generate_code(prompt_content))
            code = re.sub(r'```', placeholder, code)
            code = code.replace('`', "'")
            code = code.replace(placeholder, "```")

            md_template_string = markdown.markdown(
                code, extensions=["fenced_code"]
            )

            # Pass the conversation history to the template
            html_string = render_template('prompt.html',
                                          code=md_template_string,
                                          prompt=prompt_content)

            return html_string

        # Also pass the conversation history when rendering the GET request
        html_string = render_template('prompt.html',
                                      prompt=openai_playground.prompt)
        # conversation_history=conversation_history)

        return html_string

    # Register the blueprint with the app
    app.register_blueprint(prompt_bp)
