import os
import re

from openai import OpenAI, OpenAIError

import markdown
import markdown.extensions.fenced_code

from flask import Flask, request, url_for, redirect, jsonify, render_template, g, session
from flask_bcrypt import Bcrypt
from markupsafe import escape

from functools import wraps

from flask import flash
from datetime import datetime

import sqlalchemy

from utility.db_utility import db, init_app, create_tables
from session.user import User
from session.role import Role

from session.governance import requires_role, requires_login

import logging
from logging.handlers import RotatingFileHandler

# Import the blueprints
from admin.admin_panel import admin_bp
from session.governance import governance_bp
from session.profile import profile_bp

os.environ['FLASK_DEBUG'] = "0"

# Flag for mocking GPT calls
MOCK_GPT_CALL = False  # Set to False to use the real API
MOCK_RESPONSE_FILE = "data/mock_response.md"  # Path to your mock response markdown file


# Store the conversation history
# conversation_history = []


class OpenAIPlayground:
    def __init__(self, api_key):
        self.api_key = api_key
        self.engine = "gpt-4-0125-preview"
        self.prompt = ''
        # self.programming_language = ''

    # def generate_code(self, prompt, programming_language):
    def generate_code(self, prompt):
        try:
            if MOCK_GPT_CALL:
                # Read the mock response from the markdown file
                with open(MOCK_RESPONSE_FILE, 'r') as file:
                    return file.read()

            client = OpenAI()
            client.api_key = self.api_key
            self.prompt = prompt

            completion_prompt = f"{prompt}:"
            completion = client.chat.completions.create(
                model=self.engine,
                messages=[{"role": "user", "content": f"{completion_prompt}"}],
                stream=True
            )

            fullResponse = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    # Directly append the content to fullResponse without stripping colons
                    fullResponse += chunk.choices[0].delta.content

            # After the loop, strip whitespace and remove the trailing colon if it's there
            fullResponse = fullResponse.strip()
            if fullResponse.endswith(':'):
                fullResponse = fullResponse[:-1]

            return fullResponse


        except OpenAIError as e:
            error_msg = e.args[0]  # Extracting the error message from the exception
            return jsonify({"error": error_msg}), 400  # Return error message and status code


app = Flask(__name__)

data_directory = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

