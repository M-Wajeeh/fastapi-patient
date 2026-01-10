#Field validator is used for  customizing validation logic for specific fields, 
# allowing you to enforce complex business rules, transform data (like cleaning strings), 
# or apply rules that go beyond basic type hints (like checking if an age is within a valid range).

from pydantic import BaseModel, EmailStr, Field , field_validator
from typing import List, Dict , Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    married: bool 
    allergies: List[str]
    contacts: dict[str,str]

#create a new method for validation of mails keeping in mind it is to be used with a decorator
    @field_validator('email')
    @classmethod
    def validate_email(cls,value):
        domain=['numl.edu.pk','nust.edu.pk']
        domain_found=value.split('@')[-1]
        if domain_found in domain:
            return value
        raise ValueError("Email domain is not valid")

#create a new method so that name should always bs in capitals
    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        return value.upper()

def insert_patient(patient: Patient):
    print("Patient name:", patient.name)
    print("Patient age:", patient.age)
    print("Patient allergies:", patient.allergies)
    print("Patient contacts:", patient.contacts)
    print("Patient email:", patient.email)
    print("inserted successfully")


patient_info = {
    "name": "John Doe",
    "age": 30,
    "email":"aws@numl.edu.pk",
    "married": False,
    "allergies": ["pollens", "nuts"],
    "contacts": {
        "email":"johndoe@numl.edu.pk",
        "phone":"1234567890"
    }
}

patient1 = Patient(**patient_info) # validation and coersion is done at this step
insert_patient(patient1)
