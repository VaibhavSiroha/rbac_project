# Django RBAC Project

A Django REST Framework project implementing Role-Based Access Control (RBAC) with JWT authentication.

## Features

- JWT Authentication
- Role-based access control (Admin, Manager, User)
- User management API
- Permission-based access control
- SQLite database

## Quick Setup (5 minutes)

1. Clone the repository:

```bash
git clone <repository-url>
cd rbac_project
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication

#### Register a new user

```bash
POST /api/auth/register/
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "role": "User"  # Optional, defaults to "User"
}
```

#### Login

```bash
POST /api/auth/login/
{
    "username": "user@example.com",
    "password": "securepass123"
}
```

Returns JWT tokens and user permissions.

#### Refresh Token

```bash
POST /api/auth/token/refresh/
{
    "refresh": "<refresh_token>"
}
```

### User Management

#### List Users

```bash
GET /api/users/
```

- Admin/Manager: Lists all users
- User: Lists only their own profile

#### Create User

```bash
POST /api/users/create/
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "role": "User"
}
```

Admin/Manager only

#### Update User

```bash
PUT /api/users/{id}/
{
    "username": "updateduser",
    "email": "updated@example.com"
}
```

Admin/Manager only

#### Delete User

```bash
DELETE /api/users/{id}/delete/
```

Admin only

#### Change User Role

```bash
PUT /api/users/{id}/role/
{
    "role": "Manager"
}
```

Admin only

## Role Permissions

### Admin

- Full access to all endpoints
- Can manage user roles
- Can delete users

### Manager

- Can view all users
- Can create users
- Can update users
- Cannot delete users
- Cannot manage roles

### User

- Can only view their own profile
- Cannot create/update/delete users
- Cannot manage roles

## Testing

Run the test suite:

```bash
python manage.py test users
```

## Security

- JWT authentication
- Role-based access control
- Password validation
- Input sanitization
- Protected endpoints

## Default Admin Credentials

After running migrations and creating a superuser, you can use:

- Username: (your superuser username)
- Password: (your superuser password)

## Development

The project uses:

- Django 5.2
- Django REST Framework
- djangorestframework-simplejwt
- SQLite (development)

---

# RBAC API Documentation

## Overview

This API provides authentication and role-based access control for user management.

## Authentication

JWT authentication using djangorestframework-simplejwt.

## Roles & Permissions

- **Admin:** all permissions
- **Manager:** view, create, update users
- **User:** view only their own profile

## Endpoints

All endpoints are under `/api/`.

### Auth

- **POST /api/auth/register/**
  - Register a new user
  - Body: `{ "username": "user", "email": "user@mail.com", "password": "pass", "role": "User" }`
- **POST /api/auth/login/**
  - Login, returns JWT tokens + user info + permissions
  - Body: `{ "username": "user", "password": "pass" }`

### User Management

- **GET /api/users/**
  - List users (Admin/Manager only; Users see only their profile)
- **POST /api/users/**
  - Create a new user (Admin/Manager only)
- **PUT /api/users/{id}/**
  - Update user info (Admin/Manager only)
- **DELETE /api/users/{id}/**
  - Delete user (Admin only)
- **PUT /api/users/{id}/role/**
  - Change user role (Admin only)

### Example: Register

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "bob", "email": "bob@mail.com", "password": "bobpass", "role": "User"}'
```

### Example: Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "bob", "password": "bobpass"}'
```

### Example: List Users (as Admin)

```bash
curl -X GET http://localhost:8000/api/users/ \
  -H 'Authorization: Bearer <access_token>'
```

## 🧪 Test Scenarios

- Manager tries to delete a user → denied (403)
- User tries to view all users → sees only their own profile

## 📝 Notes

- All endpoints require JWT authentication except register/login.
- Use the returned access token in the `Authorization: Bearer <token>` header.
- Input is validated and sanitized.

---

**No frontend included. Backend API only.**
