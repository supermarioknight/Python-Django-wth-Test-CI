# School Schedule API
A Django REST Framework API for managing school schedules, including classes, teachers, subjects, students, and schedules. It uses PostgreSQL as the database and is containerized using Docker and Docker Compose.

## Project Overview
The School Schedule API is a backend application built with Django and Django REST Framework (DRF) that allows users to:

Manage teachers, subjects, classes, students, and schedules.
Retrieve schedules with filtering options.
Handle high traffic loads with performance optimizations.
Run tests to ensure the correctness of the application.
Deploy easily using Docker and Docker Compose.

## Features
- RESTful API: Provides endpoints for accessing and managing school schedules.
- Filtering and Ordering: Supports filtering schedules by date and class, and orders results by day and hour.
- Performance Optimizations:
    - Database indexing for faster queries.
    - Query optimizations using select_related.
- Testing: Includes unit tests for models and API endpoints.
- Dockerized: Easy setup and deployment using Docker and Docker Compose.
- Continuous Integration: Configured with GitHub Actions for automated testing.

## Prerequisites
- Docker and Docker Compose installed on system.
- Python 3.9 or higher (if running without Docker).
- PostgreSQL (if running without Docker).
- Git (for cloning the repository).

## Installation

1. Clone the Repository
    ```
    git clone https://github.com/supermarioknight/school_schedule.git
    cd school_schedule
    ```

2. Create and Activate a Virtual Environment (Optional)
    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```

3. Set Up Environment Variables
    Create a `.env` file in the project root with the following content:
    

    ```
    # .env

    SECRET_KEY='secret-key'  # Replace with a secure, randomly generated key
    DEBUG=True
    ALLOWED_HOSTS=*

    # Database configuration
    POSTGRES_DB=school_schedule_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=db  # Use 'localhost' if not using Docker
    POSTGRES_PORT=5432
    ```

## Running the Application

### Using Docker and Docker Compose

1. Build and Run the Docker Containers:
    ```
    docker-compose up --build
    ```
2. Apply Migrations:
    ```
    docker-compose exec web python manage.py migrate
    ```
3. Create a Superuser (Optional):
    ```
    docker-compose exec web python manage.py createsuperuser
    ```
4. Access the Application:
    - The application will be accessible at http://localhost:8000/.

### Without Docker
1. Run Database Migrations:
    ```
    python manage.py migrate
    ```
2. Create a Superuser (Optional):
    ```
    python manage.py createsuperuser
    ```
3. Run the Development Server:
    ```
    python manage.py runserver
    ```

## Running Tests

To run the tests, execute:

```
# Using Docker
docker-compose exec web python manage.py test

# Without Docker
python manage.py test
```

## API Endpoints

### Admin URL
```
http://localhost:8000/admin/
```

### Base URL
```
http://localhost:8000/api/
```

### Endpoints
- Get All Schedules
    ```
    GET /api/schedule/
    ```
- Get Schedules for Today
    ```
    GET /api/schedule/?for_today=true
    ```
- Get Schedules for a Specific Class
    ```
    GET /api/schedule/?class_name=ClassName
    ```
- Get Schedules for Today and a Specific Class
    ```
    GET /api/schedule/?for_today=true&class_name=ClassName
    ```

    #### Request Parameters
    - for_today: Set to 'true' to filter schedules for the current day.
    - class_name: Filter schedules by class name.

    #### Response Format
    Example Response
    ```
    [
        {
            "class_assigned": {
                "name": "5A",
                "student_count": 25
            },
            "subject": {
                "name": "Math"
            },
            "day_of_week": "Monday",
            "hour": "09:00:00",
            "teacher": {
                "name": "Alex"
            }
        },
        {
            "class_assigned": {
                "name": "5A",
                "student_count": 25
            },
            "subject": {
            "name": "English",
            },
            "day_of_week": "Monday",
            "hour": "10:00:00",
            "teacher": {
                "name": "Alex"
            }
        }
    ]
    ```


## Potential Improvements

- Advanced Caching: Implement Redis or Memcached for more efficient caching strategies to handle high traffic loads.
- Asynchronous Processing: Use asynchronous views and an ASGI server like Uvicorn for better concurrency.
- Search Functionality: Integrate full-text search capabilities using tools like Elasticsearch.
- Rate Limiting and Throttling: Implement rate limiting to prevent abuse and manage load effectively.
- Monitoring and Logging: Integrate monitoring tools like Sentry for error tracking and set up structured logging.
- Continuous Deployment: Extend CI/CD pipelines to include automated deployments to staging or production environments.
- Environment-Specific Settings: Separate settings for development, staging, and production environments.