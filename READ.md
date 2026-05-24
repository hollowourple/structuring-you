StructuringYou 

A personal organisation web app built with Flask and MySQL.

-> Features
Login/Signin

Enter username, email and password
Password hashing in the MySQL DB

Tasks Module (complete)

Add, edit, and delete tasks
Star-based priority picker (1–5)
Deadline tracking
Archive completed tasks
Sort by priority and deadline
See task details popup

Dashboard / Overview (complete)

Summary card showing most urgent active task
Total active task count
Date display


Coming Soon

🍽️ Meal Planner
🛒 Groceries (auto-generated from meals)
💰 Finances tracker


🛠️ Tech Stack

Backend: Python, Flask
Database: MySQL (via Flask-MySQLDB)
Frontend: HTML, CSS, JavaScript, Jinja2
Fonts: Cinzel Decorative, IM Fell French Canon
Auth: Session-based with Werkzeug password hashing


-> Running Locally
Prerequisites

Python 3.x
MySQL
pip

Setup
bash# Clone the repo
git clone https://github.com/yourusername/structuring-you.git
cd structuring-you

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
Database Setup
Create a MySQL database named structuring and run the following:
sqlCREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE userTasks (
    taskID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT NOT NULL,
    taskTitle VARCHAR(200) NOT NULL,
    taskDesc VARCHAR(500),
    deadline DATETIME,
    priority INT DEFAULT 1,
    isCompleted BOOLEAN DEFAULT FALSE,
    isArchived BOOLEAN DEFAULT FALSE,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(userID) REFERENCES users(user_id)
);
Config
Edit config.py with your MySQL credentials:
pythonclass Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'your_password'
    MYSQL_DB = 'structuring'
    MYSQL_CURSORCLASS = 'DictCursor'
    MYSQL_AUTOCOMMIT = True
    SECRET_KEY = 'your_secret_key'
Run
bashpython app.py
Visit http://127.0.0.1:5000

📁 Project Structure
structuring-you/
├── app.py
├── config.py
├── requirements.txt
├── templates/
│   ├── userlogin.html
│   ├── signup.html
│   ├── dashboard.html
│   └── tasks.html

