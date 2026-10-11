from flask import Blueprint, request, jsonify, session

from database import get_db_connection


applications_bp = Blueprint(
    "applications",
    __name__,
    url_prefix="/api/applications"
)


def student_required():
    if "user_id" not in session:
        return False, jsonify({
            "success": False,
            "message": "Authentication required"
        }), 401

    if session.get("user_role") != "student":
        return False, jsonify({
            "success": False,
            "message": "Student access required"
        }), 403

    return True, None, None


def recruiter_required():
    if "user_id" not in session:
        return False, jsonify({
            "success": False,
            "message": "Authentication required"
        }), 401

    if session.get("user_role") != "recruiter":
        return False, jsonify({
            "success": False,
            "message": "Recruiter access required"
        }), 403

    return True, None, None


# ========================================
# Apply For Job
# ========================================

@applications_bp.route("", methods=["POST"])
def apply_for_job():

    allowed, response, status_code = student_required()

    if not allowed:
        return response, status_code

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    job_id = data.get("job_id")
    cover_letter = data.get("cover_letter", "").strip()

    if not job_id:
        return jsonify({
            "success": False,
            "message": "job_id is required"
        }), 400

    student_id = session["user_id"]
    student_name = session.get(
        "user_name",
        "A student"
    )

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        # ----------------------------------------
        # Get Job + Recruiter
        # ----------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                title,
                company,
                deadline,
                status,
                recruiter_id
            FROM jobs
            WHERE id = %s
            """,
            (job_id,)
        )

        job = cursor.fetchone()

        if not job:
            return jsonify({
                "success": False,
                "message": "Job not found"
            }), 404

        if job["status"] != "open":
            return jsonify({
                "success": False,
                "message": (
                    "This job is no longer "
                    "accepting applications"
                )
            }), 400

        # ----------------------------------------
        # Check Existing Application
        # ----------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM applications
            WHERE job_id = %s
              AND student_id = %s
            """,
            (
                job_id,
                student_id
            )
        )

        existing_application = cursor.fetchone()

        if existing_application:
            return jsonify({
                "success": False,
                "message": "You have already applied for this job"
            }), 409

        # ----------------------------------------
        # Create Application
        # ----------------------------------------

        cursor.execute(
            """
            INSERT INTO applications (
                job_id,
                student_id,
                cover_letter
            )
            VALUES (%s, %s, %s)
            """,
            (
                job_id,
                student_id,
                cover_letter or None
            )
        )

        application_id = cursor.lastrowid

        # ----------------------------------------
        # Create Recruiter Notification
        # ----------------------------------------

        notification_title = "New Job Application"

        notification_message = (
            f"{student_name} applied for "
            f"{job['title']}."
        )

        cursor.execute(
            """
            INSERT INTO notifications (
                user_id,
                title,
                message,
                type,
                related_id
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                job["recruiter_id"],
                notification_title,
                notification_message,
                "application",
                application_id
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Application submitted successfully",
            "application_id": application_id
        }), 201

    except Exception:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Failed to submit application"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Get My Applications
# ========================================

@applications_bp.route("/my", methods=["GET"])
def get_my_applications():

    allowed, response, status_code = student_required()

    if not allowed:
        return response, status_code

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
                a.id,
                a.job_id,
                a.cover_letter,
                a.status,
                a.applied_at,
                a.updated_at,
                j.title,
                j.company,
                j.location,
                j.job_type,
                j.salary,
                j.deadline
            FROM applications a
            INNER JOIN jobs j
                ON a.job_id = j.id
            WHERE a.student_id = %s
            ORDER BY a.applied_at DESC
            """,
            (session["user_id"],)
        )

        applications = cursor.fetchall()

        return jsonify({
            "success": True,
            "count": len(applications),
            "applications": applications
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Failed to fetch applications"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Get Single Application
# ========================================

@applications_bp.route(
    "/<int:application_id>",
    methods=["GET"]
)
def get_application(application_id):

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Authentication required"
        }), 401

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        if session.get("user_role") == "student":

            cursor.execute(
                """
                SELECT
                    a.id,
                    a.job_id,
                    a.student_id,
                    a.cover_letter,
                    a.status,
                    a.applied_at,
                    a.updated_at,
                    j.title,
                    j.company,
                    j.location,
                    j.job_type,
                    j.salary,
                    j.deadline
                FROM applications a
                INNER JOIN jobs j
                    ON a.job_id = j.id
                WHERE a.id = %s
                  AND a.student_id = %s
                """,
                (
                    application_id,
                    session["user_id"]
                )
            )

        elif session.get("user_role") == "recruiter":

            cursor.execute(
                """
                SELECT
                    a.id,
                    a.job_id,
                    a.student_id,
                    a.cover_letter,
                    a.status,
                    a.applied_at,
                    a.updated_at,
                    u.name AS student_name,
                    u.email AS student_email,
                    j.title,
                    j.company,
                    j.location,
                    j.job_type,
                    j.salary,
                    j.deadline
                FROM applications a
                INNER JOIN jobs j
                    ON a.job_id = j.id
                INNER JOIN users u
                    ON a.student_id = u.id
                WHERE a.id = %s
                  AND j.recruiter_id = %s
                """,
                (
                    application_id,
                    session["user_id"]
                )
            )

        else:

            return jsonify({
                "success": False,
                "message": "Invalid user role"
            }), 403

        application = cursor.fetchone()

        if not application:

            return jsonify({
                "success": False,
                "message": (
                    "Application not found "
                    "or access denied"
                )
            }), 404

        return jsonify({
            "success": True,
            "application": application
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Failed to fetch application"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Get Applications For Recruiter's Job
# ========================================

@applications_bp.route(
    "/job/<int:job_id>",
    methods=["GET"]
)
def get_job_applications(job_id):

    allowed, response, status_code = recruiter_required()

    if not allowed:
        return response, status_code

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
            SELECT id
            FROM jobs
            WHERE id = %s
              AND recruiter_id = %s
            """,
            (
                job_id,
                session["user_id"]
            )
        )

        job = cursor.fetchone()

        if not job:

            return jsonify({
                "success": False,
                "message": (
                    "Job not found or access denied"
                )
            }), 404

        cursor.execute(
            """
            SELECT
                a.id,
                a.job_id,
                a.student_id,
                a.cover_letter,
                a.status,
                a.applied_at,
                a.updated_at,
                u.name AS student_name,
                u.email AS student_email,
                sp.phone,
                sp.location,
                sp.education,
                sp.skills,
                sp.experience,
                sp.bio,
                sp.resume
            FROM applications a
            INNER JOIN users u
                ON a.student_id = u.id
            LEFT JOIN student_profiles sp
                ON a.student_id = sp.user_id
            WHERE a.job_id = %s
            ORDER BY a.applied_at DESC
            """,
            (job_id,)
        )

        applications = cursor.fetchall()

        return jsonify({
            "success": True,
            "count": len(applications),
            "applications": applications
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Failed to fetch job applications"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Update Application Status
# ========================================

@applications_bp.route(
    "/<int:application_id>/status",
    methods=["PUT"]
)
def update_application_status(application_id):

    allowed, response, status_code = recruiter_required()

    if not allowed:
        return response, status_code

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    new_status = data.get("status", "").strip()

    allowed_statuses = [
        "Applied",
        "Shortlisted",
        "Interview",
        "Selected",
        "Rejected"
    ]

    if new_status not in allowed_statuses:
        return jsonify({
            "success": False,
            "message": "Invalid application status"
        }), 400

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        # ----------------------------------------
        # Get Application + Student + Job
        # ----------------------------------------

        cursor.execute(
            """
            SELECT
                a.id,
                a.student_id,
                a.status AS current_status,
                j.title AS job_title
            FROM applications a
            INNER JOIN jobs j
                ON a.job_id = j.id
            WHERE a.id = %s
              AND j.recruiter_id = %s
            """,
            (
                application_id,
                session["user_id"]
            )
        )

        application = cursor.fetchone()

        if not application:

            return jsonify({
                "success": False,
                "message": (
                    "Application not found "
                    "or access denied"
                )
            }), 404

        # ----------------------------------------
        # Check If Status Actually Changed
        # ----------------------------------------

        old_status = application["current_status"]

        if old_status == new_status:

            return jsonify({
                "success": True,
                "message": "Application status is already set",
                "status": new_status
            }), 200

        # ----------------------------------------
        # Update Application
        # ----------------------------------------

        cursor.execute(
            """
            UPDATE applications
            SET status = %s
            WHERE id = %s
            """,
            (
                new_status,
                application_id
            )
        )

        # ----------------------------------------
        # Create Student Notification
        # ----------------------------------------

        notification_title = (
            f"Application {new_status}"
        )

        notification_message = (
            f"Your application for "
            f"{application['job_title']} "
            f"has been marked as "
            f"{new_status}."
        )

        cursor.execute(
            """
            INSERT INTO notifications (
                user_id,
                title,
                message,
                type,
                related_id
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                application["student_id"],
                notification_title,
                notification_message,
                "application_status",
                application_id
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": (
                "Application status "
                "updated successfully"
            ),
            "status": new_status
        }), 200

    except Exception:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": (
                "Failed to update "
                "application status"
            )
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()