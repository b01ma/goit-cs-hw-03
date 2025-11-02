# GoIT Computer Systems - Homework #3

**Woolf University. Neoversity GoIT. Computer Systems Course**

This repository contains solutions for Homework #3, which focuses on database management systems using PostgreSQL and MongoDB with Docker containerization.

## 📋 Overview

The homework consists of two main tasks:

1. **Task 1**: PostgreSQL database with task management system
2. **Task 2**: MongoDB database with CRUD operations for cat management

## 🏗️ Project Structure

```
goit-cs-hw-03/
├── README.md
├── docker-compose.yml          # Docker services configuration
├── Makefile                    # Convenient management commands
├── .env.example               # Environment variables template
├── venv/                      # Python virtual environment
├── src/
│   ├── task_1/               # PostgreSQL Task Management System
│   │   ├── README.md         # Detailed documentation
│   │   ├── requirements.txt  # Python dependencies (psycopg2, faker)
│   │   ├── schema.sql        # Database schema creation
│   │   ├── seed.py          # Database seeding with fake data
│   │   └── sql_requests.py  # SQL query implementations (14 methods)
│   └── task_2/              # MongoDB Cat Management System
│       ├── requirements.txt # Python dependencies (pymongo)
│       └── main.py         # CRUD operations implementation
└── .gitignore
```

## 🚀 Quick Start

### Prerequisites

-   Docker & Docker Compose
-   Python 3.8+
-   Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd goit-cs-hw-03

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Start Services

```bash
# Start PostgreSQL and MongoDB containers
docker-compose up -d

# Check containers status
docker ps
```

### 3. Install Dependencies

```bash
# For Task 1 (PostgreSQL)
pip install -r src/task_1/requirements.txt

# For Task 2 (MongoDB)
pip install -r src/task_2/requirements.txt
```

## 📊 Task 1: PostgreSQL Task Management System

### Description

Implementation of a task management system using PostgreSQL with proper database design, relationships, and comprehensive SQL operations.

### Features

-   **Database Schema**: Users, Status, and Tasks tables with foreign key relationships
-   **Cascade Deletion**: Tasks automatically deleted when user is removed
-   **Unique Constraints**: Email (users) and name (status) fields are unique
-   **Comprehensive SQL Operations**: 14 different query implementations

### Database Schema

```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL
);

-- Status table
CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

-- Tasks table
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  status_id INTEGER REFERENCES status(id),
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### SQL Operations Implemented

1. Get all tasks for a specific user
2. Select tasks by status (using subqueries)
3. Update task status
4. Get users without tasks (NOT IN + subquery)
5. Add new task for user
6. Get incomplete tasks
7. Delete specific task
8. Find users by email pattern (LIKE)
9. Update user name
10. Get task count by status (GROUP BY)
11. Get tasks by email domain (JOIN + LIKE)
12. Get tasks without description
13. Get users with "in progress" tasks (INNER JOIN)
14. Get users with task counts (LEFT JOIN + GROUP BY)

### Usage

```bash
# Setup database schema
docker exec -i task_management_db psql -U admin -d task_management < src/task_1/schema.sql

# Seed with fake data
python src/task_1/seed.py

