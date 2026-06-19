# Migration Notes

## Folder structure
The application has been refactored into Flask blueprints: `routes/auth`, `routes/admin`, `routes/user`, and `routes/api`. MongoDB access now goes through `database/mongo.py` and the service layer in `services/`.

## Route changes
- `/` redirects by authentication state and role.
- `/login` is the only public login page.
- `/register` is only available until the first admin exists; it creates an admin account.
- `/admin/dashboard`, `/admin/upload`, `/admin/settings`, `/admin/users`, and `/admin/users/create` require admin role.
- `/user/dashboard`, `/user/search`, and `/user/profile` require login.

## MongoDB collections
- `users`: `name`, `email`, `phone`, `password`, `role`, `is_active`, timestamps.
- `documents`: document metadata, physical properties, `file_path`, `status`, creator information.
- `report_types`: report type/sub-report type settings.
- `activity`: recent activity rows for dashboards.

## Password migration
Existing bcrypt byte-string passwords should be reset by an admin because new authentication uses Werkzeug password hashes.

## Environment
Set `SECRET_KEY`, `MONGO_URI`, `MONGO_DB_NAME`, and optionally `UPLOAD_FOLDER` in production.
