import time
from utilities.email_pytest_report import Email_Pytest_Report
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pytest
from pytest import fixture
import json
from datetime import datetime, timedelta
import os

GLOBAL_PATH = "data.json"
MANAGER_PATH = "MenagerData.json"
KYC_PATH = "Login_KYC.json"
def load_json(path):
    with open(path) as data_file:
        data = json.load(data_file)
        return data


@fixture(params=load_json(GLOBAL_PATH))
def data_test(request):
    my_data = request.param
    return my_data

@fixture(params=load_json(MANAGER_PATH))
def manager_data_test(request):
    my_data = request.param
    return my_data

@fixture(params=load_json(KYC_PATH))
def kyc_data(request):
    my_data = request.param
    return my_data

@fixture()
def get_tomorrow_date():
    today = datetime.now()

    # Calculate tomorrow's date
    tomorrow = today + timedelta(days=2)
    # Format tomorrow's date in dd/mm/YYYY
    tomorrow_formatted = tomorrow.strftime('%d/%m/%Y')
    return tomorrow_formatted


@fixture()
def get_six_month_date():
    today = datetime.now()

    # Calculate tomorrow's date
    tomorrow = today + timedelta(days=180)
    # Format tomorrow's date in dd/mm/YYYY
    six_month = tomorrow.strftime('%d/%m/%Y')
    return six_month


@fixture()
def end_the_year():
    # Get the current year
    current_year = datetime.now().year

    # Since we want to find the end date of the current year, it would be December 31st of the current year
    end_of_year_date = datetime(current_year, 12, 31)
    end_year_date = end_of_year_date.strftime("%d/%m/%Y")

    return end_year_date

