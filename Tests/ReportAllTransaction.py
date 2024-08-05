import os
import time
import glob
import pytest
from selenium.webdriver.common.by import By
from TestData.LoginData import LoginDataTest
from pageObjects.Login import LogingDetails
from utilities.BaseClass import BaseClass


@pytest.mark.usefixtures("setup")
@pytest.mark.regression
class TestReportAllTrans(BaseClass):
    def test_ReportAllTransaction(self, GetData,set_download_path):
        PATH = set_download_path
        login_page = LogingDetails(self.driver)
        login_page.UserName().send_keys(GetData["mail"])
        login_page.Password().send_keys(GetData["password"])
        login_page.SubmitButton().click()
        self.driver.maximize_window()
        time.sleep(5)

        self.driver.find_element(By.XPATH, "//span[text()='Reports']").click()
        # self.driver.find_element(By.ID, "Account-Reports-Business-link").click()
        # self.driver.find_element(By.XPATH, "//label[@for='allTransaction']").click()
        self.driver.find_element(By.ID,"all-transactions-link").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH,"//span[@class='xlsx-tag']").click()
        time.sleep(5)

        assert  self.xlsx_exists(PATH)
        #     print("At least one .xlsx file exists in the folder.")
        # else:
        #     print("No .xlsx files found in the folder.")

    def xlsx_exists(self,folder_path):
        # Create a pattern to match all .xlsx files
        pattern = os.path.join(folder_path, '*.xlsx')

        # Find all .xlsx files in the folder
        xlsx_files = glob.glob(pattern)

        # Return True if any .xlsx files are found, False otherwise
        return len(xlsx_files) > 0




    @pytest.fixture(params=LoginDataTest.LoginData)
    def GetData(self, request):
        return request.param
