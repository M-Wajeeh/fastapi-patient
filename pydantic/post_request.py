from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

DATA_FILE = "patient.json"

# -------------------- FILE HANDLING --------------------

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------- MODEL --------------------

class Patient(BaseModel):
    id: Annotated[int, Field(..., description="Unique patient ID")]
    name: Annotated[str, Field(min_length=3, max_length=12)]
    city: Annotated[str, Field(min_length=3, max_length=20)]
    age: Annotated[int, Field(gt=0, lt=100)]
    gender: Annotated[Literal["male", "female", "other"],Field(description='Gender of the patient "male", "female", "other" ')]
    height: Annotated[float, Field(description="Height in cm")]
    weight: Annotated[float, Field(description="Weight in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        return "Obesity"

# -------------------- ROUTES --------------------

@app.get("/")
def home():
    return {"message": "Patient Record API is running"}

@app.post("/add_patient/")
def add_patient(patient: Patient):
    data = load_data()

    if str(patient.id) in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")

    data[str(patient.id)] = patient.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(status_code=201, content={
        "message": "Patient added successfully",
        "patient": patient.model_dump()
    })
