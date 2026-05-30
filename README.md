# Breathe ESG – Tech Intern Assignment

A full-stack ESG data ingestion platform built using Django, React, PostgreSQL, Render, and Vercel.

## Live Demo

### Frontend
https://breath-esg-seven.vercel.app

### Backend API
https://breath-esg-backend-cx8m.onrender.com

---

# Problem Statement

Companies provide ESG activity data from multiple systems such as:

- SAP Exports
- Utility Bills
- Travel Systems
- Manual Excel Sheets

The platform ingests raw SAP CSV files, normalizes data, identifies suspicious records, and provides a review workflow for ESG teams.

---

# Features Implemented

## 1. SAP CSV Upload

Users can upload SAP export CSV files.

Supported fields:

- Fuel
- Quantity
- Unit

Example:

| Fuel | Quantity | Unit |
|--------|----------|------|
| Diesel | 1000 | L |
| Diesel | -50 | L |

---

## 2. Data Normalization

The system automatically normalizes units.

Examples:

| Input | Output |
|---------|---------|
| 1000 L | 1000 L |
| 5000 ml | 5 L |
| 10 gal | 37.85 L |

---

## 3. Suspicious Record Detection

The system automatically flags suspicious records.

Rules implemented:

- Negative quantity values
- Invalid quantities
- Failed normalization

Example:

| Value | Status |
|---------|---------|
| 1000 L | Valid |
| -50 L | Suspicious |

---

## 4. Review Queue

All uploaded records appear in a review queue.

Reviewers can:

- Approve records
- Reject records

---

## 5. Dashboard

Real-time dashboard displaying:

- Total Records
- Approved Records
- Suspicious Records

---

## 6. PostgreSQL Storage

All uploaded records are stored permanently in PostgreSQL.

Tables include:

- Company
- DataSource
- EmissionRecord
- AuditLog

---

## 7. Audit Trail

Every action is stored for tracking.

Examples:

- Upload
- Approve
- Reject

This provides traceability and governance.

---

# Architecture

```
React Frontend (Vercel)
        |
        |
        ▼
Django REST API (Render)
        |
        |
        ▼
PostgreSQL Database (Render)
```

---

# Technology Stack

## Frontend

- React
- Axios
- CSS

## Backend

- Django
- Django REST Framework

## Database

- PostgreSQL

## Deployment

- Vercel
- Render

---

# API Endpoints

## Upload SAP File

POST

```http
/api/upload/sap/
```

### Form Data

```text
file: sap_sample.csv
```

### Response

```json
{
  "rows_read": 3,
  "records_created": 3,
  "suspicious_records": 1
}
```

---

## Review Queue

GET

```http
/api/review/
```

Returns all uploaded records.

---

## Update Review Status

POST

```http
/api/review/<id>/
```

Example:

```json
{
  "status": "APPROVED"
}
```

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/yeolevishakha27/Breath_ESG.git
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`

```env
DATABASE_URL=your_database_url
DEBUG=True
```

Run migrations

```bash
python manage.py migrate
```

Start server

```bash
python manage.py runserver
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# Deployment

## Backend

Hosted on Render

```text
https://breath-esg-backend-cx8m.onrender.com
```

## Frontend

Hosted on Vercel

```text
https://breath-esg-seven.vercel.app
```

---

# Assignment Coverage

| Requirement | Status |
|------------|---------|
| SAP CSV Upload | ✅ |
| Data Ingestion | ✅ |
| Normalization | ✅ |
| Suspicious Detection | ✅ |
| Review Workflow | ✅ |
| Dashboard | ✅ |
| Audit Logging | ✅ |
| PostgreSQL | ✅ |
| Deployment | ✅ |

---

# Author

**Vishakha Yeole**

B.Tech Information Technology  
G.H. Raisoni College of Engineering & Management, Pune

GitHub:
https://github.com/yeolevishakha27

LinkedIn:
https://www.linkedin.com/in/vishakha-yeole-a12204263/
