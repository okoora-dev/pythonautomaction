import json
import time

import requests
from pytest import mark

EMAIL = 'doravol203@visignal.com'


def test_KYC1(kyc_data):
    url_path = kyc_data["qa_path"]

    url = f"{url_path}/api/Kyc/UploadKYCFile?tag=ownership_tree"

    with open(r'C:/Users/Administrator/Pictures/Untitled.png', 'rb') as file:
        files = {'file': file}
        authorization = kyc_data['Autho']

        headers = {
            "Authorization": f"Bearer {authorization}",
        }


        # # Make a POST request
        response = requests.post(url, files=files, headers=headers)
        print(response.text)

    url = f"{url_path}/api/Kyc/UploadKYCFile?tag=certificate_of_incorporation"

    with open(r'C:/Users/Administrator/Pictures/Untitled.png', 'rb') as file:
        files = {'file': file}
        authorization = kyc_data['Autho']

        headers = {
            "Authorization": f"Bearer {authorization}",
        }

        # # Make a POST request
        response = requests.post(url, files=files, headers=headers)
        print(response.text)

        url = f"{url_path}/api/Kyc/UploadKYCFile?tag=incorporation_document"

        with open(r'C:/Users/Administrator/Pictures/Untitled.png', 'rb') as file:
            files = {'file': file}
            authorization = kyc_data['Autho']

            headers = {
                "Authorization": f"Bearer {authorization}",
            }

            # # Make a POST request
            response = requests.post(url, files=files, headers=headers)
            print(response.text)