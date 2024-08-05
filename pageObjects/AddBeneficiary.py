from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


class GetBeneficiary:
    def __init__(self,driver):
        self.driver = driver
        self.action = ActionChains
    contactsMenu = (By.XPATH, "(//span[normalize-space()='Contacts'])[1]")
    beneficiaries = (By.CLASS_NAME,"mdc-tab__text-label")
    selectBeneficiaries = (By.XPATH,"(//span[contains(text(),'Beneficiaries')])[1]")
    addContact = (By.CLASS_NAME,"add-contact")
    boxes = (By.CLASS_NAME,"box-radio")
    moveToBeneficiaries = (By.XPATH,"(//p[normalize-space()='Beneficiaries'])[1]")
    nextButton = (By.XPATH,"(//span[@class='mat-mdc-button-touch-target'])[5]")

    def ContactsMenu(self):
        return self.driver.find_element(*GetBeneficiary.contactsMenu)

    def Beneficiaries(self):
        return self.driver.find_element(*GetBeneficiary.beneficiaries)

    def SelectBeneficiaries(self):
        return self.driver.find_element(*GetBeneficiary.selectBeneficiaries)

    def AddContact(self):
        return self.driver.find_element(*GetBeneficiary.addContact)

    def Boxes(self):
        return self.driver.find_element(*GetBeneficiary.boxes)

    def MoveToBeneficiaries(self):
        return self.driver.find_element(*GetBeneficiary.moveToBeneficiaries)

    def NextButton(self):
        return self.driver.find_element(*GetBeneficiary.nextButton)

