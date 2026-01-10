# Patient Record API

A simple Patient Record Management API built using **FastAPI** and **Pydantic**.  
This project demonstrates REST APIs, data validation, custom field validators, and computed fields.

---

## Tech Stack
- Python 3.10+
- FastAPI
- Pydantic v2
- JSON file storage

---

## Project Structure
```
├── main.py              # FastAPI application and routes
├── patient.json         # Patient records data
├── pydantic_model.py    # Pydantic Patient model
├── validators.py        # Field validators and computed fields
├── README.md
```

---

## API Endpoints

### Root
```
GET /
```
Returns a welcome message.

---

### About
```
GET /about
```
Returns a short description of the API.

---

### View All Patients
```
GET /view
```
Returns all patient records from `patient.json`.

---

### Get Patient by ID
```
GET /patient/{patient_id}
```

- Uses path parameter validation
- Returns `404` if patient ID is not found

Example:
```
/patient/P001
```

---

### Sort Patients
```
GET /sort?field=bmi&sort_by=asc
```

**Query Parameters**
- `field`: `height`, `weight`, `bmi`
- `sort_by`: `asc` or `desc`

Invalid values return proper HTTP errors.

---

## Pydantic Model

The `Patient` model validates and enforces strict typing:
- Name length constraints
- Valid email format
- Strict integer age validation
- Optional allergies
- Structured contact information

---

## Field Validators

Custom validators are used to:
- Restrict email domains
- Normalize patient names to uppercase

These checks run automatically during model creation.

---

## Computed Field

A computed field is used to calculate **BMI**:
- BMI is derived from height and weight
- It is not stored manually
- Always remains consistent with source data

---

## Running the Application

Install dependencies:
```bash
pip install fastapi uvicorn pydantic
```

Start the server:
```bash
uvicorn main:app --reload
```

Open API documentation:
```
http://127.0.0.1:8000/docs
```

---
