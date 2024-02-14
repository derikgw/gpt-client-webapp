from flask import Blueprint, Response, request, session
from flask_socketio import SocketIO, emit
from markupsafe import escape
from session.governance import requires_login
from session.user import User

streaming_bp = Blueprint('streaming', __name__)

socketio = SocketIO()


def init(app, openai_playground):
    socketio.init_app(app)

    @streaming_bp.route('/generate_stream', methods=['POST'])
    @requires_login
    def generate_stream(prompt):

        def generate():
            # Use openai_playground passed as an argument to generate code
            for chunk in openai_playground.generate_code(prompt):
                yield f"data: {chunk}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    @socketio.on('start_stream')
    def handle_start_stream(data):
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        prompt = data['prompt']

        # Simulated streaming from openai_playground
        for response in openai_playground.generate_code(prompt):
            emit('stream_response', {'response': response})

    # Register the blueprint with the app
    app.register_blueprint(streaming_bp)
