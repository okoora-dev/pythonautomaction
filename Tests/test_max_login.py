import pytest
import requests
import json

payload = {
  "userName": "godom91844@deligy.com",
  "password": "Okoora1!"
}

headers = {"Content-Type" : "application/json"}

@pytest.mark.order(1)
@pytest.mark.max
def test_max_login_api(get_user_data):
    user_data = get_user_data
    url = user_data['path']
    login_response = send_login(url,payload,headers)
    login_data = login_response.json()
    assert login_response.status_code == 200

    #Open file and save the auth
    with open('user_data.json', 'r') as file:
        data = json.load(file)
        data["Auth"] = login_data['accessToken']
    with open("user_data.json", "w") as json_file:
        json.dump(data, json_file, indent=2)

def send_login(url,payload,header):
    url = f"{url}/api/Authentication/login"
    response = requests.post(url,json=payload,headers=header)
    return response





















