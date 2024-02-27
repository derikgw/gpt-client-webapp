import os
from flask import Flask
from flask_bcrypt import Bcrypt
from utility.db_utility import init_app, create_tables
from utility.openai_playground import OpenAIPlayground
from flask_wtf.csrf import CSRFProtect

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

    database_dir = os.path.join(base_directory, 'data')
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    database_path = os.path.join(database_dir, 'users.db')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(database_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@"
        f"{os.environ.get('DB_HOST', 'dgw-gpt-web-app-db-1.c14eqauu2cjj.us-east-2.rds.amazonaws.com')}/{os.environ.get('DB_NAME', 'gpt_client')}"
    )

    print(app.config['SQLALCHEMY_DATABASE_URI'])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    csrf = CSRFProtect(app)
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
