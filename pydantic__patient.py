#type validation using pydantic
from pydantic import BaseModel
from typing import List, Dict , Optional

class Patient(BaseModel):
    name: str
    age: int
    married: bool
    allergies: Optional[List[str]] = None
    contacts: dict[str,str]


def insert_patient(patient: Patient):
    print("Patient name:", patient.name)
    print("Patient age:", patient.age)
    print("Patient allergies:", patient.allergies)
    print("Patient contacts:", patient.contacts)
    print("inserted successfully")


patient_info = {
    "name": "John Doe",
    "age": 30,
    "married": False,
    "allergies": ["pollens", "nuts"],
    "contacts": {
        "email":"johndoe@gmail.com",
        "phone":"1234567890"
    }
}

patient1 = Patient(**patient_info)
insert_patient(patient1)
