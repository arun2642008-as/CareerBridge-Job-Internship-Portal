from flask import Blueprint, request, jsonify, session
from database import get_db_connection


jobs_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")


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


@jobs_bp.route("", methods=["POST"])
def create_job():
    allowed, response, status_code = recruiter_required()

    if not allowed:
        return response, status_code

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    title = data.get("title", "").strip()
    company = data.get("company", "").strip()
    description = data.get("description", "").strip()
    skills = data.get("skills", "").strip()
    location = data.get("location", "").strip()
    job_type = data.get("job_type", "").strip()
    salary = data.get("salary", "").strip()
    experience = data.get("experience", "").strip()
    deadline = data.get("deadline", "").strip()

    required_fields = {
        "title": title,
        "company": company,
        "description": description,
        "skills": skills,
        "location": location,
        "job_type": job_type,
        "deadline": deadline
    }

    missing_fields = [
        field
        for field, value in required_fields.items()
        if not value
    ]

    if missing_fields:
        return jsonify({
            "success": False,
            "message": "Missing required fields",
            "fields": missing_fields
        }), 400

    allowed_job_types = [
        "Full Time",
        "Part Time",
        "Internship",
        "Remote"
    ]

    if job_type not in allowed_job_types:
        return jsonify({
            "success": False,
            "message": "Invalid job type"
        }), 400

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
            INSERT INTO jobs (
                recruiter_id,
                title,
                company,
                description,
                skills,
                location,
                job_type,
                salary,
                experience,
                deadline
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                session["user_id"],
                title,
                company,
                description,
                skills,
                location,
                job_type,
                salary or None,
                experience or None,
                deadline
            )
        )

        connection.commit()

        job_id = cursor.lastrowid

        return jsonify({
            "success": True,
            "message": "Job created successfully",
            "job_id": job_id
        }), 201

    except Exception:
        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Failed to create job"
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


@jobs_bp.route("", methods=["GET"])
def get_jobs():
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
                recruiter_id,
                title,
                company,
                description,
                skills,
                location,
                job_type,
                salary,
                experience,
                deadline,
                status,
                created_at
            FROM jobs
            WHERE status = 'open'
            ORDER BY created_at DESC
            """
        )

        jobs = cursor.fetchall()

        return jsonify({
            "success": True,
            "count": len(jobs),
            "jobs": jobs
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "Failed to fetch jobs"
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


@jobs_bp.route("/my", methods=["GET"])
def get_my_jobs():
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
            SELECT
                id,
                title,
                company,
                description,
                skills,
                location,
                job_type,
                salary,
                experience,
                deadline,
                status,
                created_at,
                updated_at
            FROM jobs
            WHERE recruiter_id = %s
            ORDER BY created_at DESC
            """,
            (session["user_id"],)
        )

        jobs = cursor.fetchall()

        return jsonify({
            "success": True,
            "count": len(jobs),
            "jobs": jobs
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "Failed to fetch your jobs"
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
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
                recruiter_id,
                title,
                company,
                description,
                skills,
                location,
                job_type,
                salary,
                experience,
                deadline,
                status,
                created_at,
                updated_at
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

        return jsonify({
            "success": True,
            "job": job
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "Failed to fetch job"
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


@jobs_bp.route("/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    allowed, response, status_code = recruiter_required()

    if not allowed:
        return response, status_code

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
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

        cursor.execute(
            """
            SELECT id
            FROM jobs
            WHERE id = %s AND recruiter_id = %s
            """,
            (job_id, session["user_id"])
        )

        job = cursor.fetchone()

        if not job:
            return jsonify({
                "success": False,
                "message": "Job not found or access denied"
            }), 404

        fields = [
            "title",
            "company",
            "description",
            "skills",
            "location",
            "job_type",
            "salary",
            "experience",
            "deadline",
            "status"
        ]

        updates = []
        values = []

        for field in fields:
            if field in data:
                updates.append(f"{field} = %s")
                values.append(data[field])

        if not updates:
            return jsonify({
                "success": False,
                "message": "No fields provided for update"
            }), 400

        if "job_type" in data:
            if data["job_type"] not in [
                "Full Time",
                "Part Time",
                "Internship",
                "Remote"
            ]:
                return jsonify({
                    "success": False,
                    "message": "Invalid job type"
                }), 400

        if "status" in data:
            if data["status"] not in ["open", "closed"]:
                return jsonify({
                    "success": False,
                    "message": "Invalid job status"
                }), 400

        values.append(job_id)
        values.append(session["user_id"])

        query = f"""
            UPDATE jobs
            SET {", ".join(updates)}
            WHERE id = %s AND recruiter_id = %s
        """

        cursor.execute(query, tuple(values))
        connection.commit()

        return jsonify({
            "success": True,
            "message": "Job updated successfully"
        }), 200

    except Exception:
        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Failed to update job"
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


@jobs_bp.route("/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
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
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM jobs
            WHERE id = %s AND recruiter_id = %s
            """,
            (job_id, session["user_id"])
        )

        if cursor.rowcount == 0:
            return jsonify({
                "success": False,
                "message": "Job not found or access denied"
            }), 404

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Job deleted successfully"
        }), 200

    except Exception:
        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Failed to delete job"
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()