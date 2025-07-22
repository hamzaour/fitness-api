# Fitness API

A simple FastAPI project for managing users and workouts, built with SQLAlchemy, SQLite, and modern authentication best practices.  
This project demonstrates user registration (with hashed passwords), login, and full CRUD operations for workouts.

---

## Features

- User registration with password hashing (bcrypt)
- User authentication (login)
- Full CRUD API for workouts
- SQLAlchemy ORM with SQLite database
- Pydantic data validation
- Modular project structure with routers

---

## Getting Started

### 1. **Clone the repo**

```bash
git clone https://github.com/YOUR-USERNAME/fitness-api.git
cd fitness-api´´´


## 2. Install requirements

> Requires Python 3.11+

bash
pip install -r requirements.txt

## 3. Run the server
bash
Copy
Edit
uvicorn main:app --reload

## 4. Explore the API
Open your browser at http://127.0.0.1:8000/docs for the interactive Swagger UI.

## Project Structure
css
Copy
Edit
APIs/
  main.py
  database.py
  models.py
  routers/
    auth.py
    workouts.py



