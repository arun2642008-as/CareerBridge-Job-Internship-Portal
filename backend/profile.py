from flask import Blueprint, request, jsonify, session

from database import get_db_connection


profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/api/profile"
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


def calculate_profile_completion(profile):

    fields = [
        "phone",
        "location",
        "education",
        "skills",
        "experience",
        "bio",
        "resume"
    ]

    completed = 0

    for field in fields:

        value = profile.get(field)

        if value is not None and str(value).strip():
            completed += 1

    percentage = round(
        (completed / len(fields)) * 100
    )

    return percentage


@profile_bp.route("", methods=["GET"])
def get_profile():

    auth_error = student_required()

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
                u.id,
                u.name,
                u.email,
                u.role,
                p.phone,
                p.location,
                p.education,
                p.skills,
                p.experience,
                p.bio,
                p.resume,
                p.created_at,
                p.updated_at
            FROM users u
            LEFT JOIN student_profiles p
                ON u.id = p.user_id
            WHERE u.id = %s
              AND u.role = 'student'
            """,
            (user_id,)
        )

        profile = cursor.fetchone()

        if not profile:
            return jsonify({
                "success": False,
                "message": "Student profile not found"
            }), 404

        profile_completion = calculate_profile_completion(
            profile
        )

        return jsonify({
            "success": True,
            "profile": {
                "id": profile["id"],
                "name": profile["name"],
                "email": profile["email"],
                "role": profile["role"],
                "phone": profile["phone"] or "",
                "location": profile["location"] or "",
                "education": profile["education"] or "",
                "skills": profile["skills"] or "",
                "experience": profile["experience"] or "",
                "bio": profile["bio"] or "",
                "resume": profile["resume"] or "",
                "profile_completion": profile_completion
            }
        }), 200

    except Exception:

        return jsonify({
            "success": False,
            "message": "Unable to load profile"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()


@profile_bp.route("", methods=["PUT"])
def update_profile():

    auth_error = student_required()

    if auth_error:
        return auth_error

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    phone = data.get("phone", "").strip()
    location = data.get("location", "").strip()
    education = data.get("education", "").strip()
    skills = data.get("skills", "").strip()
    experience = data.get("experience", "").strip()
    bio = data.get("bio", "").strip()
    resume = data.get("resume", "").strip()

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
            SELECT id
            FROM student_profiles
            WHERE user_id = %s
            """,
            (user_id,)
        )

        existing_profile = cursor.fetchone()

        if existing_profile:

            cursor.execute(
                """
                UPDATE student_profiles
                SET
                    phone = %s,
                    location = %s,
                    education = %s,
                    skills = %s,
                    experience = %s,
                    bio = %s,
                    resume = %s
                WHERE user_id = %s
                """,
                (
                    phone,
                    location,
                    education,
                    skills,
                    experience,
                    bio,
                    resume,
                    user_id
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO student_profiles (
                    user_id,
                    phone,
                    location,
                    education,
                    skills,
                    experience,
                    bio,
                    resume
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    phone,
                    location,
                    education,
                    skills,
                    experience,
                    bio,
                    resume
                )
            )

        connection.commit()

        cursor.execute(
            """
            SELECT
                u.id,
                u.name,
                u.email,
                u.role,
                p.phone,
                p.location,
                p.education,
                p.skills,
                p.experience,
                p.bio,
                p.resume
            FROM users u
            LEFT JOIN student_profiles p
                ON u.id = p.user_id
            WHERE u.id = %s
              AND u.role = 'student'
            """,
            (user_id,)
        )

        profile = cursor.fetchone()

        profile_completion = calculate_profile_completion(
            profile
        )

        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "profile": {
                "id": profile["id"],
                "name": profile["name"],
                "email": profile["email"],
                "role": profile["role"],
                "phone": profile["phone"] or "",
                "location": profile["location"] or "",
                "education": profile["education"] or "",
                "skills": profile["skills"] or "",
                "experience": profile["experience"] or "",
                "bio": profile["bio"] or "",
                "resume": profile["resume"] or "",
                "profile_completion": profile_completion
            }
        }), 200

    except Exception:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to update profile"
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection.is_connected():
            connection.close()