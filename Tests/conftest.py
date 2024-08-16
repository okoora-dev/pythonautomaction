import json
import time
import asyncio
from datetime import datetime
import asyncio
from playwright.async_api import async_playwright
import pytest
import os
import glob

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from utilities.DB import TestSqlQuery
from utilities.email_pytest_report import Email_Pytest_Report

driver = None

TEST_NAME = ""


# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()

@pytest.fixture(scope="session")
async def page():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
            slow_mo=50,
            args=["--start-maximized"],
        )
        context = await browser.new_context(no_viewport=True)
        await context.tracing.start(
            name="playwright",
            screenshots=True,
            snapshots=True,
            sources=True,
        )
        page = await context.new_page()
        yield page
        # await context.tracing.stop(path=f"./traces/playwright.zip")
        await context.close()
        await browser.close()




def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test to be run by asyncio")

@pytest.fixture()
def todayAt(hr, min=0, sec=0, micros=0):
    now = datetime.now()
    return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)


def pytest_runtest_setup(item):
    global TEST_NAME
    TEST_NAME = str(item.name)



def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="http://localhost", help="Base URL for the application")

@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture(scope='class')
def get_url(base_url):
    if base_url == 'qa':
        return {"url":"https://okoora-qa-front2023.azurewebsites.net/login","mail":"jipop81748@in2reach.com","password":"Okoora2!","user_id":"a11103d7-51c3-458a-ae24-775858544a97",
                "db_schem":"ofakimdb"}
    else:
        return {"mail": "feteb17715@randrai.com", "password": "Okoora1!","user_id":"defddb4a-a050-4afd-bebc-2bb7cfd7a6a3",
                "url": "https://demo2.okoora.com/login/","db_schem":"ofakimdb_Copy"}


# @pytest.fixture(scope="class")
# def setup(request):
#     global driver
#     options = webdriver.ChromeOptions()
#     # options.add_argument("headless")
#     options.add_experimental_option("detach", True)
#     chromepath = Service("C:/chromedriver.exe")
#     driver = webdriver.Chrome(service=chromepath, options=options)
#
#     driver.implicitly_wait(15)
#
#     driver.maximize_window()
#     time.sleep(2)
#     # driver.get("https://okoora-qa-front2023.azurewebsites.net/")
#     request.cls.driver = driver
#     yield
#     # driver.close()



@pytest.fixture()
def email_pytest_report(request):
    "pytest fixture for device flag"
    return request.config.getoption("--email_pytest_report")


@pytest.fixture(scope="function")
def set_download_path():
    new_folder_path = r'C:\Users\Administrator\Downloads'
    pattern = os.path.join(new_folder_path, '*.xlsx')

    xls_files = glob.glob(pattern)

    for file in xls_files:
        os.remove(file)
        print(f"Deleted: {file}")

    return new_folder_path  # Now, any file you download using Python will be saved in this new folder







def pytest_addoption(parser):
    parser.addoption("--db-name", action="store", help="Database name")


def pytest_terminal_summary():

    "add additional section in terminal summary reporting."
    # if not hasattr(terminalreporter.config, 'workerinput'):
    #     if terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
    report_file_path = 'C:/Users/Administrator/Automation/Tests/GUI.html'
    email_obj = Email_Pytest_Report()
    # Send html formatted email body message with pytest report as an attachment
    email_obj.send_test_report_email(html_body_flag=True, attachment_flag=True, report_file_path=report_file_path)

def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)




@pytest.fixture()
def get_user_data():
    with open("user_data.json", "r") as file:
        data = json.load(file)
        return data


@pytest.fixture(scope='session')
def conn_str(request):
    database = request.config.getoption("--db-name")
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=ofakimdev-dbsrv.database.windows.net;"
        f"DATABASE={database};"
        "UID=dbadmin;"
        "PWD=Mq#86Eyq!D"
    )
    return conn_str

@pytest.fixture(scope='session')
def sql_query(conn_str):
    return TestSqlQuery(conn_str)
