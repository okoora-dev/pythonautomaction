import time
from pytest import fixture
import json
from datetime import datetime, timedelta
import pytest

PATH = "Api_data.json"


@pytest.fixture()
def load_json():
    with open(r"C:\Users\Administrator\Automation\Okoora_Api\Api_data.json") as data_file:
        data = json.load(data_file)
        return data


def data_test(request):
    my_data = request.param
    return my_data


@pytest.fixture()
def get_path():
    return "https://okoora-web-api-stage.azurewebsites.net"


@pytest.fixture()
def get_beneficiary(load_json):
    beneficiary = load_json['beneficiaryId']
    return beneficiary


@pytest.fixture()
def get_header_data(load_json):
    data_params = load_json
    request_id = data_params['request_id']
    account_id = data_params['accountId']

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Api-Key": request_id,
        "X-Client-Id": account_id
    }
    return headers

@pytest.fixture()
def get_header_upload_file(load_json):
    data_params = load_json
    request_id = data_params['request_id']
    # account_id = data_params['accountId']
    form_data = {
        'Accept': "application/json",
        'Content-Type': 'application/json',
        "X-Api-Key": request_id,
        "X-Client-Id": "b595f697-14fc-4ba7-9091-039254bd41f8"
    }
    return form_data

def pytest_addoption(parser):
    parser.addoption("--db-name", action="store", default="default_db", help="Database name for testing")

@pytest.fixture(scope='session')
def db_name(request):
    return request.config.getoption("--db-name")