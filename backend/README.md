# This is for the processing layer

#The processing layer is responsible for processing the data from the database and create endpoints that can be used for the frontend

To run the main python file, run the following command:

```bash
cd backend
python main.py
```

hehe

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