# Test SQL operations
python src/task_1/sql_requests.py
```

### Connection Parameters

-   **Host**: localhost
-   **Port**: 5432
-   **Database**: task_management
-   **Username**: admin
-   **Password**: password123

## 🍃 Task 2: MongoDB Cat Management System

### Description

Implementation of CRUD (Create, Read, Update, Delete) operations using MongoDB and PyMongo library for managing cat information.

### Features

-   **Complete CRUD Operations**: Create, read, update, and delete cats
-   **Error Handling**: Comprehensive try-catch blocks for all operations
-   **Data Validation**: Duplicate prevention and existence checks
-   **Professional Logging**: Clear success/error messages

### Document Structure

```json
{
    "_id": ObjectId("60d24b783733b1ae668d4a77"),
    "name": "barsik",
    "age": 3,
    "features": ["walks in slippers", "allows petting", "ginger"]
}
```

### CRUD Operations

-   **Create**: `create_cat(name, age, features)` - Add new cat with duplicate check
-   **Read**:
    -   `read_all_cats()` - Display all cats
    -   `read_cat_by_name(name)` - Find specific cat
-   **Update**:
    -   `update_cat_age(name, new_age)` - Update cat's age
    -   `update_cat_features(name, new_features)` - Add features to cat
-   **Delete**:
    -   `delete_cat(name)` - Remove specific cat
    -   `delete_all_cats()` - Remove all cats

### Usage

```bash
# Run CRUD operations demo
python src/task_2/main.py
```

### Connection Parameters

-   **Host**: localhost
-   **Port**: 27017
-   **Database**: cats_database
-   **Username**: admin
-   **Password**: password123

## 🐳 Docker Services

### PostgreSQL Service

```yaml
postgres:
    image: postgres:15-alpine
    container_name: task_management_db
    environment:
        POSTGRES_DB: task_management
        POSTGRES_USER: admin
        POSTGRES_PASSWORD: password123
    ports:
        - "5432:5432"
```

### MongoDB Service

```yaml
mongodb:
    image: mongo:7.0
    container_name: cats_db
    environment:
        MONGO_INITDB_ROOT_USERNAME: admin
        MONGO_INITDB_ROOT_PASSWORD: password123
        MONGO_INITDB_DATABASE: cats_database
    ports:
        - "27017:27017"
```

## 🛠️ Development Tools

### Makefile Commands

```bash
make help          # Show available commands
make up            # Start all containers
make down          # Stop containers
make logs          # Show PostgreSQL logs
make clean         # Remove containers and volumes
make psql          # Connect to PostgreSQL
make demo          # Run database demo
```

### Useful Commands

```bash
# PostgreSQL
docker exec -it task_management_db psql -U admin -d task_management

# MongoDB
docker exec -it cats_db mongosh -u admin -p password123 --authenticationDatabase admin

# Check container logs
docker-compose logs postgres
docker-compose logs mongodb
```

## 📚 Dependencies

### Task 1 (PostgreSQL)

-   `psycopg2-binary==2.9.11` - PostgreSQL adapter
-   `faker==37.12.0` - Generate fake data

### Task 2 (MongoDB)

-   `pymongo==4.10.1` - MongoDB driver

## ✅ Acceptance Criteria

### Task 1 Criteria - ✅ COMPLETED

1. ✅ Tables created according to requirements
2. ✅ Unique constraints on email (users) and name (status)
3. ✅ Cascade deletion implemented for user-task relationship
4. ✅ Table creation script provided (schema.sql)
5. ✅ Seed script with Faker library implemented
6. ✅ All required SQL queries implemented (14 operations)

### Task 2 Criteria - ✅ COMPLETED

1. ✅ Database created according to document structure requirements
2. ✅ All CRUD operations implemented
3. ✅ Exception handling for all database operations
4. ✅ Functions clearly commented and well-structured

## 🎯 Learning Outcomes

This homework demonstrates proficiency in:

-   **Database Design**: Proper schema design with relationships and constraints
-   **SQL Mastery**: Complex queries including JOINs, subqueries, and aggregations
-   **NoSQL Operations**: MongoDB document manipulation and CRUD operations
-   **Python Database Integration**: Using psycopg2 and PyMongo libraries
-   **Docker Containerization**: Multi-service application deployment
-   **Error Handling**: Robust exception management in database operations
-   **Code Organization**: Clean, documented, and maintainable code structure

## 👨‍💻 Author

**Student**: b01ma  
**Course**: GoIT Computer Systems  
**Institution**: Woolf University, Neoversity  
**Date**: November 2025

## 📄 License

This project is for educational purposes as part of the GoIT Computer Systems course.
