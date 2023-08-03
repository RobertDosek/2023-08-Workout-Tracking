import os
import requests
from datetime import datetime

NUTRI_APP_ID = os.environ["NUTRI_APP_ID"]
NUTRI_API_KEY = os.environ["NUTRI_API_KEY"]
GENDER = "male"
WEIGHT_KG = 95
HEIGHT_CM = 175
AGE = 47
PROJECT_NAME = "My workouts"
SHEET_NAME = "workouts"
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/1439e1d085b64e8b78556f423a9f87a4/myWorkouts/workouts"

# input exercise info
question = input("What exercises you did today?: ")

headers = {
    "x-app-id": NUTRI_APP_ID,
    "x-app-key": NUTRI_API_KEY
}

parameters = {
 "query": question,
 "gender": GENDER,
 "weight_kg": WEIGHT_KG,
 "height_cm": HEIGHT_CM,
 "age": AGE
}

# post to nutritionix
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

# date manipulation
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# post rows into sheet
for exercise in result["exercises"]:

    # each column is one parameter, must be in nested payload
    sheet_params = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]

        }
    }

    # bearer token Authentication
    bearer_headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_params, headers=bearer_headers)
    print(sheet_response.text)



