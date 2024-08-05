import json
import time

import requests
from pytest import mark


@mark.api_test
@mark.order("first")
def test_Login(data_test):
    url_path = data_test["demo_path"]
    mail = data_test["mail"]
    my_pass = data_test["password"]

    url = f"{url_path}/api/Authentication/Login"

    payload = {
        "username": mail,
        "password": my_pass
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    res_data = response.json()
    print(res_data)
    print(res_data['accessToken'])

    with open('data.json', 'r') as file:
        data = json.load(file)
        data[0]["Autho"] = res_data['accessToken']

    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=2)

    time.sleep(1)
