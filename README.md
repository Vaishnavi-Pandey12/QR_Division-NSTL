# QR Division Report Management System

## Overview

The **QR Division Report Management System** is a centralized digital report repository developed for **QR Division, NSTL** to manage technical reports, inspection records, investigation documents, defect reports, verification reports, and related institutional documentation in a structured and searchable web application.

The application is designed as a Flask-based central report management platform that supports secure access, role-aware workflows, document metadata capture, searchable report storage, dashboard analytics, and activity tracking. It provides a professional foundation for academic, internship, and government project demonstrations, while remaining extensible for future AI-assisted capabilities such as report summarization, OCR, semantic search, and recommendation systems.

The system uses a **Flask backend**, **MongoDB Atlas database**, **Bootstrap 5 frontend**, **Jinja2 templates**, and **Flask-Login authentication**. Reports can be uploaded with rich metadata, stored in the application upload directory, indexed in MongoDB, searched through advanced filters, and summarized through dashboard statistics and charts.

Key capabilities include:

- Flask backend with Blueprint-based route organization
- MongoDB Atlas persistence for users, documents, report types, and activity logs
- Bootstrap 5 and custom CSS dashboard interface
- Role-based authentication and protected routes
- Report upload and metadata management
- Advanced search and filtering
- Dashboard analytics with Chart.js
- Activity tracking for important system actions
- Service-layer architecture for authentication, users, documents, reports, and logs

---

## Features

### Authentication

- Secure login using email or phone number
- Role Based Access Control for protected pages
- Admin and user dashboards
- First-admin registration flow when no admin exists
- Public registration disabled after the first admin is created
- Password hashing with Werkzeug security utilities
- Flask-Login session management
- Active/inactive user account checks
- CSRF-protected forms through Flask-WTF

### Report Management

- Upload reports through a protected upload page
- Supported file types: PDF, DOCX, XLSX, and PPTX
- File storage under `static/uploads/` through the configured upload folder
- Metadata management for report title, document number, year, division, report type, author, investigation type, client, platform type, and summary
- Technical property capture for geometric and mass properties
- Report categorization using report types
- Pending approval status on newly uploaded documents
- Upload activity logging

### Search System

- Advanced search page
- Filtering by title, document number, author, year, division, report type, investigation type, client, and platform type
- Text search support for report content-related queries
- Pagination support in the document service
- Sorting support for safe sortable fields
- MongoDB indexes for searchable and filterable document fields

### Dashboard

- Professional dashboard layout with sidebar navigation and top navbar
- Statistics cards for total documents, total users, pending approvals, and uploads this month
- Chart.js dashboard visualizations
- Uploads per month chart
- Reports by division chart
- Reports by type chart
- Recent activity table

### Administration

- Admin-only user management
- Create users
- Edit users
- Activate users
- Deactivate users
- Reset user passwords
- Assign roles: `admin`, `manager`, `operator`, and `user`
- Report type management
- Default report type preloading
- Activity log tracking for login, logout, upload, search, user operations, and report type operations

---

## Technology Stack

| Layer          | Technology                |
| -------------- | ------------------------- |
| Backend        | Flask                     |
| Database       | MongoDB Atlas             |
| Frontend       | HTML, CSS, Bootstrap 5    |
| Templates      | Jinja2                    |
| Authentication | Flask-Login               |
| Security       | Werkzeug Password Hashing |
| Charts         | Chart.js                  |

---

## Project Structure

```text
QR_Division-NSTL/
├── app.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── database/
│   ├── __init__.py
│   └── mongo.py
├── models/
│   ├── document.py
│   ├── report_type.py
│   └── user.py
├── routes/
│   ├── admin/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── user/
│       ├── __init__.py
│       └── routes.py
├── services/
│   ├── activity_service.py
│   ├── auth_service.py
│   ├── document_service.py
│   ├── report_service.py
│   └── user_service.py
├── static/
│   ├── dashboard.css
│   ├── js/
│   │   └── dashboard.js
│   └── style.css
├── templates/
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── settings.html
│   │   ├── upload.html
│   │   ├── user_form.html
│   │   └── users.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── layouts/
│   │   └── base.html
│   ├── partials/
│   │   └── dashboard_body.html
│   └── user/
│       ├── dashboard.html
│       ├── profile.html
│       └── search.html
├── utils/
│   ├── __init__.py
│   ├── decorators.py
│   └── helpers.py
├── LICENSE
├── MIGRATION.md
├── README.md
├── package-lock.json
├── package.json
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone <repo-url>
cd QR_Division-NSTL
```

