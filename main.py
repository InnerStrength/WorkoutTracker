import requests
import datetime
from dotenv import load_dotenv
import os

date = datetime.datetime.now().strftime("%m/%d/%Y")
time = datetime.datetime.now().strftime("%I:%M:%S %p")

load_dotenv("environment.env")

# -------------------  Keys and Endpoints Set Up ----------------- #
nutri_id = os.getenv("NUTRI_ID")
nutri_key = os.getenv("NUTRI_KEY")
nutri_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutri_header = {
    "x-app-id": nutri_id,
    "x-app-key": nutri_key
}
sheety_endpoint = "https://api.sheety.co/fee65a9ca7e1d7089d4f3f13e3af654a/myWorkouts/sheet1"
sheety_headers = {
    "Authorization": os.getenv("AUTHORIZATION")
}

# -------------------  Receive and Parse Exercies ----------------- #
query = input("What exercises did you do and for how long?\n")
nutri_json ={
    "query": query,
    "gender": "male",
    "weight_kg": 79.4,
    "height_cm": 180.3,
    "age": 33
}
responses = requests.post(nutri_endpoint, json=nutri_json, headers=nutri_header).json()["exercises"]

for response in responses:
    print(response)
    response_parse = (response["user_input"], response["duration_min"], response["nf_calories"])
    print(response_parse)
    # ---------------- Access and Post to Sheety --------------- #
    sheety_body = {
        "sheet1":{
            "date": date,
            "time": time,
            "exercise": response_parse[0],
            "duration": response_parse[1],
            "calories": response_parse[2],
            }
    }
    print(sheety_body["sheet1"])
    response = requests.post(sheety_endpoint, json=sheety_body, headers=sheety_headers)
    print(response.json())


