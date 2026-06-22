# CyberWatch API Documentation

## Overview

CyberWatch is a Security Operations Center (SOC) monitoring and incident management platform designed to help security analysts monitor devices, manage security incidents, and track system activity.

### Base URL

```http
http://127.0.0.1:5000/api/v1
```

### Authentication

CyberWatch uses JSON Web Tokens (JWT) for authentication.

Protected endpoints require the following header:

```http
Authorization: Bearer <your_token>
```

### User Roles

The system currently supports:

* Admin
* Analyst

Admins have access to administrative functions such as user management, role management, and log archiving.



# Authentication Endpoints

## Register User

### Endpoint

```http
POST /auth/register
```

### Request Body

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "john123"
}
```

### Success Response

```json
{
  "status": "success",
  "message": "User registered successfully"
}
```

---

## Login User

### Endpoint

```http
POST /auth/login
```

### Request Body

```json
{
  "username": "admin",
  "password": "admin123"
}
```

### Success Response

```json
{
  "status": "success",
  "message": "Login successful",
  "token": "<jwt_token>"
}
```

---

## Current User

### Endpoint

```http
GET /auth/me
```

### Authentication

Required

---

## Change Password

### Endpoint

```http
PATCH /auth/change-password
```

### Authentication

Required

### Request Body

```json
{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

---

## Logout

### Endpoint

```http
POST /auth/logout
```

### Authentication

Required


# User Management Endpoints

> All User Management endpoints require Admin privileges.

---

## Get All Users

### Endpoint

GET /users

### Authentication

Required (Admin)

### Search

Search users by username, email, or role.

Example:

GET /users?search=alice

GET /users?search=admin

### Success Response

```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@cyberwatch.com",
      "role": "admin"
    }
  ]
}
```

---

## Get Single User

### Endpoint

GET /users/<user_id>

### Authentication

Required (Admin)

### Example

GET /users/1

### Success Response

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@cyberwatch.com",
    "role": "admin"
  }
}
```

---

## Update User Role

### Endpoint

PATCH /users/<user_id>/role

### Authentication

Required (Admin)

### Request Body

```json
{
  "role": "admin"
}
```

### Allowed Roles

* admin
* analyst

### Success Response

```json
{
  "status": "success",
  "message": "User role updated to admin"
}
```

### Audit Logging

This endpoint creates an audit log entry recording:

* Who performed the role change
* Which user was affected
* The new role assigned


# Log Management Endpoints

> All Log Management endpoints require authentication.

---

## Get All Logs

### Endpoint

GET /logs

### Authentication

Required

### Pagination

Example:

GET /logs?page=1&limit=10

### Filtering

Filter by severity:

GET /logs?severity=high

Filter by status:

GET /logs?status=open

Filter archived logs:

GET /logs?archived=true

### Search

Search by:

* Event
* Severity
* Status
* Device hostname

Examples:

GET /logs?search=failed

GET /logs?search=high

GET /logs?search=Firewall

### Success Response

```json
{
  "status": "success",
  "page": 1,
  "limit": 10,
  "total_logs": 25,
  "total_pages": 3,
  "logs": [...]
}
```

---

## Create Log

### Endpoint

POST /logs

### Authentication

Required

### Request Body

```json
{
  "device_id": 1,
  "event": "Failed Login Attempt",
  "severity": "high"
}
```

### Allowed Severity Levels

* low
* medium
* high

### Success Response

```json
{
  "status": "success",
  "message": "Log received successfully"
}
```

---

## Get Single Log

### Endpoint

GET /logs/<log_id>

### Authentication

Required

### Example

GET /logs/1

---

## Update Log

### Endpoint

PUT /logs/<log_id>

### Authentication

Required

### Purpose

Update log details such as event information and severity.

---

## Update Log Status

### Endpoint

PATCH /logs/<log_id>/status

### Authentication

Required

### Request Body

```json
{
  "status": "resolved"
}
```

### Common Status Values

* open
* investigating
* resolved

---

## Archive Log

### Endpoint

PATCH /logs/<log_id>/archive

### Authentication

Required (Admin)

### Rules

Only resolved incidents can be archived.

### Success Response

```json
{
  "status": "success",
  "message": "Log archived successfully"
}
```

### Audit Logging

This endpoint creates an audit record whenever a log is archived.


# Device Management Endpoints

> All Device Management endpoints require authentication.

---

## Get All Devices

### Endpoint

GET /devices

### Authentication

Required

### Search

Search by:

* Hostname
* IP Address
* Operating System
* Status

Examples:

GET /devices?search=Firewall

GET /devices?search=Linux

GET /devices?search=192.168

GET /devices?search=active

### Success Response

```json
{
  "status": "success",
  "total_devices": 3,
  "devices": [...]
}
```

---

## Register Device

### Endpoint

POST /devices

### Authentication

Required

### Request Body

```json
{
  "hostname": "Firewall-01",
  "ip_address": "192.168.1.10",
  "operating_system": "Linux"
}
```

### Success Response

```json
{
  "status": "success",
  "message": "Device registered successfully"
}
```

### Audit Logging

This endpoint creates an audit record when a device is registered.

---

## Get Single Device

### Endpoint

GET /devices/<device_id>

### Authentication

Required

### Example

GET /devices/1

---

## Update Device Status

### Endpoint

PATCH /devices/<device_id>/status

### Authentication

Required

### Request Body

```json
{
  "status": "offline"
}
```

### Common Status Values

* active
* inactive
* offline

---

## Get Device Logs

### Endpoint

GET /devices/<device_id>/logs

### Authentication

Required

### Example

GET /devices/1/logs

### Purpose

Retrieve all logs associated with a specific device.


# Dashboard Endpoints

---

## Dashboard Statistics

### Endpoint

GET /dashboard/stats

### Authentication

Required

### Purpose

Retrieve summary statistics for the CyberWatch dashboard.

### Example Response

```json
{
  "status": "success",
  "data": {
    "total_devices": 10,
    "total_logs": 150,
    "open_incidents": 12,
    "resolved_incidents": 138
  }
}
```


# System Endpoints

---

## Health Check

### Endpoint

GET /health

### Authentication

Not Required

### Purpose

Verify that the CyberWatch API is running and available.

### Success Response

```json
{
  "status": "success",
  "message": "CyberWatch API is running"
}
```
