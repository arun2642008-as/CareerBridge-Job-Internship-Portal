import os

from flask import Flask, jsonify, send_from_directory

from config import Config
from database import get_db_connection

from auth import auth_bp
from jobs import jobs_bp
from applications import applications_bp
from profile import profile_bp
from saved_jobs import saved_jobs_bp
from notifications import notifications_bp


app = Flask(__name__)

app.config.from_object(Config)


FRONTEND_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend"
    )
)


# ========================================
# Register API Blueprints
# ========================================

app.register_blueprint(auth_bp)

app.register_blueprint(jobs_bp)

app.register_blueprint(applications_bp)

app.register_blueprint(profile_bp)

app.register_blueprint(saved_jobs_bp)

app.register_blueprint(notifications_bp)


# ========================================
# Frontend
# ========================================

@app.route("/", methods=["GET"])
def home():

    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


@app.route("/<path:filename>", methods=["GET"])
def frontend_files(filename):

    file_path = os.path.join(
        FRONTEND_FOLDER,
        filename
    )

    if os.path.isfile(file_path):

        return send_from_directory(
            FRONTEND_FOLDER,
            filename
        )

    return jsonify({
        "success": False,
        "message": "Frontend page not found"
    }), 404


# ========================================
# Health Check
# ========================================

@app.route("/api/health", methods=["GET"])
def health_check():

    return jsonify({
        "success": True,
        "message": "CareerBridge API is healthy"
    }), 200


# ========================================
# Database Test
# ========================================

@app.route("/api/test-db", methods=["GET"])
def test_database():

    connection = get_db_connection()

    if connection is None:

        return jsonify({
            "success": False,
            "message": (
                "Database connection failed. "
                "Check your MySQL configuration."
            )
        }), 500

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT DATABASE()"
        )

        database_name = cursor.fetchone()[0]

        return jsonify({
            "success": True,
            "message": "Database connection successful",
            "database": database_name
        }), 200

    except Exception:

        app.logger.exception(
            "Database test failed"
        )

        return jsonify({
            "success": False,
            "message": (
                "Unable to verify the "
                "database connection"
            )
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Run Application
# ========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )