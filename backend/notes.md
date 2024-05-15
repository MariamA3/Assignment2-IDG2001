pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-JWT-Extended Flask-Bcrypt pymysql python-dotenv email-validator

# Step 1: Generate a New Migration Script

# Run whenever you make changes to your SQLAlchemy models.

flask db migrate -m "Description of changes"

# Step 2: Review the Generated Migration Script

# Locate the script in `migrations/versions/` and review it to ensure it correctly represents the intended changes.

# Step 3: Apply the Migration to the Database

# This updates your database schema according to the migration script.

flask db upgrade

# Optional Steps:

# If you need to revert the last applied migration, you can use:

flask db downgrade

# To create a full database backup before applying migrations (recommended), use appropriate database backup commands, e.g., for MySQL:

mysqldump -u username -p database_name > backup.sql

# To restore a database from a backup in case something goes wrong:

mysql -u username -p database_name < backup.sql

# Routes

http://127.0.0.1:4000/categories
http://127.0.0.1:4000/categories/<int:id>
