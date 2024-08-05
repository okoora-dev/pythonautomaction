import json
import time

import requests
from pytest import mark

EMAIL = 'kiyic66765@vasteron.com'
ID = 227383148

def test_KYC(kyc_data):
    url_path = kyc_data["demo_path"]
    url = f"{url_path}/api/Signup/CreateNewUser"
    payload = {
            "accountType": 2,
            "email": EMAIL,
            "countryCode": "IL",
            "phoneCode": "972",
            "phoneNumber": "534040500",
            "passwords":
                {
                    "password": "Okoora1!",
                    "confirmPassword": "Okoora1!"
                },
            "role": 1,
            "firstName": "Pay",
            "lastName": "MeRoy",
            "idNumber": ID,
            "birthDate": "10-02-1995",
            "city": "Givatayim",
            "address": "blkabka",
            "houseNumber": "234",
            "zipCode": "1242341"
        }

    response = requests.post(url, json=payload)
    assert response.status_code == 200
    url_path = kyc_data["demo_path"]
    my_pass = kyc_data["password"]

    url = f"{url_path}/api/Authentication/Login"

    payload = {
        "username": EMAIL,
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

    with open('./Login_KYC.json', 'r') as file:
        data = json.load(file)
        data[0]["Autho"] = res_data['accessToken']
        data[0]['mail'] = EMAIL

    with open("./Login_KYC.json", "w") as json_file:
        json.dump(data, json_file, indent=2)

    time.sleep(1)

    url_path = kyc_data["demo_path"]

    url = f"{url_path}/api/Kyc/UploadKYCFile?tag=ownership_tree"

    with open(r'C:/Users/Administrator/Pictures/Untitled.png', 'rb') as file:
        files = {'file': file}
        authorization = kyc_data['Autho']

        headers = {
            "Authorization": f"Bearer {authorization}",
        }

        # # Make a POST request
        response = requests.post(url, files=files, headers=headers)
        result = response.json()
        with open('./Login_KYC.json', 'r') as file:
            data = json.load(file)
            data[0]["ownership_tree"] = result
            print(data[0]["ownership_tree"])

        with open("./Login_KYC.json", "w") as json_file:
            json.dump(data, json_file, indent=2)

    url = f"{url_path}/api/Kyc/UploadKYCFile?tag=certificate_of_incorporation"

    with open(r'C:/Users/Administrator/Pictures/Untitled.png', 'rb') as file:
        files = {'file': file}
        authorization = kyc_data['Autho']

        headers = {
            "Authorization": f"Bearer {authorization}",
        }

        # # Make a POST request
        response = requests.post(url, files=files, headers=headers)
        result = response.json()
        with open('./Login_KYC.json', 'r') as file:
            data = json.load(file)
            data[0]["certificate_of_incorporation"] = result

        with open("./Login_KYC.json", "w") as json_file:
            json.dump(data, json_file, indent=2)

        url = f"{url_path}/api/Kyc/UploadKYCFile?tag=incorporation_document"

        with open(r'C:/Users/Administrator/Pictures/Untitled.png', 'rb') as file:
            files = {'file': file}
            authorization = kyc_data['Autho']

            headers = {
                "Authorization": f"Bearer {authorization}",
            }

            response = requests.post(url, files=files, headers=headers)
            result = response.json()

            with open('./Login_KYC.json', 'r') as file:
                data = json.load(file)
                data[0]["incorporation_document"] = result

            with open("./Login_KYC.json", "w") as json_file:
                json.dump(data, json_file, indent=2)

            url = f"{url_path}/api/Kyc/UpdateActivateAccountTableToDb?name=About_Business&isValid=false"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }
            certificate_of_incorporation = kyc_data['certificate_of_incorporation']
            incorporation_document = kyc_data['incorporation_document']
            ownership_tree = kyc_data['ownership_tree']
            print(type(ownership_tree))

            payload = {
                "funds_source": [
                    "Ongoing business activity"
                ],
                "funds_source_other": "",
                "banks_work_today": [
                    "Union"
                ],
                "money_laundering": "0",
                "state_incorporation": "Israel",
                "business_name": "fgsagd",
                "business_number": "321312",
                "certificate_of_incorporation": certificate_of_incorporation,
                "date_incorporation": "2020-02-03T22:00:00.000Z",
                "business_type": "Private",
                "company_website": "",
                "business_category": "Business Support & Supplies",
                "business_subcategory": "Consultants",
                "business_subcategory_free_text": "",
                "has_diamond_member_certificate": "",
                "upload_diamond_certificate": "",
                "report_diamond_reports": "",
                "sure_not_fake_diamonds": "",
                "your_product": "fasdf",
                "business_address": "gfdagadfg",
                "business_zipcode": "432434",
                "business_email": "424@fdsf.com",
                "any_cryptocurrency_activities": "0",
                "any_gambling_activities": "0",
                "purpose_of_joining_company": [
                    "Preservation of money value"
                ],
                "purpose_of_joining_company_other": "",
                "exposure_to_foreign_currency": {
                    "currencies": [
                        "USD"
                    ],
                    "currency_groups": {
                        "USD": {
                            "estimated_yearly_holdings": "10000"
                        }
                    }
                },
                "get_excess_return_from_foreign_exchange_over_banks_return": "0",
                "interested_receiving_speculative_investment": "0",
                "incorporation_document": incorporation_document,
                "ownership_tree": ownership_tree,
                "face_recognition": "1"
            }
            response = requests.post(url, json=payload, headers=headers)

            print(response)

            url = f"{url_path}/api/Kyc/GetProgressStatus"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }

            response = requests.get(url,headers=headers)
            print(response.json())

            url = f"{url_path}/api/Kyc/UpdateActivateAccountTableToDb?name=System_Activity&isValid=true"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }
            payload={
                      "product_interest": [
                        "Receive funds"
                      ],
                      "countries_funds_sent": [
                        "United States"
                      ],
                      "annual_activity": "10000",
                      "isEligible": {
                        "value": "false",
                        "option_1": "null",
                        "option_2": "null",
                        "option_3": "null",
                        "option_4": "null",
                        "option_5": "null",
                        "option_6": "null",
                        "option_7": "null",
                        "option_8": "null",
                        "option_9": "null",
                        "option_10": "null"
                      },
                      "face_recognition": "1"
                    }

            response = requests.post(url,json=payload,headers=headers)
            result = response.json()
            print(result)

            url = f"{url_path}/api/Kyc/GetProgressStatus"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }

            response = requests.get(url, headers=headers)
            print(response.json())

            url = f"{url_path}/api/Kyc/UpdateActivateAccountTableToDb?name=Private&isValid=false"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }
            payload = {
                  "role_in_company": {
                    "value": "CEO",
                    "other": "",
                    "power_of_attorney": ""
                  },
                  "country": "Israel",
                  "email": "nacik96482@visignal.com",
                  "phone": "534040500",
                  "full_name": "Pay MeRoy",
                  "date_of_birth": "1995-10-02T10:00:00.000Z",
                  "gender": "",
                  "identity": "238660955",
                  "identities": [
                    "Israel"
                  ],
                  "israel_affinity": "",
                  "israel_affinity_other": "",
                  "street_address": "blkabka",
                  "street_address_2": "",
                  "city": "Givatayim",
                  "zipcode": "1242341",
                  "years_involved_in_company": "8",
                  "criminal_record": "0",
                  "local_public_figure": "0",
                  "foreign_public_figure": "0",
                  "representative_acts_in_his_own_name": "1",
                  "face_recognition": "1"
                }

            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            print(result)

            url = f"{url_path}/api/Kyc/GetProgressStatus"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }

            response = requests.get(url, headers=headers)
            print(response.json())

            url = f"{url_path}/api/Kyc/UpdateActivateAccountTableToDb?name=Shareholders&isValid=true"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }
            payload = {
                  "number_of_owners": "0",
                  "person_or_company_1": {
                    "type": 1,
                    "choose_entity": "",
                    "company_name": "",
                    "incorporation_number": "",
                    "first_name": "",
                    "last_name": "",
                    "phone_code": "",
                    "phone_number": "",
                    "email": "",
                    "stake_in_company": "",
                    "date_of_birth": "",
                    "date_of_incorporation": "",
                    "id_issuing_country": "",
                    "id_type": "",
                    "identity": "",
                    "citizenship": [],
                    "proof_of_address_type": "",
                    "residential_address": "",
                    "address_1": "",
                    "address_2": "",
                    "city": "",
                    "zipcode": "",
                    "state": "",
                    "front_of_document": "",
                    "back_of_document": "",
                    "copy_of_certificate_of_incorporation": "",
                    "proof_of_address": "",
                    "company_draft": "",
                    "shareholders_structure": "",
                    "name_of_primary_shareholder": ""
                  },
                  "person_or_company_2": {
                    "type": 2,
                    "choose_entity": "",
                    "company_name": "",
                    "incorporation_number": "",
                    "first_name": "",
                    "last_name": "",
                    "phone_code": "",
                    "phone_number": "",
                    "email": "",
                    "stake_in_company": "",
                    "date_of_birth": "",
                    "date_of_incorporation": "",
                    "id_issuing_country": "",
                    "id_type": "",
                    "identity": "",
                    "citizenship": [],
                    "proof_of_address_type": "",
                    "residential_address": "",
                    "address_1": "",
                    "address_2": "",
                    "city": "",
                    "zipcode": "",
                    "state": "",
                    "front_of_document": "",
                    "back_of_document": "",
                    "copy_of_certificate_of_incorporation": "",
                    "proof_of_address": "",
                    "company_draft": "",
                    "shareholders_structure": "",
                    "name_of_primary_shareholder": ""
                  },
                  "person_or_company_3": {
                    "type": 3,
                    "choose_entity": "",
                    "company_name": "",
                    "incorporation_number": "",
                    "first_name": "",
                    "last_name": "",
                    "phone_code": "",
                    "phone_number": "",
                    "email": "",
                    "stake_in_company": "",
                    "date_of_birth": "",
                    "date_of_incorporation": "",
                    "id_issuing_country": "",
                    "id_type": "",
                    "identity": "",
                    "citizenship": [],
                    "proof_of_address_type": "",
                    "residential_address": "",
                    "address_1": "",
                    "address_2": "",
                    "city": "",
                    "zipcode": "",
                    "state": "",
                    "front_of_document": "",
                    "back_of_document": "",
                    "copy_of_certificate_of_incorporation": "",
                    "proof_of_address": "",
                    "company_draft": "",
                    "shareholders_structure": "",
                    "name_of_primary_shareholder": ""
                  },
                  "person_or_company_4": {
                    "type": 4,
                    "choose_entity": "",
                    "company_name": "",
                    "incorporation_number": "",
                    "first_name": "",
                    "last_name": "",
                    "phone_code": "",
                    "phone_number": "",
                    "email": "",
                    "stake_in_company": "",
                    "date_of_birth": "",
                    "date_of_incorporation": "",
                    "id_issuing_country": "",
                    "id_type": "",
                    "identity": "",
                    "citizenship": [],
                    "proof_of_address_type": "",
                    "residential_address": "",
                    "address_1": "",
                    "address_2": "",
                    "city": "",
                    "zipcode": "",
                    "state": "",
                    "front_of_document": "",
                    "back_of_document": "",
                    "copy_of_certificate_of_incorporation": "",
                    "proof_of_address": "",
                    "company_draft": "",
                    "shareholders_structure": "",
                    "name_of_primary_shareholder": ""
                  },
                  "representatives_politically_exposed": {
                    "value": "0",
                    "detail_their_names": ""
                  },
                  "actions_by_government_agencies_within_past_five_years": "0",
                  "face_recognition": "1"
                }
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            print(result)

            url = f"{url_path}/api/Kyc/GetProgressStatus"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }

            response = requests.get(url, headers=headers)
            print(response.json())

            # url = f"{url_path}/api/Kyc/UploadKYCFile"
            #
            # with open(r'C:/Users/Administrator/Pictures/Untitled.png', 'rb') as file:
            #     files = {'file': file}
            #     authorization = kyc_data['Autho']
            #
            #     headers = {
            #         "Authorization": f"Bearer {authorization}",
            #     }
            #
            #     # # Make a POST request
            #     response = requests.post(url, files=files, headers=headers)
            #     result = response.json()
            #     with open('./Login_KYC.json', 'r') as file:
            #         data = json.load(file)
            #         data[0]["signatureFileId"] = result
            #         print(data[0]["signatureFileId"])
            #
            #     with open("./Login_KYC.json", "w") as json_file:
            #         json.dump(data, json_file, indent=2)

            signatureFileId = str(upload_kyc_file(url_path,authorization))
            # signatureFileId = kyc_data["signatureFileId"]
            MarketingServicesFileId = str(upload_kyc_file(url_path,authorization))
            # MarketingServicesFileId =MarketingServicesFileId = kyc_data["MarketingServicesFileId"]
            ServicesFileId = str(upload_kyc_file(url_path,authorization))
            # ServicesFileId = kyc_data["ServicesFileId"]
            SystemFileId = str(upload_kyc_file(url_path,authorization))
            # SystemFileId = kyc_data["SystemFileId"]
            DisclosureFileId = str(upload_kyc_file(url_path,authorization))
            # DisclosureFileId = kyc_data["DisclosureFileId"]
            print(signatureFileId)
            print(MarketingServicesFileId)
            print(ServicesFileId)
            print(SystemFileId)
            print(DisclosureFileId)
            url = f"{url_path}/api/Kyc/UpdateActivateAccountTableToDb?name=Agree_Terms&isValid=false"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }
            payload ={
                  "frameworkInformationSystem": 'true',
                  "frameworkInformationSystemFileId":SystemFileId,
                  "receivingConnectionWithFinancialAssetServices": 'true',
                  "receivingConnectionWithFinancialAssetServicesFileId": ServicesFileId,
                  "receivingInvestmentMarketingServices": 'true',
                  "receivingInvestmentMarketingServicesFileId": MarketingServicesFileId,
                  "riskDisclosure": 'true',
                  "riskDisclosureFileId": DisclosureFileId,
                  "agreeToInformOnAnyChange": 'true',
                  "signature": 'true',
                  "signatureFileId": signatureFileId,
                  "face_recognition": "1"
                    }

            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            print(result)
            time.sleep(3)
            url = f"{url_path}/api/Kyc/GetProgressStatus"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }

            response = requests.get(url, headers=headers)
            print(response.json())

            url = f"{url_path}/api/Kyc/CompleteKyc"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {authorization}"
            }

            response = requests.post(url, headers=headers)
            result = response.json()
            print(response.status_code)



def upload_kyc_file(url_qa,authorization_temp):

    url_path = url_qa
    url = f"{url_path}/api/Kyc/UploadKYCFile"
    with open(r'C:/Users/Administrator/Pictures/Untitled.png', 'rb') as file:
        files = {'file': file}
        authorization = authorization_temp

        headers = {
            "Authorization": f"Bearer {authorization}",
        }

        response = requests.post(url, files=files, headers=headers)
        result = response.json()
        return result
