import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

from urllib.parse import quote

from utility.db_utility import init_app, create_tables
from utility.openai_playground import OpenAIPlayground

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

    app.config['MOCK_GPT_CALL'] = mock_gpt_call
    app.config['MOCK_RESPONSE_FILE'] = mock_response_file
    app.config['SECRET_KEY'] = os.environ.get('GPT_WEB_APP_AUTH_SECRET')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.environ.get('DB_USER')}:{quote(os.environ.get('DB_PASS'))}@"
        f"{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME', 'gpt_client')}"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    csrf = CSRFProtect(app)

    talisman = Talisman(app, content_security_policy={
        'default-src': [
            '\'self\'',  # Allows resources from the same origin
        ],
        'script-src': [
            '\'self\'',  # Allows scripts hosted on your domain
            'https://cdn.jsdelivr.net',  # Allows specific external scripts
            'https://cdn.socket.io',
        ],
        'style-src': [
            '\'self\'',  # Allows CSS hosted on your domain
        ],
        'img-src': [
            '\'self\'',  # Allows images from the same origin
            # Include other trusted image sources here if necessary
        ],
        'connect-src': [
            '\'self\'',  # Allows AJAX requests to your domain
            # Include other domains if you're making requests to external APIs
        ],
        'font-src': [
            '\'self\'',  # Allows fonts from the same origin
            # Add external font sources here if you use them
        ],
        'object-src': '\'none\'',  # Disallows all object/embed plugins
        # Add other directives as needed
    })

    bcrypt = Bcrypt(app)
    api_key = os.environ.get('OPENAI_API_KEY')

    openai_playground = OpenAIPlayground(
        api_key=api_key,
        mock_gpt_call=app.config['MOCK_GPT_CALL'],
        mock_response_file=app.config['MOCK_RESPONSE_FILE']
    )

    # Initialize the database, register blueprints, etc.
    init_app(app)

    stream_routing.init(app, openai_playground)
    auth_routing.init(app, openai_playground)
    dashboard_routing.init(app, openai_playground)
    prompt_routing.init(app, openai_playground)
    generation_routing.init(app, openai_playground)
    profile_routing.init(app, openai_playground)
    admin_routing.init(app, openai_playground)

    with app.app_context():
        create_tables(app)

    return app, openai_playground
