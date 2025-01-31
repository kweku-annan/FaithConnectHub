
# FaithConnectHub

FaithConnectHub is a Church Management System built with Flask. It provides functionalities for user registration, authentication, and role-based access control (RBAC) for managing church members.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourrepo/faithconnecthub.git
    cd faithconnecthub
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    - Ensure you have MySQL installed and running.
    - Create a database for the project.
    - Update the `.env` file with your database credentials.

5. **Run the application:**
    ```sh
    python main.py
    ```

## Configuration

Create a `.env` file in the root directory and add the following environment variables:
```dotenv
FaithConnectHub_USER="your_db_user"
FaithConnectHub_PWD="your_db_password"
FaithConnectHub_HOST="localhost"
FaithConnectHub_DB="your_db_name"
FaithConnectHub_ENV="dev"

# Flask Config
SECRET_KEY="your_secret_key"
JWT_SECRET_KEY="your_jwt_secret_key"
```

## Usage

To start the Flask application, run:
```sh
python main.py
```

## API Endpoints

### Authentication

#### Register a new user
**Endpoint:** `POST /register`

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "MEMBER"
}
```

**Response:**
```json
{
  "Message": "Registered Successfully! Here are your details:",
  "username": "john_doe",
  "email": "john@example.com",
  "role": "MEMBER"
}
```

#### Login a user
**Endpoint:** `POST /login`

**Request:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "your_jwt_token"
}
```

### Members

#### Retrieve all members (Admin & Pastor only)
**Endpoint:** `GET /members`

**Request Header:**
```
Authorization: Bearer your_jwt_token
```

**Response:**
```json
[
  {
    "id": "1",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "MEMBER"
  },
  {
    "id": "2",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "role": "PASTOR"
  }
]
```

#### Create a new member (Admin & Pastor only)
**Endpoint:** `POST /members`

**Request Header:**
```
Authorization: Bearer your_jwt_token
```

**Request:**
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "MEMBER"
}
```

**Response:**
```json
{
  "id": "3",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "MEMBER"
}
```

#### View a member's profile (Member, Admin & Pastor)
**Endpoint:** `GET /members/<member_id>`

**Request Header:**
```
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
  "id": "1",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "MEMBER"
}
```

#### Update a member's profile (Member, Admin & Pastor)
**Endpoint:** `PUT /members/<member_id>`

**Request Header:**
```
Authorization: Bearer your_jwt_token
```

**Request:**
```json
{
  "name": "Johnathan Doe"
}
```

**Response:**
```json
{
  "id": "1",
  "name": "Johnathan Doe",
  "email": "john@example.com",
  "role": "MEMBER"
}
```

#### Delete a member's profile (Member, Admin & Pastor)
**Endpoint:** `DELETE /members/<member_id>`

**Request Header:**
```
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
  "message": "Member deleted successfully"
}
```

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

### `/app` - Main Application Code
Contains core parts of the application.

- **`/models`** - Defines database models using SQLAlchemy.
- **`/routes`** - Handles API routes.
- **`/services`** - Contains business logic separate from routes.
- **`/schemas`** - Data validation and serialization.
- **`/utils`** - Utility/helper functions.

### `/tests` - Testing Code
Contains unit and integration tests.

### `config.py` - Configuration Settings
Contains app configuration, such as database connection and security settings.

### `main.py` - Application Entry Point
Initializes and starts the Flask application.

### `requirements.txt` - Dependencies
Lists required Python packages.

### `README.md` - Documentation
Provides an overview of the project and how to set it up.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
```