from pydantic import BaseModel, EmailStr, field_validator, computed_field
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    weight_kg: float
    height_m: float
    age: int
    married: bool 
    allergies: List[str]
    contacts: Dict[str, str]

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        allowed_domains = ['numl.edu.pk', 'nust.edu.pk']
        domain = value.split('@')[-1]
        if domain in allowed_domains:
            return value
        raise ValueError("Email domain is not valid")

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        return value.upper()

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight_kg / (self.height_m ** 2), 2)


def insert_patient(patient: Patient):
    print("Patient name:", patient.name)
    print("Patient age:", patient.age)
    print("Patient allergies:", patient.allergies)
    print("Patient contacts:", patient.contacts)
    print("Patient email:", patient.email)
    print("Patient BMI:", patient.bmi)
    print("Inserted successfully")


patient_info = {
    "name": "John Doe",
    "age": 30,
    "email": "aws@numl.edu.pk",
    "weight_kg": 72,
    "height_m": 1.75,
    "married": False,
    "allergies": ["pollens", "nuts"],
    "contacts": {
        "email": "johndoe@numl.edu.pk",
        "phone": "1234567890"
    }
}

patient1 = Patient(**patient_info)
insert_patient(patient1)
