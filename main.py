import os

from flask import g, session

from session.user import User

import logging
from logging.handlers import RotatingFileHandler
from utility.app_factory import create_app

from asgiref.wsgi import WsgiToAsgi

os.environ['FLASK_DEBUG'] = "0"

# Flag for mocking GPT calls
mock_gpt_call = os.environ.get('MOCK_GPT_CALL', 'False') == 'True'
mock_response_file = os.environ.get('MOCK_RESPONSE_FILE', 'data/mock_response.md')

# Get the directory where main.py is located
directory = os.path.dirname(os.path.abspath(__file__))
# Pass this directory to the create_app function
app, openai_playground, socketio = create_app(base_directory=directory, mock_gpt_call=mock_gpt_call, mock_response_file=mock_response_file)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.current_user = None
    else:
        g.current_user = User.query.get(user_id)


@app.context_processor
def inject_user():
    return {'current_user': g.get('current_user', None)}

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    # Wrap the Flask application in an ASGI application
    asgi_app.run(app, host='0.0.0.0', port=80)
