
from selenium.webdriver.common.by import By

from utilities.BaseClass import BaseClass

class LogingDetails(BaseClass):

    def __init__(self,driver):
        self.driver = driver
    userName = (By.NAME, "username")
    password = (By.NAME,"password")
    submitButton = (By.CLASS_NAME, "submit-btn")

    def UserName(self):
        return self.driver.find_element(*LogingDetails.userName)

    def Password(self):
        return self.driver.find_element(*LogingDetails.password)
    def SubmitButton(self):
        return self.driver.find_element(*LogingDetails.submitButton)






