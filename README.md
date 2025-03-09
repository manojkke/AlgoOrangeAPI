# Student CRUD Application

This is a simple CRUD (Create, Read, Update, Delete) application for managing student records using FastAPI and SQLAlchemy.

## Project Structure

```
student-crud-app
├── app
│   ├── main.py               # Entry point of the application
│   ├── crud
│   │   └── student.py        # CRUD operations for students
│   ├── models
│   │   └── student.py        # SQLAlchemy model for Student
│   ├── routers
│   │   └── student.py        # API endpoints for student operations
│   ├── schemas
│   │   └── student.py        # Pydantic schemas for data validation
│   └── database.py           # Database connection and session management
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd student-crud-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage

- **Create a Student:**
  - Endpoint: `POST /students`
  - Request Body: `{"name": "John Doe", "age": 20, "grade": "A"}`

- **Get a Student:**
  - Endpoint: `GET /students/{student_id}`

- **Update a Student:**
  - Endpoint: `PUT /students/{student_id}`
  - Request Body: `{"name": "John Doe", "age": 21, "grade": "A+"}`

- **Delete a Student:**
  - Endpoint: `DELETE /students/{student_id}`

## License

This project is licensed under the MIT License.