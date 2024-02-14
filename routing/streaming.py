import markdown
from flask import Blueprint, Response, request, session
from flask_socketio import SocketIO, emit
from markupsafe import escape
from session.governance import requires_login
from session.user import User

streaming_bp = Blueprint('streaming', __name__)

socketio = SocketIO()


def init(app, openai_playground):
    socketio.init_app(app)

    @socketio.on('start_stream')
    def handle_start_stream(data):
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        prompt = data['prompt']
        response_id = data['responseId']

        # Simulated streaming from openai_playground
        for response in openai_playground.generate_code(prompt):
            md_template_string = markdown.markdown(
                response, extensions=["fenced_code"]
            )
            emit('stream_response', {'response_id': response_id, 'response': md_template_string})

    # Register the blueprint with the app
    app.register_blueprint(streaming_bp)
