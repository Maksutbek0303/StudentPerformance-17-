from fastapi import FastAPI
import joblib
import uvicorn
from pydantic import BaseModel
student_app = FastAPI()

model = joblib.load('model.pkl')
scaler = joblib.load('scaler (1).pkl')

class StudentSchema(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation: str
    match_score: int
    reading_score: int

race_ethnicity_list = ['group B', 'group C', 'group D', 'group E']
parental_education_list = ["bachelor's degree", 'high school', "master's degree", 'some college', 'some high school']

@student_app.post('/predict/')
async def predict(student: StudentSchema):
    student_dict = student.dict()

    new_gender = student_dict.pop('gender')

    gender1or_0 = [
        1 if new_gender == 'male' else 0
    ]

    new_race = student_dict.pop('race_ethnicity')
    race1or_0 = [
        1 if new_race == i else 0 for i in race_ethnicity_list

    ]

    new_parent = student_dict.pop('parental_level_of_education')
    parent1_0 = [
        1 if new_parent == i else 0 for i in parental_education_list

    ]

    new_lunch = student_dict.pop('lunch')
    test1_0 = [
        1 if new_lunch == "standard" else 0,

    ]

    new_test = student_dict.pop('test_preparation')
    lunch1_0 = [
        1 if new_test == "none" else 0,

    ]


    features =  list(student_dict.values()) + gender1or_0 + race1or_0 + parent1_0 + test1_0 + lunch1_0

    scaled_data = scaler.transform([features])
    print(model.predict(scaled_data))
    pred = model.predict(scaled_data)[0]
    return {'predict': round(pred, 2)}





if __name__ == '__main__':
    uvicorn.run(student_app, host='127.0.0.1', port=8000)
