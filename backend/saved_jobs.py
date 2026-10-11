from flask import Blueprint, request, jsonify, session

from database import get_db_connection


saved_jobs_bp = Blueprint(
    "saved_jobs",
    __name__,
    url_prefix="/api/saved-jobs"
)


def student_required():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Not authenticated"
        }), 401

    if session.get("user_role") != "student":
        return jsonify({
            "success": False,
            "message": "Student access required"
        }), 403

    return None


# ========================================
# Save Job
# ========================================

@saved_jobs_bp.route("/<int:job_id>", methods=["POST"])
def save_job(job_id):

    auth_error = student_required()

    if auth_error:
        return auth_error

    student_id = session["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed"
        }), 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        # Check whether the job exists
        cursor.execute(
            """
            SELECT id, title, company
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

        # Check whether already saved
        cursor.execute(
            """
            SELECT id
            FROM saved_jobs
            WHERE student_id = %s
              AND job_id = %s
            """,
            (student_id, job_id)
        )

        existing_saved_job = cursor.fetchone()

        if existing_saved_job:
            return jsonify({
                "success": False,
                "message": "Job already saved"
            }), 409

        # Save the job
        cursor.execute(
            """
            INSERT INTO saved_jobs (
                student_id,
                job_id
            )
            VALUES (%s, %s)
            """,
            (
                student_id,
                job_id
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Job saved successfully",
            "saved_job": {
                "id": cursor.lastrowid,
                "job_id": job_id
            }
        }), 201

    except Exception:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to save job"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Get Saved Jobs
# ========================================

@saved_jobs_bp.route("", methods=["GET"])
def get_saved_jobs():

    auth_error = student_required()

    if auth_error:
        return auth_error

    student_id = session["user_id"]

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
                sj.id AS saved_id,
                sj.job_id,
                sj.saved_at,

                j.title,
                j.company,
                j.description,
                j.skills,
                j.location,
                j.job_type,
                j.salary,
                j.experience,
                j.deadline,
                j.status,
                j.created_at

            FROM saved_jobs sj

            INNER JOIN jobs j
                ON sj.job_id = j.id

            WHERE sj.student_id = %s

            ORDER BY sj.saved_at DESC
            """,
            (student_id,)
        )

        saved_jobs = cursor.fetchall()

        return jsonify({
            "success": True,
            "saved_jobs": saved_jobs,
            "count": len(saved_jobs)
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Unable to load saved jobs"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Check Saved Job
# ========================================

@saved_jobs_bp.route(
    "/check/<int:job_id>",
    methods=["GET"]
)
def check_saved_job(job_id):

    auth_error = student_required()

    if auth_error:
        return auth_error

    student_id = session["user_id"]

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
            FROM saved_jobs
            WHERE student_id = %s
              AND job_id = %s
            """,
            (
                student_id,
                job_id
            )
        )

        saved_job = cursor.fetchone()

        return jsonify({
            "success": True,
            "saved": saved_job is not None
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Unable to check saved job"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ========================================
# Remove Saved Job
# ========================================

@saved_jobs_bp.route(
    "/<int:job_id>",
    methods=["DELETE"]
)
def remove_saved_job(job_id):

    auth_error = student_required()

    if auth_error:
        return auth_error

    student_id = session["user_id"]

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
            DELETE FROM saved_jobs
            WHERE student_id = %s
              AND job_id = %s
            """,
            (
                student_id,
                job_id
            )
        )

        deleted_rows = cursor.rowcount

        connection.commit()

        if deleted_rows == 0:
            return jsonify({
                "success": False,
                "message": "Saved job not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Job removed from saved jobs"
        }), 200

    except Exception:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to remove saved job"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()