app.config['SECRET_KEY'] = os.environ.get('GPT_WEB_APP_AUTH_SECRET')
database_path = os.path.join(os.path.dirname(__file__), 'data', 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(database_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_app(app)  # Initialize the database with the Flask app

with app.app_context():
    create_tables(app)  # Create the database tables

# Register the admin blueprint
app.register_blueprint(admin_bp)
app.register_blueprint(governance_bp)
app.register_blueprint(profile_bp)

bcrypt = Bcrypt(app)

api_key = os.environ.get('OPENAI_API_KEY')
openai_playground = OpenAIPlayground(api_key)


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'error')
            return redirect(url_for('register'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        # Fetch the default role
        default_role = Role.query.filter_by(name='user').first()
        if not default_role:
            flash('Registration error: default role not found.', 'error')
            return redirect(url_for('register'))

        # Include email in the User creation
        user = User(username=username, email=email, password_hash=hashed_pw,
                    active=False, role=default_role)  # Set active to False initially
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            app.logger.error('An error occurred: %s', str(e))
            flash('This username is already taken.', 'error')
            return redirect(url_for('register'))

        flash('Your account has been created. Please wait for an admin to activate it.', 'success')
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        # If there is no user with that username, redirect to the registration page
        if user is None:
            flash('No account found with that username. Please register.', 'info')
            return redirect(url_for('register'))

        # If the user exists but the password is incorrect, return to login page with an error
        if not bcrypt.check_password_hash(user.password_hash, password):
            flash('Password is incorrect, please try again.', 'error')
            return render_template('login.html')

        if not user.active:
            flash('Your account is not active. Please contact an administrator.', 'warning')
            return render_template('login.html')

        # If the user exists and the password is correct, proceed to login
        session['user_id'] = user.id
        # Update last login time
        user.last_login = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
@requires_login
def logout():
    session.pop('user_id', None)
    return redirect('/login')


@app.route('/')
@app.route('/dashboard')
@requires_login
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])
    if user is None:
        # If the user is not found, they might have been deleted.
        session.pop('user_id', None)  # Clean up session
        return redirect('/login')

    # Pass the user's username to the dashboard template
    return render_template('dashboard.html', username=user.username)


from flask import flash


@app.route('/generate', methods=['POST'])
@requires_login
def generate():
    try:

        prompt = escape(request.form.get('prompt'))

        # Initialize an array to hold the contents of each file
        file_contents = []

        # Check if files were uploaded
        files = request.files.getlist('files')
        if files:
            for file in files:
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file:  # If there is a file
                    # Read the content of the file
                    file_content = file.read().decode('utf-8')  # Assuming text files encoded in UTF-8
                    file_contents.append(file_content)

        # Possibly concatenate file contents with the original prompt
        files_text = '\n'.join(file_contents)
        full_prompt = f"{prompt}\n\n{files_text}"  # Adjust as needed

        # Send the concatenated prompt to GPT-4 API
        response = openai_playground.generate_code(full_prompt)

        # Process and return the response as before...

        # This section remains the same
        placeholder = "{TRIPPLETICKS}"

        # Existing code to generate response...
        # Assuming `response` is the variable holding the API's return value

        if isinstance(response, tuple):
            # Log error, handle the tuple, or return an error message
            error_msg = "Error occurred: Missing API key or other issue."
            app.logger.error(error_msg + " Response: %s", str(response))
            return jsonify({"error": error_msg}), 400
        elif isinstance(response, str):
            # Process the response as before
            placeholder = "{TRIPPLETICKS}"
            response_processed = re.sub(r'```', placeholder, response)
            response_processed = response_processed.replace('`', "'")
            response_processed = response_processed.replace(placeholder, "```")
            md_template_string = markdown.markdown(response_processed, extensions=["fenced_code"])
            return jsonify({"prompt": full_prompt, "response": md_template_string})
        else:
            # Handle other types or unexpected structures
            return jsonify({"error": "Unexpected response format"}), 400

    except Exception as e:
        # General exception handling
        app.logger.error("An exception occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500

# response_processed = re.sub(r'```', placeholder, response)
# response_processed = response_processed.replace('`', "'")
# response_processed = response_processed.replace(placeholder, "```")
# md_template_string = markdown.markdown(response_processed, extensions=["fenced_code"])

# return jsonify({"prompt": full_prompt, "response": md_template_string})


@app.route('/prompt', methods=['GET', 'POST'])
@requires_login
def prompt():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        prompt = escape(prompt)
        code = openai_playground.generate_code(prompt)

        # Placeholder for triple backticks
        placeholder = "#TRIPLEBACKTICK#"

        # Process the response
        code = re.sub(r'```', placeholder, code)
        code = code.replace('`', "'")
        code = code.replace(placeholder, "```")

        md_template_string = markdown.markdown(
            code, extensions=["fenced_code"]
        )

        # Pass the conversation history to the template
        htmlString = render_template('prompt.html',
                                     code=md_template_string,
                                     prompt=prompt)
        # conversation_history=conversation_history)

        # Append the new prompt and response to the conversation history
        # conversation_history.append({"prompt": prompt, "response": md_template_string})
        return htmlString

    # Also pass the conversation history when rendering the GET request
    htmlString = render_template('prompt.html',
                                 prompt=openai_playground.prompt)
    # conversation_history=conversation_history)

    return htmlString


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Set the log level you want
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    # debug = os.environ.get("FLASK_DEBUG") == "1"
    # app.run(debug=debug, use_reloader=not (debug and os.environ.get("PYCHARM_DEBUG") == "1"))
    # app.run(debug=True, port=5005)
    app.run(host='0.0.0.0', port=5005)
