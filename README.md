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

All the endpoints are running on `http://localhost:5000`

### 1. Plans

#### 1.1 Create a Plan

**Request**
```http
POST /plan
Content-Type: application/json
{
    "name": "Premium",
    "price": 29.99
}
```
**Response**
```json
{
	"message": "The Plan was registered."
}
```
---

#### 1.2 List All Plans

**Request**
```http
GET /plan?page=1&per_page=10
```

**Response**
```json
{
    "data": [
        {
            "name": "Premium",
            "price": 29.99
        }
    ],
    "pagination": {
        "page": 1,
        "pages": 1,
        "per_page": 10,
        "total": 1
    }
}
```
---
#### 1.3 Get Plan By Id

**Request**
```http
GET /plan/1
```

**Response**
```json
{
	"data": {
		"active": true,
		"id": 1,
		"name": "Plan 12",
		"price": 1.0
	}
}
```
---
#### 1.4 Update a Plan

**Request**
```http
PUT /plan/1
Content-Type: application/json
{
    "name": "Plus",
    "price": 39.99
}
```
**Response**
204 - No content

---

#### 1.5 Delete a Plan
**Request**
```http
DELETE /plan/1
```
**Response**
204 - No content

---

#### 1.6 Change status of a Plan

**Request**
```http
POST /plan/1/changeStatus
```
**Response**
204 - No content

---

### 2. User

#### 2.1 Register a user

**Request**
```http
POST /user/register
Content-Type: application/json
{
    "name": "User Name",
    "email": "user@example.com",
    "password": "secret"
}
```

**Response**
```json
{
	"message": "User registered"
}
```
---
#### 2.2 Authenticate a User
**Request**
```http
POST /auth/login
Content-Type: application/json
{    
    "email": "user@example.com",
    "password": "secret"
}
```

**Response**
```json
{
	"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0ODMwOTI1OSwianRpIjoiYzQxNDlhMmItNmNiZS00MTkxLTliNzItZTcwMmUzN2Q0YTlmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDgzMDkyNTksImNzcmYiOiJhY2I0NTJiOC02YzllLTQ1MWItYTMwYS0xOTQ4MjRlNjZmOTUiLCJleHAiOjE3NDgzMTAxNTl9.0CNfRbP8TvjKKzea2bRjZXm91hzicmIF0fJUYbMGOfA"
}
```

---

### 3. Subscriptions

#### 3.1 Subscribe a User to a Plan

**Request**
```http
POST /subscriptions/subscribe
Authorization: Bearer {access_token}
Content-Type: application/json
{    
    "plan_id": 1
}
```

**Response**
```json
{
	"message": "The subscription has been completed."
}
```

---

### 3.2. Cancel a Subscription

**Request**
```http
POST /subscriptions/cancel
Authorization: Bearer {access_token}
```

**Response**
```json
{
	"message": "The subscription has been canceled."
}
```
---
### 3.3 History of Subscriptions

**Request**
```http
GET /subscriptions/history
Authorization: Bearer {access_token}
```

**Response**
```json
{
	"data": [
		{
			"active": false,
			"canceled_at": "2025-05-27T00:56:11",			
			"plan": {
				"id": 1,
				"name": "Premium"
			}
		},
		{
			"active": true,
			"canceled_at": null,			
			"plan": {
				"id": 2,
				"name": "Plus"
			}
		}
	]
}
```