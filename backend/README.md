# This is for the processing layer

#The processing layer is responsible for processing the data from the database and create endpoints that can be used for the frontend

To run the main python file, run the following command:

```bash
cd backend
python main.py
```

## Database connection

To run the database you will need to create a .env file in the backend folder with the following content:

```bash
MYSQLDATABASE=database
MYSQLHOST=host
MYSQLPASSWORD=password
MYSQLPORT=port
MYSQLUSER=user
MYSQL_DATABASE=database
MYSQL_PRIVATE_URL=url
MYSQL_ROOT_PASSWORD=password
MYSQL_URL=url
```

You will find these variables in the railway database under the tab variables copy those into the .env file.
If you have done this the database should connect and the api should work locally.

# API Documentation

## Endpoints

### For the posts table

- GET /posts: Get all posts.
- GET /posts/<id>: Get a specific post by ID.
- POST /posts: Create a new post.
- - Request body: { "title": "string", "content": "string", "user_id": "int", "category_id": "int"}
- PUT /posts/<id>: Update a post by ID.
- - Request body: { "title": "string", "content": "string", "user_id": "int", "category_id": "int"}
- DELETE /posts/<id>: Delete a post by ID.

### For the users table

- GET /users: Get all users.
- GET /users/<id>: Get a specific user by ID.
- POST /users: Create a new user.
- - Request body: { "username": "string", "email": "string" }
- PUT /users/<id>: Update a user by ID.
- - Request body: { "username": "string", "email": "string" }
- DELETE /users/<id>: Delete a user by ID.

### For the categories table

- GET /categories: Get all categories.
- GET /categories/<id>: Get a specific category by ID.
- POST /categories: Create a new category.
- - Request body: { "name": "string" }
- PUT /categories/<id>: Update a category by ID.
- - Request body: { "name": "string"}

### For some ifo

pip3 install Flask Flask-SQLAlchemy Flask-Migrate Flask-JWT-Extended Flask-Bcrypt pymysql python-dotenv email-validator Flask-Cors RedisCache

# Create a new Flask project

flask db init

# This will create a new directory called migrations in your project.

export FLASK_APP=main.py

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
