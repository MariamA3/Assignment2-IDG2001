# Assignment 2 – IDG2001

## Overview
This project aims to develop a simplified version of a Reddit-like forum website using Docker and DockerCompose, hosted on the Chameleon Cloud (OpenStack). The website allows users to interact by creating and browsing posts within different categories, similar to subreddits.

## Features
- **User Authentication and Management:** Users can create accounts, log in, and manage their profiles. User information such as username, email, and password (hashed and salted) are stored securely.
- **Post Creation and Interaction:** Users can create posts within predefined categories. Each post includes essential information such as user, category, text, date, and the number of likes. Additionally, users can interact with posts by liking them.
- **Category-based Feeds:** The website supports category-based feeds, allowing users to browse posts within specific categories or "sub-reddits." Users can view the latest posts in each category and interact with them.
- **User-specific Feeds:** Users can view posts created by specific users by visiting their profile pages. If logged in, users can see detailed information about the user, including the ability to delete their own posts.
- **Cache and Load Balancing:** The system includes a cache module to enhance performance under heavy loads. Additionally, a load balancer distributes incoming traffic among multiple web servers to improve scalability and reliability.
- **Data Persistence:** A relational database system (RDB) is utilized to store user data, post information, and other relevant data. The database is modeled to ensure efficient storage and retrieval of information.

## Technologies Used

- Docker
- DockerCompose
- Python (FastAPI or Flask)
- MySQL or PostgreSQL
- Redis
- Nginx (for load balancing)


## Installation and Setup
1. Clone the repository to your local machine.
2. Install Docker and DockerCompose if not already installed.
3. Set up the Chameleon Cloud (OpenStack) environment as per the project requirements.
4. Modify the DockerCompose file and environment variables as needed.
5. Run `docker-compose up --build` to build and start the containers.



## Testing
1. Ensure all containers are running using `docker ps`.
2. Use the provided test files to run unit tests for the cache and processing layers.
3. Run `pytest`, `flake8 .`, and `mypy .` to check for errors and ensure PEP-8 compliance.

