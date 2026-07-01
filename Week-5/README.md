# Student Management System API

## Technologies Used
- Python
- FastAPI
- Uvicorn
- MongoDB
- PyMongo
- Pydantic

## Features
- Add Student
- View All Students
- View Student by ID
- Update Student
- Delete Student

## Run the Project

Install dependencies:

```bash
pip install fastapi uvicorn pymongo pydantic
```

Start the server:

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```