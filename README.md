# GPT-4 Enhanced Flask Application

This Flask application, integrating OpenAI's GPT-4 API, allows for dynamic code snippet generation based on user prompts. It features advanced user authentication, profile management, and an administrative interface for a secure and personalized coding experience.

## Application Features

- **User Roles and Permissions**: Implements a role-based access control system, enabling differentiated access levels and functionalities for regular users and administrators.
- **Dynamic Profile Customization**: Users can edit their profiles, including usernames and emails, ensuring a tailored application experience.
- **Advanced Administrative Interface**: Provides a comprehensive suite of tools for user account management, including detailed user activity insights and the ability to modify user roles.
- **Modular Design for Scalability**: Structured with separate modules for profiles (`profile.py`), admin functions (`admin_panel.py`), and database interactions (`db_utility.py`), facilitating easy maintenance and expansion.

## Technology Stack

### Backend Technologies

- **Python 3.12.1 & Flask**: For backend logic, web server operations, and session management.
- **SQLAlchemy**: For database management, abstracting database interactions and supporting various database systems.

### Frontend Technologies

- **Prism.js with Twilight Theme**: Enhances code snippet readability with advanced syntax highlighting.

## Getting Started

### Initial Setup

Clone the repository and install dependencies to set up your local development environment:

```bash
git clone https://github.com/derikgw/gpt-client-webapp.git
cd gpt-client-webapp
pip install -r requirements.txt
```

### Configuration

1. **Environment Variables**: Securely store your OpenAI API key and Flask's `SECRET_KEY`.
2. **Database Setup**: Initialize the database schema with `python db_utility.py`.

### Running the App

Launch the application and access the web interface at `http://localhost:5005/`.

```bash
python main.py
```

## Application Insights

- **User Engagement**: Register, login, and personalize your profile for a custom experience.
- **Code Snippet Generation**: Use the power of GPT-4 to generate code snippets in various programming languages.
- **Admin Dashboard**: An exclusive area for administrators to manage user accounts and application settings.

## Security Measures

- **Role-Based Access Control**: Ensures users can only access features appropriate to their role.
- **Profile Editing Safeguards**: Validates changes to prevent conflicts and ensure data integrity.
- **Recommended HTTPS Deployment**: For encrypted communication and data protection.

## Advanced Security and Governance

- **Session Governance**: The application enforces user authentication across sessions, ensuring secure access to its features. With the `governance.py` module, it introduces session-based access controls and route protections to maintain a secure environment.
- **Role-Based Access Control (RBAC)**: Through custom decorators, the application restricts access to certain functionalities based on user roles, ensuring that only authorized users can perform sensitive operations.
- **Automated Session Validation**: Before every request, the system verifies user sessions, redirecting unauthenticated users to the login page, thus bolstering security against unauthorized access.

## Community Contributions

We encourage contributions to enhance the application's functionality. Please refer to our contribution guidelines for more details.

## License

This project is licensed under the Apache License 2.0, promoting open and reproducible software development.
