# Cloud Insights Test

This repository is an API that can be used to register plans and users subscriptions.

## Install

a) Configure environment file

```bash
cp .env-sample .env
```

b) Up the docker containers

```bash
docker compose up -d --build
```

c)  Run migrations

```bash
docker compose exec app flask db upgrade  
```

d) Run tests
```bash
docker compose exec app pytest
```

## API Endpoints Examples

### 1. Create a Plan

**Request**
```http
POST /plans
Content-Type: application/json

{
    "name": "Premium",
    "price": 29.99,
    "duration_months": 12
}
```

**Response**
```json
{
    "id": 1,
    "name": "Premium",
    "price": 29.99,
    "duration_months": 12
}
```

---

### 2. List All Plans

**Request**
```http
GET /plans
```

**Response**
```json
[
    {
        "id": 1,
        "name": "Premium",
        "price": 29.99,
        "duration_months": 12
    }
]
```

---

### 3. Register a User

**Request**
```http
POST /users
Content-Type: application/json

{
    "email": "user@example.com",
    "name": "User Name"
}
```

**Response**
```json
{
    "id": 1,
    "email": "user@example.com",
    "name": "User Name"
}
```

---

### 4. Subscribe a User to a Plan

**Request**
```http
POST /subscriptions
Content-Type: application/json

{
    "user_id": 1,
    "plan_id": 1
}
```

**Response**
```json
{
    "id": 1,
    "user_id": 1,
    "plan_id": 1,
    "start_date": "2024-06-01",
    "end_date": "2025-06-01"
}
```

---

### 5. List User Subscriptions

**Request**
```http
GET /users/1/subscriptions
```

**Response**
```json
[
    {
        "id": 1,
        "plan_id": 1,
        "start_date": "2024-06-01",
        "end_date": "2025-06-01"
    }
]
```

---

