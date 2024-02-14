# OpenAI Playground Flask App

This Flask-based web application leverages OpenAI's GPT-4 API to generate code snippets based on user inputs. With an enriched feature set, including user authentication, profile management, and an admin panel, it offers a comprehensive environment for users to interact with AI-generated code in a secure and friendly manner.

## Enhanced Features

- **Profile Management**: Users can update their email addresses and usernames through a dedicated profile page, ensuring a personalized experience.
- **Admin Panel Enhancements**: Administrators have the ability to manage user accounts, including activation, deactivation, and removal, directly from a web interface.
- **Modular Architecture**: Introduction of separate modules (`profile.py`, `admin_panel.py`, `db_utility.py`, `extensions.py`) for better code organization and maintenance.
- **Extended Security Measures**: The application now includes additional security features to safeguard user data and interactions.

## Technical Stack and Requirements

### Python and Flask

- **Python 3.12.1**: Ensures compatibility and leverages the latest language features for optimal performance.
- **Flask Framework**: Utilizes Flask to serve web pages, handle requests, and manage sessions in a lightweight manner.

### Frontend and Syntax Highlighting

- **Prism.js**: Integrates with the Twilight theme to offer enhanced code snippet readability across various programming languages.

### Database and ORM

- **SQLAlchemy**: Employs SQLAlchemy for database interactions, providing an abstraction layer to work with multiple database engines seamlessly.

## Getting Started

### Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/derikgw/gpt-client-webapp.git
cd gpt-client-webapp
pip install -r requirements.txt
```

### Configuration

1. **Environment Variables**: Set your OpenAI API key and Flask's `SECRET_KEY` in your environment or a `.env` file for local development.
2. **Database Initialization**: Run `python db_utility.py` to set up your database schema before starting the application.

### Running the Application

```bash
python main.py
```
Access the web interface at `http://localhost:5005/`.

## Usage Highlights

- **User Registration and Login**: Securely register and authenticate to access and personalize your experience.
- **Code Generation**: Input your prompt and receive AI-generated code snippets in the language of your choice.
- **Admin Dashboard**: Exclusively for administrators to manage the application's user base effectively.

## Security and Best Practices

- **User Authentication**: Leveraging Flask-Login for handling user sessions and access control.
- **Input Validation**: Ensuring all user inputs are sanitized to prevent common web vulnerabilities.
- **HTTPS**: Recommended deployment with HTTPS to encrypt data in transit.

## Contributions and License

- **Contributing**: We welcome contributions! Please see the contribution guidelines for how to get involved.
- **License**: Distributed under the Apache License 2.0. See LICENSE for more information.
