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

# Patient API Documentation

## Base URL

```
https://assign.immunefile.com/
```

## Overview

This API provides access to patient data with pagination, search, and filtering capabilities. All responses are in JSON format with consistent structure.

---

## Authentication

**No authentication required for Patient API** - This is a mock API for development purposes.

---

## Response Format

All API responses follow this consistent format:

### Success Response

```json
{
  "success": true,
  "data": {...},
  "pagination": {...}  // Only for paginated endpoints
}
```

### Error Response

```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error info" // Optional
}
```

---

## Endpoints

### 1. Get Patients List (Paginated)

Get a paginated list of all patients with optional search and filtering.

**Endpoint:** `GET /api/patients`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (starts from 1) |
| `limit` | integer | 10 | Number of items per page (max: 100) |
| `search` | string | - | Search in patient name or medical issue |

**Example Requests:**

```bash
# Get first page with default limit (10 items)
GET /api/patients

# Get page 2 with 5 items per page
GET /api/patients?page=2&limit=5

# Search for patients with "fever"
GET /api/patients?search=fever

# Combined: search with pagination
GET /api/patients?search=back&page=1&limit=3
```

**Example Response:**

```json
{
  "success": true,
  "data": [
    {
      "patient_id": 1,
      "patient_name": "Zoe Normanvill",
      "age": 77,
      "photo_url": "https://example.com/photo1.jpg",
      "contact": [
        {
          "address": "5 Moulton Hill",
          "number": "157-677-1133",
          "email": "smcneice0@geocities.com"
        }
      ],
      "medical_issue": "fever"
    }
  ],
  "pagination": {
    "current_page": 1,
    "per_page": 10,
    "total_records": 50,
    "total_pages": 5,
    "has_next": true,
    "has_previous": false
  }
}
```

---

### 2. Get Single Patient

Get detailed information about a specific patient by ID.

**Endpoint:** `GET /api/patients/{patient_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `patient_id` | integer | Yes | Unique patient identifier |

**Example Requests:**

```bash
# Get patient with ID 1
GET /api/patients/1

# Get patient with ID 25
GET /api/patients/25
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "patient_id": 1,
    "patient_name": "Zoe Normanvill",
    "age": 77,
    "photo_url": "https://example.com/photo1.jpg",
    "contact": [
      {
        "address": "5 Moulton Hill",
        "number": "157-677-1133",
        "email": "smcneice0@geocities.com"
      }
    ],
    "medical_issue": "fever"
  }
}
```

**Error Response (Patient Not Found):**

```json
{
  "success": false,
  "message": "Patient not found"
}
```

---

### 3. Get Patient Statistics

Get statistical summary of all patient data.

**Endpoint:** `GET /api/patients/stats`

**Example Request:**

```bash
GET /api/patients/stats
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "total_patients": 100,
    "average_age": 45,
    "medical_issues_breakdown": {
      "fever": 15,
      "headache": 12,
      "back pain": 8,
      "flu symptoms": 10,
      "allergies": 7,
      "other": 48
    }
  }
}
```

---

### 4. Health Check

Simple endpoint to check if the API is running.

**Endpoint:** `GET /health`

**Example Request:**

```bash
GET /health
```

**Example Response:**

```json
{
  "status": "OK",
  "message": "Patient API is running"
}
```

---

## Data Structure

### Patient Object

```json
{
  "patient_id": 1, // Unique identifier
  "patient_name": "John Doe", // Full name
  "age": 45, // Age in years
  "photo_url": "https://...", // Profile photo URL
  "contact": [
    // Contact information array
    {
      "address": "123 Main St", // Physical address
      "number": "555-1234", // Phone number
      "email": "john@example.com" // Email address
    }
  ],
  "medical_issue": "fever" // Primary medical concern
}
```

### Pagination Object

```json
{
  "current_page": 1, // Current page number
  "per_page": 10, // Items per page
  "total_records": 50, // Total number of records
  "total_pages": 5, // Total number of pages
  "has_next": true, // Whether there's a next page
  "has_previous": false // Whether there's a previous page
}
```

---

## Error Codes

| HTTP Status | Description           | Example Scenario                               |
| ----------- | --------------------- | ---------------------------------------------- |
| 200         | Success               | Request completed successfully                 |
| 400         | Bad Request           | Invalid parameters (e.g., invalid page number) |
| 404         | Not Found             | Patient ID doesn't exist or invalid endpoint   |
| 500         | Internal Server Error | Server-side error or invalid JSON data         |

---

## Testing the API

### Using cURL

```bash
# Test patient list
curl "https://assign.immunefile.com/api/patients?page=1&limit=5"

# Test single patient
curl "https://assign.immunefile.com/api/patients/1"

# Test search
curl "https://assign.immunefile.com/api/patients?search=fever"

# Test statistics
curl "https://assign.immunefile.com/api/patients/stats"

# Test health check
curl "https://assign.immunefile.com/health"
```

### Using Postman

1. Create a new collection called "Patient API"
2. Add requests for each endpoint above
3. Set the base URL to your server address
4. Test different parameter combinations

---

## Common Use Cases

### 1. Patient List with Pagination

Perfect for displaying a table or grid of patients with page navigation.

### 2. Search Functionality

Filter patients by name or medical issue for quick lookup.

### 3. Patient Detail View

Show complete patient information in a modal or separate page.

### 4. Dashboard Statistics

Display summary cards with patient counts and medical issue breakdown.

### 5. Infinite Scroll

Load more patients by incrementing the page parameter.

---

## Rate Limits

**No rate limits** - This is a development API.

## CORS

**Enabled for all origins** - Frontend applications can call this API from any domain.

---

## Support

For questions or issues with this API, please contact the development team.

**Happy coding! 🚀**

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
