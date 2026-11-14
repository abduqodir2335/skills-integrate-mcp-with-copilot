# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for the GitHub Skills activity
- Sign up for activities
- Teacher login required to register or unregister students

## Getting Started

1. From the repository root, install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. From the repository root, run the application:

   ```
   uvicorn src.app:app --reload
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

4. Configure teacher accounts in `src/teachers.json` by running this command
   from the repository root:

   ```python
   python src/create_teacher.py
   ```

   The command prompts for a username and password (without displaying the
   password) and stores only a salted PBKDF2-HMAC-SHA256 hash. Keep the
   credentials file private. Set `SESSION_SECRET` to a stable, private random
   value before deployment and `COOKIE_SECURE=true` when serving over HTTPS.

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/auth/status`                                                    | Check whether the current browser is logged in as a teacher          |
| POST   | `/auth/login`                                                      | Log in with a teacher username and password                          |
| POST   | `/auth/logout`                                                     | Log out the current teacher                                          |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Register a student (teacher login required)                         |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher login required)                    |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
