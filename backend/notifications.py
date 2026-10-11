from flask import Blueprint, jsonify, session

from database import get_db_connection


notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/api/notifications"
)


def user_required():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Not authenticated"
        }), 401

    return None


# ========================================
# Get Notifications
# ========================================

@notifications_bp.route("", methods=["GET"])
def get_notifications():

    auth_error = user_required()

    if auth_error:
        return auth_error

    user_id = session["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                title,
                message,
                type,
                related_id,
                is_read,
                created_at
            FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        notifications = cursor.fetchall()

        unread_count = sum(
            1
            for notification in notifications
            if not notification["is_read"]
        )

        return jsonify({
            "success": True,
            "notifications": notifications,
            "unread_count": unread_count,
            "count": len(notifications)
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Unable to load notifications"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Get Unread Notification Count
# ========================================

@notifications_bp.route(
    "/unread-count",
    methods=["GET"]
)
def get_unread_count():

    auth_error = user_required()

    if auth_error:
        return auth_error

    user_id = session["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM notifications
            WHERE user_id = %s
              AND is_read = FALSE
            """,
            (user_id,)
        )

        unread_count = cursor.fetchone()[0]

        return jsonify({
            "success": True,
            "unread_count": unread_count
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Unable to get unread count"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Mark One Notification As Read
# ========================================

@notifications_bp.route(
    "/<int:notification_id>/read",
    methods=["PUT"]
)
def mark_notification_read(notification_id):

    auth_error = user_required()

    if auth_error:
        return auth_error

    user_id = session["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE notifications
            SET is_read = TRUE
            WHERE id = %s
              AND user_id = %s
            """,
            (
                notification_id,
                user_id
            )
        )

        updated_rows = cursor.rowcount

        connection.commit()

        if updated_rows == 0:

            return jsonify({
                "success": False,
                "message": "Notification not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Notification marked as read"
        }), 200

    except Exception:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to mark notification as read"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Mark All Notifications As Read
# ========================================

@notifications_bp.route(
    "/read-all",
    methods=["PUT"]
)
def mark_all_notifications_read():

    auth_error = user_required()

    if auth_error:
        return auth_error

    user_id = session["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE notifications
            SET is_read = TRUE
            WHERE user_id = %s
              AND is_read = FALSE
            """,
            (user_id,)
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "All notifications marked as read"
        }), 200

    except Exception:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to mark notifications as read"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()