### Create Environment

Using Conda:

```bash
conda create -n flask_env python=3.10
conda activate flask_env
```

Alternatively, using Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file in the project root:

```env
MONGO_URI=<mongodb-atlas-uri>
MONGO_DB_NAME=qr_division_nstl
SECRET_KEY=your_secret_key
```

The application reads configuration values from environment variables through `config/settings.py`. MongoDB Atlas should be reachable from the running environment and the connection string should include valid credentials and database access permissions.

### Run Application

```bash
python app.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000/
```

---

## Database Collections

The system uses MongoDB collections to store users, reports, report categories, and activity logs.

### users

Stores application user accounts and role information.

| Field        | Description                                      |
| ------------ | ------------------------------------------------ |
| `_id`        | MongoDB ObjectId                                 |
| `name`       | Full name of the user                            |
| `email`      | User email address, stored in lowercase          |
| `phone`      | Optional phone number used as an alternate login |
| `password`   | Hashed password generated by Werkzeug            |
| `role`       | User role: `admin`, `manager`, `operator`, `user` |
| `is_active`  | Boolean account status flag                      |
| `created_at` | Account creation timestamp                       |
| `updated_at` | Last update timestamp, when applicable           |

### documents

Stores uploaded report metadata and file references.

| Field                | Description                                      |
| -------------------- | ------------------------------------------------ |
| `_id`                | MongoDB ObjectId                                 |
| `title`              | Report title                                     |
| `document_number`    | Unique or official document/report number        |
| `report_type`        | Report category                                  |
| `division`           | Division associated with the document            |
| `author`             | Report author                                    |
| `author_email`       | Author email address                             |
| `year`               | Report year                                      |
| `investigation_type` | Investigation category or type                   |
| `client`             | Client or requesting organization                |
| `platform_type`      | Platform associated with the report              |
| `summary`            | Short report summary                             |
| `length`             | Geometric property: length                       |
| `breadth`            | Geometric property: breadth                      |
| `draft`              | Geometric property: draft                        |
| `design_speed`       | Geometric property: design speed                 |
| `density`            | Mass property: density                           |
| `displacement`       | Mass property: displacement                      |
| `cb`                 | Mass property: block coefficient                 |
| `cp`                 | Mass property: prismatic coefficient             |
| `file_name`          | Stored file name                                 |
| `file_path`          | Relative file path under static uploads          |
| `uploaded_by`        | User ID of uploader                              |
| `created_by`         | User ID of creator                               |
| `created_by_name`    | Name of creator                                  |
| `status`             | Report workflow status, defaulting to `Pending`  |
| `created_at`         | Upload timestamp                                 |

### report_types

Stores report categories and optional sub-types used for report classification.

| Field        | Description                                 |
| ------------ | ------------------------------------------- |
| `_id`        | MongoDB ObjectId                            |
| `name`       | Report type name                            |
| `sub_type`   | Optional sub-category                       |
| `description`| Optional report type description            |
| `created_at` | Creation timestamp                          |
| `updated_at` | Last update timestamp, when applicable      |

Default report types include:

- Final Acceptance Report
- Issue of Boarding Pass
- Failure Analysis Board
- Inspection Report
- Verification Report
- Defect Report
- Defect Investigation Report

### activity_logs

Stores auditable application activity.

| Field       | Description                                  |
| ----------- | -------------------------------------------- |
| `_id`       | MongoDB ObjectId                             |
| `user`      | User name or system identifier               |
| `action`    | Action performed, such as Login or Upload    |
| `entity`    | Entity affected by the action                |
| `status`    | Activity status, defaulting to `Success`     |
| `timestamp` | Activity timestamp                           |

---

## User Roles

### Admin

Permissions:

- Manage users
- Create users
- Edit users
- Activate and deactivate users
- Reset passwords
- Assign roles
- Upload reports
- Manage report types
- Access admin dashboard
- View recent activity logs
- Access protected administrative modules

### Manager

Permissions:

- Upload reports
- Access protected upload workflows
- Access authenticated dashboard and search pages

### Operator

Permissions:

- Access authenticated dashboard pages
- Search reports
- View profile information

### User

Permissions:

- Search reports
- View dashboard
- View profile information

> Note: Report upload is currently protected by manager-level access, which allows `admin` and `manager` users. If standard users should upload reports, their role can be elevated or the upload route policy can be adjusted.

---

## Authentication Flow

The root route is role aware:

