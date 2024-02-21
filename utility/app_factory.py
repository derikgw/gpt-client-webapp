import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

import logging
from logging.handlers import RotatingFileHandler

from utility.db_utility import init_app, create_tables
from utility.openai_playground import OpenAIPlayground

from werkzeug.middleware.proxy_fix import ProxyFix

# Assuming you have an init_streaming function in extensions.streaming
import routing.streaming as stream_routing
import routing.auth as auth_routing
import routing.dashboard as dashboard_routing
import routing.prompt as prompt_routing
import routing.generation as generation_routing
import routing.profile as profile_routing
import routing.admin_panel as admin_routing


def create_app(base_directory=None, mock_gpt_call=False, mock_response_file=None):
    if base_directory is None:
        base_directory = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__, root_path=base_directory)
    # Existing configuration setup

    logging.basicConfig(level=logging.INFO)  # Set the log level you want
    handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    app.config['MOCK_GPT_CALL'] = mock_gpt_call
    app.config['MOCK_RESPONSE_FILE'] = mock_response_file
    app.config['SECRET_KEY'] = os.environ.get('GPT_WEB_APP_AUTH_SECRET')
    database_dir = os.path.join(base_directory, 'data')
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    database_path = os.path.join(database_dir, 'users.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(database_path)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # ToDo: Read origins in from a config file.
    # cors_origins = ["http://gpt.derikwilson.com", "https://gpt.derikwilson.com"]
    # Fetch the environment variable and split it into a list
    cors_origins = os.environ.get('CORS_ORIGINS', "http://defaultorigin.com").split(',')
    app.logger.info(f"Origins being loaded: {cors_origins}")

    CORS(app, resources={r"/*": {"origins": cors_origins}}, supports_credentials=True)
    socketio = SocketIO(app, cors_allowed_origins=cors_origins, monitor_clients=True, logger=True, engineio_logger=True,
                        methods=["GET", "POST"], cors_credentials=True)

    bcrypt = Bcrypt(app)
    api_key = os.environ.get('OPENAI_API_KEY')

    openai_playground = OpenAIPlayground(
        api_key=api_key,
        mock_gpt_call=app.config['MOCK_GPT_CALL'],
        mock_response_file=app.config['MOCK_RESPONSE_FILE']
    )

    # Initialize the database, register blueprints, etc.
    init_app(app)

    database_path = os.path.join(database_dir, 'users.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(database_path)

    stream_routing.init(app, openai_playground)
    auth_routing.init(app, openai_playground)
    dashboard_routing.init(app, openai_playground)
    prompt_routing.init(app, openai_playground)
    generation_routing.init(app, openai_playground)
    profile_routing.init(app, openai_playground)
    admin_routing.init(app, openai_playground)

    with app.app_context():
        create_tables(app)

    return app, openai_playground, socketio
