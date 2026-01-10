#type validation using pydantic
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict , Optional, Annotated

class Patient(BaseModel):
    #name with metadata using annotated
    name: Annotated[str, Field(min_length=4,max_length=50,title="Name of patient",
                               description="Full name of patient less than 50 characters",example="John Doe")]
    email: EmailStr
    age: Annotated[int,Field(gt=18,lt=50,strict=True)]  #if we add strict=true it will only accept int not float

    #using annotated to set a default value
    married: Annotated[bool, Field(default=False, title="Is the patient married or not: True/False")]
    allergies: Optional[List[str]] = None
    contacts: dict[str,str]


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
    "email":"aws@gmail.com",
    "married": False,
    "allergies": ["pollens", "nuts"],
    "contacts": {
        "email":"johndoe@gmail.com",
        "phone":"1234567890"
    }
}

patient1 = Patient(**patient_info)
insert_patient(patient1)