1. A visitor opens `/`.
2. If the visitor is not logged in, the application redirects to `/login`.
3. If the logged-in user has role `admin`, the application redirects to `/admin/dashboard`.
4. All other authenticated users are redirected to `/user/dashboard`.

First-admin registration flow:

1. When no admin exists in MongoDB, `/register` is available.
2. The first registration creates an account with role `admin`.
3. After an admin exists, public registration is disabled.
4. New users must be created by an admin from `/admin/users`.

---

## Dashboard

The dashboard provides a central operational view of the report management system.

Dashboard modules include:

- Statistics cards for total documents, pending approvals, total users, and uploads this month
- Recent activity table showing date, user, action, entity, and status
- Chart.js visualizations for uploads per month, report type distribution, and documents by division
- Navigation sidebar for dashboard, search, upload, approval, AI agent placeholder, analysis modules, and settings
- Top navbar with profile image, username, profile link, settings link, and logout action

---

## Report Upload Workflow

1. Login with an authorized account.
2. Navigate to the upload report page.
3. Enter report metadata such as title, document number, year, division, report type, author, investigation type, client, platform type, and summary.
4. Enter geometric and mass properties when applicable.
5. Attach a supported file: PDF, DOCX, XLSX, or PPTX.
6. Submit the form.
7. The file is stored in the configured upload directory under `static/uploads/`.
8. Report metadata and file path are saved to the MongoDB `documents` collection.
9. A new activity record is written to the `activity_logs` collection.
10. The uploaded document is marked with pending status for future approval workflows.

---

## Routes Overview

### Authentication Routes

| Route       | Purpose                                      |
| ----------- | -------------------------------------------- |
| `/`         | Role-aware entry point                       |
| `/login`   | Login page and login submission              |
| `/register`| First-admin registration, if no admin exists |
| `/logout`  | Logout and session cleanup                   |

### Admin Routes

| Route                                      | Purpose                 |
| ------------------------------------------ | ----------------------- |
| `/admin/dashboard`                         | Admin dashboard         |
| `/admin/users`                             | User management list    |
| `/admin/users/create`                      | Create user             |
| `/admin/users/<user_id>/edit`              | Edit user               |
| `/admin/users/<user_id>/activate`          | Activate user           |
| `/admin/users/<user_id>/deactivate`        | Deactivate user         |
| `/admin/users/<user_id>/reset-password`    | Reset user password     |
| `/admin/upload`                            | Upload report           |
| `/admin/report-types`                      | Report type management  |
| `/admin/report-types/<report_type_id>/edit`| Edit report type        |
| `/admin/report-types/<report_type_id>/delete` | Delete report type  |
| `/admin/settings`                          | Redirects to report type settings |

### User Routes

| Route             | Purpose          |
| ----------------- | ---------------- |
| `/user/dashboard` | User dashboard   |
| `/user/search`    | Advanced search  |
| `/user/profile`   | User profile     |

### API Routes

| Route                   | Purpose                           |
| ----------------------- | --------------------------------- |
| `/api/dashboard/charts` | JSON data for dashboard Chart.js  |

---

## Security Features

- Password hashing using Werkzeug `generate_password_hash()` and `check_password_hash()`
- Flask-Login based session management
- Protected routes for authenticated users
- Role Based Access Control through reusable decorators
- Admin-only user management routes
- Manager-level upload protection
- CSRF protection for forms with Flask-WTF
- HTTP-only session cookies
- SameSite session cookie policy
- Configurable secret key through environment variables
- Account activation and deactivation support
- Public registration disabled after the first admin account exists

---

## Future Enhancements

- AI generated report summaries
- NLP-based report search
- OCR integration for scanned reports
- Semantic search using vector embeddings
- Recommendation engine for related reports
- Expanded analytics dashboard
- Two-factor authentication
- Approval workflow screens
- Document preview and secure download controls
- Fine-grained permissions for manager and operator roles
- Audit log export
- Dataset management for analysis modules
- AI assistant integration for HR Wing and technical report queries

---

## Screenshots

Screenshots can be added to this section after deployment or local execution.

### Login Page

_Add screenshot of the secure login page here._

### Admin Dashboard

_Add screenshot of the admin dashboard with statistics cards and charts here._

### Upload Report

_Add screenshot of the upload report form and drag-and-drop file area here._

### Search Page

_Add screenshot of the advanced search filters and result table here._

### User Management

_Add screenshot of the admin user management table here._

---

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

## Author

Developed as part of the **QR Division Report Management System** project.
