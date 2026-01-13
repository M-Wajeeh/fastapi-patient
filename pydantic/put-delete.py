from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
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
# ------------- PATIENT UPDATE MODEL -------------

class PatientUpdate (BaseModel):
    name: Annotated [Optional[str], Field (default=None)] 
    city: Annotated [Optional[str], Field(default=None)]
    age: Annotated [Optional[int], Field (default=None, gt=0)]
    gender: Annotated [Optional[Literal['male', 'female']], Field (default=None)] 
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated [Optional[float], Field (default=None, gt=0)]


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

@app.put("/Update_patient/{patient_id}")
def updatepatient(patient_id: str, patient_update: PatientUpdate ):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID not found")
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
         
    data[patient_id] = existing_patient_info

    #existing patient info -> pydantic object
    existing_patient_info['id'] = patient_id
    existing_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info= existing_pydantic_obj.model_dump(exclude={"id"})
    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content={
        "message": "Patient information updated successfully"})

@app.delete("/delete_patient/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID not found")

    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={
        "message": "Patient deleted successfully"
    })