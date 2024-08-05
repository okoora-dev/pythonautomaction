
import inspect
import logging

import re
import datetime

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

@pytest.mark.usefixtures("setup")
class BaseClass:

    def MoveByOffst(self):
        ActionChains(self.driver).move_by_offset(10, 10).click().perform()

    def MoveToElement(self,element):
        ActionChains(self.driver).move_to_element(element).perform()
    def ReformatCurrency(self,currency):
       return re.sub('[$₪€, EUR]', "", currency)


    def WaitUntilClickable(self,element):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))

    def WaitUntilPageLoaded(self,element):
        WebDriverWait(self.deiver, 10).until(EC.presence_of_element_located(element))

    #
    # def get_Logger(self):
    #     now = datetime.datetime.now()
    #     filename = now.strftime('regression_%H%M%d%m%Y.log')
    #     logName = inspect.stack()[1][3]
    #     logger = logging.getLogger(logName)
    #     FileHandler = logging.FileHandler(f'C:/Users/Administrator/Automation/utilities/Logs/{filename}')
    #     logger.addHandler(FileHandler)
    #     formatter = logging.Formatter('%(asctime)s %(levelname)s : %(name)-s :%(message)s')
    #     FileHandler.setFormatter(formatter)
    #     logger.setLevel(logging.INFO)
    #     return logger

    def todayAt(self,hr, min=0, sec=0, micros=0):
        now = datetime.datetime.now()
        return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)

