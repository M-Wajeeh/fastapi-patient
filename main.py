from fastapi import FastAPI , Path , HTTPException, Query
import json

app = FastAPI()
                   
def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
    return data

@app.get("/")
def display():
    return {"message": "Welcome to the Patient Record API!"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage patient record!"}

@app.get("/view")
def view_data():
    data = load_data()
    return data


@app.get('/patient/{patient_id}')
def get_patient(patient_id: str=Path(..., description="The ID of the patient to be retrieved"),example="P001"):
    #load data from json file
    data=load_data()
    #check for patient id in data
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Error! Patient ID not found.")
    
@app.get('/sort')
def sort_patients(field: str=Query(..., description="The field to sort patients by", example="age"), 
                  sort_by: str=Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending", example="asc")):
    if field not in ['height','weight','bmi']:
        raise HTTPException(status_code=400, detail="Error! Invalid field for sorting, select from 'height', 'weight', or 'bmi'.")
    
    if sort_by not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Error! Invalid sort order.")
    
    data = load_data()

    sort_order = True if sort_by == 'desc' else False

    sorted_data = sorted(
      data.items(),
      key=lambda item: item[1].get(field, 0),
      reverse=sort_order
)

    