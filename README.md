CareerBridge — Job & Internship Portal

Connect. Apply. Grow.

CareerBridge is a full-stack job and internship portal built to help students and job seekers discover opportunities and help recruiters manage job listings and applications.

Students can search and filter opportunities, view job details, save jobs, apply with a cover letter, manage their profiles, and track application statuses. Recruiters can publish and manage opportunities, review applicants, and update application statuses.

Project status: Source code is available on GitHub. The application currently uses a local Flask backend and MySQL database; a public deployment is a separate step.

Table of Contents

Features

Screenshots

Technology Stack

Project Structure

How It Works

Database

Getting Started

Environment Variables

Running the Application

API Overview

Security Notes

Testing

Future Improvements

Project Information

Features

Student / Job Seeker

Register and log in.

View a student dashboard.

Browse jobs and internships.

Search by job title or company.

Filter opportunities by location and job type.

View job details.

Apply for opportunities with a cover letter.

Save jobs and view saved opportunities.

View applications and track their status.

Manage profile information and profile completion.

Receive notifications and view unread notification counts.

Recruiter

Register and log in as a recruiter.

View the recruiter dashboard.

Create, edit, and manage job listings.

View applicants and review applications.

Update application statuses.

Receive notifications related to application activity.

Application workflow

A student or recruiter registers and signs in.

Recruiters create job listings.

Students search for opportunities and view job details.

Students submit applications.

Recruiters review applications and update their statuses.

Notifications help keep the relevant users informed.

Screenshots

The screenshots below show selected screens from the project. Open any image to view it at full size.

Home page



Registration



Login



Student dashboard



Job search and filters



Job details



Saved jobs



Recruiter dashboard



Create or edit a job



Notifications



Technology Stack

Area

Technologies

Frontend

HTML5, CSS3, JavaScript

Backend

Python, Flask

Database

MySQL

Database connectivity

MySQL Connector/Python

Password hashing

Werkzeug password hashing

Authentication

Flask sessions and role-based access checks

Development tools

Git, a code editor, browser, Windows Command Prompt or PowerShell

The dependencies used by the application are listed in requirements.txt.

Project Structure

CareerBridge-CERSO-Task-5/
├── backend/
│   ├── app.py
│   ├── applications.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── jobs.py
│   ├── notifications.py
│   ├── profile.py
│   └── saved_jobs.py
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   ├── applicants.html
│   ├── create-job.html
│   ├── edit-job.html
│   ├── index.html
│   ├── job-details.html
│   ├── login.html
│   ├── my-applications.html
│   ├── my-jobs.html
│   ├── notifications.html
│   ├── recruiter-dashboard.html
│   ├── register.html
│   ├── saved-jobs.html
│   ├── student-dashboard.html
│   └── student-profile.html
├── screenshots/
├── .gitignore
├── requirements.txt
└── README.md

A Python virtual environment (venv/) is created locally during setup and is intentionally not committed to Git.

How It Works

CareerBridge separates student and recruiter experiences. The Flask backend handles requests and application logic, while the frontend uses HTML, CSS, and JavaScript to display pages and interact with the API. MySQL stores account and application data.

Main modules

Module

Responsibility

backend/app.py

Flask application setup and page/API registration

backend/auth.py

Registration, login, logout, and current-user authentication

backend/database.py

MySQL connection handling

backend/jobs.py

Job listing and job management functionality

backend/applications.py

Job application workflows and application status management

backend/saved_jobs.py

Saving, removing, and listing saved jobs

backend/profile.py

Student profile operations

backend/notifications.py

Notification operations

Database

The application expects a MySQL database named careerbridge.

The database contains these main tables:

users — account details, roles, and password hashes.

student_profiles — additional student profile information.

jobs — job and internship listings.

applications — applications submitted by students.

saved_jobs — jobs saved by students.

notifications — notifications for users.

The tables and columns in your MySQL database must match the SQL queries used by the backend. This repository does not currently include a database export or schema.sql file, so you must create/import the matching schema from your existing project database before running the application on a fresh installation.

Do not export real user records or passwords when creating a schema-only backup.

Getting Started

Prerequisites

Install the following:

Python 3.x

MySQL 8.x (or a compatible MySQL server)

Git (optional, for cloning)

A modern web browser

1. Clone the repository

git clone https://github.com/arun2642008-as/CareerBridge-Job-Internship-Portal.git
cd CareerBridge-Job-Internship-Portal

Alternatively, download the repository as a ZIP file from GitHub and extract it.

2. Create and activate a virtual environment

Windows Command Prompt:

python -m venv venv
venv\Scripts\activate

Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1

If PowerShell blocks activation, use Command Prompt or follow Microsoft's guidance for your local PowerShell execution policy. Do not change system-wide security settings just to activate the environment.

3. Install Python dependencies

Run this command from the project root:

python -m pip install -r requirements.txt

