pip3 install Flask Flask-SQLAlchemy Flask-Migrate Flask-JWT-Extended Flask-Bcrypt pymysql python-dotenv email-validator Flask-Cors RedisCache

# Create a new Flask project

flask db init

# This will create a new directory called migrations in your project.

export FLASK_APP=main.py

# Step 1: Generate a New Migration Script

fuck this shitty ssh shit

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

http://127.0.0.1:4000/categories - GET, POST
http://127.0.0.1:4000/categories/<int:id> - GET, PUT, DELETE

1. Stamp the Database
   If the current schema of the database is already in the state you want and you want to synchronize Alembic's state with the database, you can use the stamp command. This command will set the current revision in the database without performing any migrations:

```bash
   flask db stamp b94c699496ff
```

However, since the revision b94c699496ff does not exist in your migrations/versions directory, you might first need to create a dummy revision just to satisfy the reference, then delete it after stamping. Here’s how to do it:

```bash
flask db revision -m "Dummy for b94c699496ff" --rev-id b94c699496ff
```

Then, you can stamp the database:

```bash
  flask db stamp b94c699496ff
```

      Finally, you can delete the dummy revision:

```bash
rm migrations/versions/b94c699496ff_dummy_for_b94c699496ff.py
```

3. Rebuild from Scratch
   In a development environment where it's feasible, consider starting over:

Drop the Database: Completely drop the database to start afresh.
Create the Database: Recreate the database.
Run Migrations: Start the migrations again

```bash
flask db upgrade
```
