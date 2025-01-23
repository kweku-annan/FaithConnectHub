# FaithConnectHub Project Structure

This document provides an overview of the project structure for FaithConnectHub and explains the purpose of each folder and file.

## Project Structure

```
/faithconnecthub
|-- /app
|   |-- /models
|   |-- /routes
|   |-- /services
|   |-- /schemas
|   |-- /utils
|-- /tests
|-- config.py
|-- main.py
|-- requirements.txt
|-- README.md
```

## Folder and File Explanations

### `/app` - Main Application Code
Contains core parts of the application.

- **`/models`** - Defines database models using SQLAlchemy (e.g., `user.py`, `event.py`).
- **`/routes`** - Handles API routes (e.g., `user_routes.py`, `event_routes.py`).
- **`/services`** - Contains business logic separate from routes (e.g., `user_service.py`).
- **`/schemas`** - Data validation and serialization (e.g., `user_schema.py`).
- **`/utils`** - Utility/helper functions (e.g., `token_utils.py`).

### `/tests` - Testing Code
Contains unit and integration tests.

- Example test files: `test_user.py`, `test_event.py`

### `config.py` - Configuration Settings
Contains app configuration, such as database connection and security settings.

Example content:
```python
import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://user:password@localhost/faithconnecthub')
    DEBUG = True
```

### `main.py` - Application Entry Point
Initializes and starts the Flask application.

Example content:
```python
from flask import Flask
from app.routes.user_routes import user_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(user_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True)
```

### `requirements.txt` - Dependencies
Lists required Python packages.

Example content:
```
Flask==2.1.1
SQLAlchemy==1.4.41
Flask-RESTful==0.3.9
Flask-JWT-Extended==4.4.3
mysqlclient==2.1.1
pytest==7.1.2
```

### `README.md` - Documentation
Provides an overview of the project and how to set it up.

Example content:
```
# FaithConnectHub

A Church Management System built with Flask.

## Installation

1. Clone the repo: `git clone https://github.com/yourrepo/faithconnecthub.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
```

This README should help you navigate the project structure effectively.