4. Prepare MySQL

Start your MySQL server and create the database:

CREATE DATABASE careerbridge;

Then create or import the six required tables listed in the Database section. The schema must match the backend's expected columns and relationships. A fresh database with only CREATE DATABASE will not be sufficient to run the application.

5. Configure environment variables

The backend reads its secret key and database connection settings from environment variables. See Environment Variables for the names and examples.

6. Start the backend

From the project root, activate the virtual environment and configure the environment variables. Then run:

cd backend
python app.py

If startup succeeds, open the local address printed by Flask. The default development address used by this project is:

http://127.0.0.1:5000

This is a local development address, not a public website.

Environment Variables

Configure these variables in your local terminal before starting the backend. Use your own local MySQL credentials; never put real credentials in this README or commit them to Git.

Variable

Purpose

Example

SECRET_KEY

Secret used by Flask sessions

A long, random, private value

MYSQL_HOST

MySQL server hostname

localhost

MYSQL_USER

MySQL username

root

MYSQL_PASSWORD

MySQL password

Your local MySQL password

MYSQL_DATABASE

Database name

careerbridge

Windows Command Prompt example

Generate a strong, random secret key privately, then set the variables in the same CMD window before running the app:

set SECRET_KEY=replace_with_a_long_random_secret
set MYSQL_HOST=localhost
set MYSQL_USER=root
set MYSQL_PASSWORD=replace_with_your_local_mysql_password
set MYSQL_DATABASE=careerbridge
cd backend
python app.py

Replace the example values on your computer. These commands set variables only for the current Command Prompt session. Do not commit a file containing real secret values.

Windows PowerShell example

$env:SECRET_KEY = "replace_with_a_long_random_secret"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "replace_with_your_local_mysql_password"
$env:MYSQL_DATABASE = "careerbridge"
Set-Location backend
python app.py

If SECRET_KEY is not set, the current backend configuration is expected to stop startup with an error. This is intentional: use a private secret rather than a hard-coded fallback.

API Overview

The frontend communicates with Flask through HTTP API routes. The authentication routes currently use the /api/auth/ prefix:

Method

Endpoint

Purpose

POST

/api/auth/register

Register a user

POST

/api/auth/login

Sign in

POST

/api/auth/logout

Sign out

GET

/api/auth/me

Retrieve the current user's session information

GET

/api/health

Check backend health

GET

/api/test-db

Test database connectivity

Other modules provide job, application, saved-job, profile, and notification functionality. Refer to the route definitions in backend/jobs.py, backend/applications.py, backend/saved_jobs.py, backend/profile.py, and backend/notifications.py for the exact methods, paths, and request formats.

Security Notes

Passwords should be stored as hashes, not plain text.

The application uses Flask sessions and role-based access checks.

Keep SECRET_KEY private and use a strong, randomly generated value.

Keep database credentials out of source code and public commits.

Do not use real student, recruiter, or application data in public screenshots or sample database exports.

Before a public production deployment, review session-cookie settings, input validation, authorization checks, CSRF protection where applicable, error handling, database permissions, and HTTPS.

Do not run Flask's development server or enable debug mode for a public production deployment. Use a production WSGI server and configure secrets through the hosting provider's environment settings.

Testing

The project README and development workflow cover testing of the main student and recruiter journeys, including:

Registration and login.

Student and recruiter dashboards.

Job search and filtering.

Job details and applications.

Duplicate application prevention.

Saved jobs and application tracking.

Student profile updates.

Job creation and editing.

Recruiter applicant review and application status updates.

Notifications and unread notification indicators.

Test the workflows again after making configuration changes or deploying to a new environment. Results may vary depending on database contents and configuration.

Future Improvements

Possible enhancements include:

A documented, version-controlled database schema and migration workflow.

Automated tests for API routes and authentication.

Production deployment with a hosted MySQL database.

Improved logging and monitoring.

Email notifications.

AI-assisted job recommendations and skill-based matching.

Resume parsing and resume feedback.

Interview scheduling.

Recruiter company profiles and analytics.

An admin dashboard.

Multi-language support.

These are potential future enhancements and should not be considered implemented features unless they are added to the application.

Project Information

Project name: CareerBridge

Project type: Job and Internship Portal

Project purpose: Academic and portfolio project

Primary users: Students/job seekers and recruiters

Tagline: Connect. Apply. Grow.

Repository: CareerBridge-Job-Internship-Portal

License

No open-source license has been added to this repository yet. Unless you add a license, other people generally do not receive explicit permission to reuse, distribute, or modify the code. Add a license file if you want to grant those permissions.

Conclusion

CareerBridge brings job discovery, applications, recruiter job management, profile management, and notifications into one application. It combines a browser-based frontend, a Flask backend, and a MySQL database to provide a foundation for a job and internship portal.

Contributions and suggestions are welcome through GitHub issues.
