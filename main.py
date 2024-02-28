import os

from flask import g, session

from session.user import User

import logging
from logging.handlers import RotatingFileHandler
from utility.app_factory import create_app

# Import the blueprints

os.environ['FLASK_DEBUG'] = "0"

# Flag for mocking GPT calls
mock_gpt_call = os.environ.get('MOCK_GPT_CALL', 'False') == 'True'
mock_response_file = os.environ.get('MOCK_RESPONSE_FILE', 'data/mock_response.md')

# Get the directory where main.py is located
directory = os.path.dirname(os.path.abspath(__file__))
# Pass this directory to the create_app function
app, openai_playground = create_app(base_directory=directory, mock_gpt_call=mock_gpt_call, mock_response_file=mock_response_file)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.current_user = None
    else:
        g.current_user = User.query.get(user_id)

@app.after_request
def set_csp_header(response):
    csp_policy = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net;"
    response.headers['Content-Security-Policy'] = csp_policy
    return response

@app.context_processor
def inject_user():
    return {'current_user': g.get('current_user', None)}


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)  # Set the log level you want
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    if os.environ.get('FLASK_ENV') == 'development':
        cert_path = os.path.expanduser('~/.ssh/devcert.pem')
        key_path = os.path.expanduser('~/.ssh/devkey.pem')
        app.run(host='0.0.0.0', port=5005, ssl_context=(cert_path, key_path))
    else:
        app.run(host='0.0.0.0', port=443)
