from flask import Flask
from config import Config
from flask import Flask, redirect, url_for

# Import blueprints
from routes.auth_routes import auth_bp
from routes.attendance_routes import attendance_bp
from routes.dashboard_routes import dashboard_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Secret key for session
app.secret_key = app.config['SECRET_KEY']

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(dashboard_bp)

# Default route
@app.route("/")
def home():
    return redirect(url_for("auth.login"))

# Run server
if __name__ == "__main__":
    app.run(debug=True)
