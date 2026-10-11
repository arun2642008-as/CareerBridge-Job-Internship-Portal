**# CareerBridge — Job \& Internship Portal**



> \*\*Connect. Apply. Grow.\*\*



CareerBridge is a web-based \*\***Job and Internship Portal**\*\* designed to connect students and job seekers with recruiters and companies through a simple, organized, and user-friendly platform.



The platform allows students to discover jobs and internships, search and filter opportunities, save jobs, apply for positions, manage their profiles, and track application statuses.



Recruiters can create and manage job opportunities, view applicants, and update application statuses.



\---



**## 📌 Project Overview**



Finding suitable jobs and internships can be difficult for students and fresh graduates because opportunities are often scattered across multiple platforms.



CareerBridge provides a centralized platform where:



\- Students can discover relevant jobs and internships.

\- Recruiters can publish job opportunities.

\- Students can apply directly through the platform.

\- Recruiters can manage applications.

\- Students can track their application progress.

\- Notifications keep users informed about important updates.



The system uses a \*\*role-based architecture\*\*, providing different functionality for students and recruiters.



\---



**## 🎯 Objectives**



The main objectives of CareerBridge are:



1\. To provide a centralized job and internship discovery platform.

2\. To connect students and job seekers with recruiters.

3\. To simplify the job application process.

4\. To allow recruiters to publish and manage job opportunities.

5\. To provide application tracking for students.

6\. To provide application management for recruiters.

7\. To notify users about important application updates.

8\. To provide a responsive and user-friendly web interface.

9\. To securely manage user authentication and application data.



\---



**# ✨ Key Features**



**## 👨‍🎓 Student / Job Seeker Features**



\- User registration and login

\- Student dashboard

\- Job and internship search

\- Job title and company search

\- Location filtering

\- Job type filtering

\- Job details viewing

\- Online job application

\- Cover letter submission

\- Saved jobs

\- My Applications

\- Application status tracking

\- Student profile management

\- Profile completion tracking

\- Notifications

\- Unread notification count

\- Responsive interface



\---



**## 🏢 Recruiter Features**



\- Recruiter registration and login

\- Recruiter dashboard

\- Create job opportunities

\- Manage posted jobs

\- Edit existing jobs

\- View applicants

\- Review applications

\- Update application status

\- Recruiter notifications

\- Application management



\---



**# 🔄 Application Workflow**



