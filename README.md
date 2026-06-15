# QR_Division-NSTL

AI-Based Central Report Management System (Intern)

## Overview

This is a Flask web application for user authentication and a dashboard interface. It includes:

- User registration with name, email, phone, and password
- User login using email or phone number
- Password reset via the "Forgot Password" page
- Protected dashboard access after login
- Dashboard UI with sidebar items for reports, search, upload, approval, and AI agent features

## Built Features

- `app.py`:
  - Flask routes for `/`, `/login`, `/register`, `/dashboard`, `/logout`, and `/forgot-password`
  - MongoDB-backed user storage using `pymongo`
  - Password hashing with `bcrypt`
  - Session-based login state management
- Templates in `templates/` for:
  - `index.html`: home page with user/admin login options
  - `login.html`: user login form
  - `register.html`: user registration form
  - `dashboard.html`: protected dashboard with placeholder panels
  - `forgot_password.html`: reset password form
- Styling in `static/` using Bootstrap and custom CSS

## Requirements

- Python 3.x
- Flask
- PyMongo
- bcrypt
- MongoDB Atlas or local MongoDB instance

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd QR_Division-NSTL
   ```

2. Install Python dependencies:

   ```bash
   pip install flask pymongo bcrypt
   ```

3. Update the MongoDB connection string in `app.py` if needed.

## Run the App

```bash
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

## Notes

- The current app stores credentials and database connection details directly in `app.py`; these should be moved to environment variables for production.
- The dashboard UI is currently a placeholder layout with sections for document upload and portal navigation.
- The admin login link on the home page is present in UI but does not have a corresponding Flask route yet.

## Project Structure

- `app.py` - Flask application logic
- `templates/` - HTML templates
- `static/` - CSS and static assets
- `package.json` - Node dependency metadata (currently contains `mongodb` package)
