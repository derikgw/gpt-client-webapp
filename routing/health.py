from flask import Blueprint, jsonify

# Define the blueprint
health_bp = Blueprint('health', __name__)

def init(app, openai_playground):
    @health_bp.route('/health', methods=['GET'])
    def health():
        # Perform any necessary health checks here.
        # For a basic health check, you can simply return a success status.
        return jsonify({'status': 'UP'}), 200

    # Register the blueprint with the app
    app.register_blueprint(health_bp)
