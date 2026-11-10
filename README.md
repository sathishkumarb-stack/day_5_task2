# Customer CRUD API – Task 2

FastAPI application with Customer CRUD operations, API Key authentication, and pagination using PostgreSQL.

## Technologies
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest

## Project Setup

### 1. Install dependencies
```bash
py -m pip install -e ".[dev]"
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/customer_db
API_KEY=your_secret_api_key
```

### 3. Run the application
```bash
py -m uvicorn src.main:app --reload
```

### 4. API Documentation
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /customers | Create customer |
| GET | /customers?page=1&per_page=10 | Get customers with pagination |
| GET | /customers/{customer_id} | Get customer by ID |
| PUT | /customers/{customer_id} | Update customer |
| DELETE | /customers/{customer_id} | Delete customer |
| GET | /health | Health check |

## Authentication

All customer CRUD endpoints require the `X-API-Key` request header.

## Response Status Codes
- 201 – Customer created
- 200 – Successful request
- 401 – API Key missing
- 403 – Invalid API Key
- 404 – Customer not found
- 409 – Duplicate email

## Run Tests
```bash
py -m pytest tests/ -v
```