```text

&#x20;                   CareerBridge

&#x20;                        │

&#x20;             ┌──────────┴──────────┐

&#x20;             │                     │

&#x20;         👨‍🎓 Student            🏢 Recruiter

&#x20;             │                     │

&#x20;             │                     │

&#x20;       Register / Login       Register / Login

&#x20;             │                     │

&#x20;             │                     │

&#x20;      Search Jobs            Create Job

&#x20;             │                     │

&#x20;      Filter Jobs            Manage Jobs

&#x20;             │                     │

&#x20;      View Details           View Applicants

&#x20;             │                     │

&#x20;         Apply              Update Status

&#x20;             │                     │

&#x20;             └──────────┬──────────┘

&#x20;                        │

&#x20;                 🔔 Notifications

&#x20;                        │

&#x20;                 Application Tracking



**🛠️ Technology Stack**

Frontend

HTML5

CSS3

JavaScript

Backend

Python

Flask

Flask-Bcrypt

Database

MySQL

Database Connectivity

MySQL Connector/Python

Authentication \& Security

Flask session-based authentication

Password hashing using Flask-Bcrypt / bcrypt

Role-based access control

Development Environment

Visual Studio Code / any code editor

Python

MySQL

Web Browser

Windows PowerShell / Command Prompt



**🏗️ Project Architecture**



CareerBridge-CERSO-Task-5/

│

├── backend/

│   ├── app.py

│   ├── applications.py

│   ├── auth.py

│   ├── config.py

│   ├── database.py

│   ├── jobs.py

│   ├── notifications.py

│   ├── profile.py

│   └── saved\_jobs.py

│

├── frontend/

│   ├── css/

│   ├── js/

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

│

├── screenshots/

│

├── .gitignore

├── requirements.txt

└── README.md



The venv/ directory is used locally for the Python virtual environment and should not be included in source-code repositories or final project archives.



**🗄️ Database Design**



CareerBridge uses a MySQL relational database named:



careerbridge



**The main tables are:**



users

&#x20;  │

&#x20;  ├── student\_profiles

&#x20;  │

&#x20;  ├── jobs

&#x20;  │      │

&#x20;  │      └── applications

&#x20;  │

&#x20;  ├── saved\_jobs

&#x20;  │

&#x20;  └── notifications



**Database Tables**



**1. Users**



Stores authentication and basic account information.



**Important fields:**



id

name

email

password

role

created\_at



**Roles supported:**



student

recruiter



**2. Student Profile**



Stores additional information about students.



**Information includes:**



Phone

Location

Education

Skills

Experience

Bio

Resume

Profile timestamps



**3. Jobs**



Stores job and internship opportunities posted by recruiters.



**Information includes:**



Job title

Company

Description

Skills

Location

Job type

Salary

Experience

Deadline

Status

Recruiter

Creation/update timestamps



**Supported job types include:**



Full Time

Part Time

Internship

Remote



**4. Applications**



Stores student applications for jobs.



Information includes:



Job

Student

Cover letter

Application status

Application date

Last updated date



**Application statuses include:**



Applied

Shortlisted

Interview

Selected

Rejected



A student cannot submit multiple applications for the same job.



**5. Saved Jobs**



Stores jobs saved by students for later viewing.



The system prevents the same student from saving the same job multiple times.



**6. Notifications**



Stores user notifications.



**Notifications include:**



Notification title

Message

Type

Related record

Read/unread status

Creation timestamp



**🔌 REST API Structure**



The backend provides REST-style API endpoints for communication between the frontend and server.



Authentication

POST /api/register

POST /api/login

POST /api/logout

GET  /api/current-user

Jobs



**The job module handles:**



Creating jobs

Viewing jobs

Editing jobs

Managing recruiter jobs

Viewing job details

Applications



**The application module handles:**



Submitting applications

Viewing applications

Managing application statuses

Preventing duplicate applications

Saved Jobs



**The saved jobs module handles:**



Saving jobs

Removing saved jobs

Viewing saved jobs

Student Profile



**The profile module handles:**



Loading profile information

Updating profile information

Profile completion information

Notifications



**The notification module provides:**



GET /api/notifications

PUT /api/notifications/<notification\_id>/read

PUT /api/notifications/read-all



Notifications are generated for important application events.



**For example:**



Student applies for a job

&#x20;       ↓

Recruiter receives notification and



Recruiter changes application status

&#x20;       ↓

Student receives notification



**🔐 Authentication and Security**



CareerBridge uses authentication and role-based access control to protect user information and functionality.



Password Security



Passwords are not stored as plain text.



Password hashing is handled using:



Flask-Bcrypt

bcrypt

Role-Based Access



**The system distinguishes between:**



Student

Recruiter



Each role receives access to the appropriate features.



**For example:**



Students can apply for jobs.

Recruiters can create jobs.

Recruiters can view applicants.

Students can track their applications.



**⚙️ Installation Prerequisites**



Install the following software before running the project:



Python 3.x

MySQL 8.x

Git (optional)

Modern web browser



**1. Clone or Download the Project**



Place the project in a suitable directory.



Example:



C:\\Users\\RC\\Desktop\\CareerBridge-CERSO-Task-5



**2. Create a Virtual Environment**



Open PowerShell or Command Prompt inside the project folder.



python -m venv venv



**3. Activate the Virtual Environment**



Windows PowerShell

venv\\Scripts\\Activate.ps1

Windows Command Prompt

venv\\Scripts\\activate



**4. Install Dependencies**



Run:



pip install -r requirements.txt

🗄️ Database Setup

**1. Open MySQL**



Open MySQL Command Line Client or another MySQL client.



**2. Create the Database**

CREATE DATABASE careerbridge;



Then select it:



USE careerbridge;

**3. Create the Required Tables**



Create the following tables:



users

student\_profiles

jobs

applications

saved\_jobs

notifications



The table definitions should match the database schema used by the backend.



**🔧 Database Configuration**



The backend database configuration is stored in:



backend/config.py



Configure the MySQL connection according to your local environment.



Example configuration structure:



Database Host

Database User

Database Password

Database Name



Never commit real database passwords or other sensitive credentials to a public repository.



**▶️ Running the Application**

**1. Activate the Virtual Environment**

venv\\Scripts\\Activate.ps1



**2. Navigate to Backend**

cd backend

**3. Start Flask**

python app.py



The Flask server will start locally.



Open the URL displayed by Flask in a web browser.



**Example:**



http://127.0.0.1:5000

🧪 Testing



CareerBridge has been tested across its major workflows.



Student Testing



The following functionality has been verified:



Registration

Login

Dashboard

Job search

Company search

Location filtering

Job type filtering

Job details

Job application

Duplicate application prevention

Saved jobs

My Applications

Application status tracking

Student profile

Profile updates

Notifications

Unread notification badge

Recruiter Testing



The following functionality has been verified:



Recruiter registration

Recruiter login

Recruiter dashboard

Job creation

Job management

Job editing

Applicant viewing

Application status management

Recruiter notifications

Notification Testing



The notification system supports:



New application

&#x20;      ↓

Recruiter notification



Application status update

&#x20;      ↓

Student notification



Unread notifications are displayed using a notification badge.



**📱 Responsive Design**



The frontend is designed to work across different screen sizes, including:



Desktop

Laptop

Tablet

Mobile devices



The major pages have been reviewed for layout consistency, spacing, navigation, forms, cards, and responsive behavior.



**🎨 User Interface**



CareerBridge provides separate interfaces for students and recruiters.



**Student Interface** **Includes:**



Dashboard

Job listings

Search and filters

Job details

Applications

Saved jobs

Notifications

Profile



**Recruiter Interface Includes:**



Dashboard

Job management

Job creation

Job editing

Applicant management

Application status updates

Notifications



**📸 Screenshots**



Project screenshots are stored in:



screenshots/



Recommended screenshots include:



Home / Landing Page

Registration

Login

Student Dashboard

Job Details

Job Application

My Applications

Saved Jobs

Student Profile

Notifications

Recruiter Dashboard

Create Job

My Jobs

Applicants



**📊 Major Modules**



**CareerBridge can be divided into the following modules:**



1\. Authentication Module

2\. Student Module

3\. Recruiter Module

4\. Job Management Module

5\. Application Management Module

6\. Saved Jobs Module

7\. Student Profile Module

8\. Notification Module

9\. Database Module

10\. REST API Module



**🌟 Advantages**



**CareerBridge provides several benefits:**



Centralized job and internship discovery

Simple application process

Role-based user experience

Recruiter job management

Application tracking

Saved job functionality

Real-time-style notification workflow

Structured relational database

Secure password handling

Responsive web interface



**🚀 Future Enhancements**



**Possible future improvements include:**



Advanced job recommendation using AI

Resume parsing

AI-powered resume analysis

Skill-based job matching

Email notifications

WhatsApp notifications

Recruiter company profiles

Advanced analytics dashboard

Interview scheduling

Online interview integration

Application statistics

Admin dashboard

Job recommendation based on student skills

Resume builder

Multi-language support



**🧑‍💻 Project Information**



Project Name: CareerBridge



Project Type: Job \& Internship Portal



Purpose: CERSO Project



Tagline:



Connect. Apply. Grow.



Primary Users:



Students / Job Seekers

Recruiters



**Frontend:**



HTML

CSS

JavaScript



**Backend:**



Python

Flask



**Database:**



MySQL



**📂 Important Files**



File / Folder	Purpose

backend/app.py	Main Flask application

backend/auth.py	Authentication functionality

backend/database.py	Database connection

backend/jobs.py	Job management

backend/applications.py	Application management

backend/profile.py	Student profile management

backend/saved\_jobs.py	Saved jobs functionality

backend/notifications.py	Notification functionality

frontend/student-dashboard.html	Student dashboard

frontend/recruiter-dashboard.html	Recruiter dashboard

frontend/job-details.html	Job details

frontend/create-job.html	Create job

frontend/my-applications.html	Student applications

frontend/my-jobs.html	Recruiter jobs

frontend/applicants.html	Applicant management

frontend/student-profile.html	Student profile

frontend/notifications.html	Notifications

requirements.txt	Python dependencies

.gitignore	Files excluded from version control

README.md	Project documentation



**🔄 Complete System Flow**



&#x20;                    ┌─────────────────────┐

&#x20;                    │     CareerBridge    │

&#x20;                    └──────────┬──────────┘

&#x20;                               │

&#x20;                 ┌─────────────┴─────────────┐

&#x20;                 │                           │

&#x20;          ┌──────▼──────┐             ┌──────▼──────┐

&#x20;          │   Student   │             │  Recruiter  │

&#x20;          └──────┬──────┘             └──────┬──────┘

&#x20;                 │                           │

&#x20;            Register/Login              Register/Login

&#x20;                 │                           │

&#x20;                 ▼                           ▼

&#x20;         Student Dashboard          Recruiter Dashboard

&#x20;                 │                           │

&#x20;         Search / Filter Jobs          Create Jobs

&#x20;                 │                           │

&#x20;            View Details              Manage Jobs

&#x20;                 │                           │

&#x20;                Apply                 View Applicants

&#x20;                 │                           │

&#x20;                 └─────────────┬─────────────┘

&#x20;                               │

&#x20;                        Application System

&#x20;                               │

&#x20;                    ┌──────────┴──────────┐

&#x20;                    │                     │

&#x20;                Student              Recruiter

&#x20;                    │                     │

&#x20;             Track Status          Update Status

&#x20;                    │                     │

&#x20;                    └──────────┬──────────┘

&#x20;                               │

&#x20;                        🔔 Notifications



**📄 License**



This project was developed as an academic project for educational and demonstration purposes.



**👨‍💻 Conclusion**



CareerBridge provides a structured platform for connecting students and recruiters through a centralized job and internship management system.



By combining a responsive frontend, Flask backend, MySQL database, REST APIs, authentication, application tracking, saved jobs, and notifications, the system provides a complete foundation for a modern job and internship portal.

