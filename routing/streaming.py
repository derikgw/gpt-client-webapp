import re

import markdown
from flask import Blueprint, Response, request, session
from flask_socketio import SocketIO, emit
from markupsafe import escape
from session.governance import requires_login
from session.user import User

streaming_bp = Blueprint('streaming', __name__)

socketio = SocketIO()


def init(app, openai_playground):
    socketio.init_app(app, cors_allowed_origins="gpt.derikwilson.com")

    @socketio.on('start_stream')
    def handle_start_stream(data):
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        prompt = data['prompt']
        response_id = data['responseId']

        # Buffer to store incoming partial markdown content
        buffer = ''

        # Simulated streaming from openai_playground
        for response in openai_playground.generate_code(prompt):

            # Placeholder for triple backticks
            placeholder = "#TRIPLEBACKTICK#"

            # Process the response
            response = re.sub(r'```', placeholder, response)
            response = response.replace('`', "'")
            response = response.replace(placeholder, "```")

            html_content = markdown.markdown(response, extensions=["fenced_code"])
            # Emit the HTML content
            emit('stream_response', {'response_id': response_id, 'response': html_content})
            # Update the buffer with the remaining content

    # Register the blueprint with the app
    app.register_blueprint(streaming_bp)
