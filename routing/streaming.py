from flask import Blueprint, Response, request
from flask_socketio import SocketIO, emit
from markupsafe import escape
from session.governance import requires_login

streaming_bp = Blueprint('streaming', __name__)


def init(app, openai_playground):
    socketio = SocketIO(app)

    @streaming_bp.route('/generate_stream', methods=['POST'])
    @requires_login
    def generate_stream(prompt):

        def generate():
            # Use openai_playground passed as an argument to generate code
            for chunk in openai_playground.generate_code(prompt):
                yield f"data: {chunk}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    def start_stream():
        # Start your stream based on the received prompt
        # This logic will depend on your specific application
        pass

    @socketio.on('start_stream')
    def handle_start_stream(json):
        prompt = json['prompt']

        # Start streaming and periodically emit 'stream_response' events with the streamed data
        for response in generate_stream(prompt):
            emit('stream_response', {'response': response})

    # Register the blueprint with the app
    app.register_blueprint(streaming_bp)
