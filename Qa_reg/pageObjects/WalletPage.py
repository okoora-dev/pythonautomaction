from selenium.webdriver.common.by import By



class GetWalletPage:
    def __init__(self,driver):
        self.driver = driver

    contactMenu = (By.XPATH, "(//span[normalize-space()='Accounts'])[1]")
    currentBalance = (By.XPATH, "(//p[@id='wallet-price'])[1]")
    contactMenu = (By.XPATH, "(//span[@class='menu-name'])[1]")
    addContact = (By.XPATH, "(//button[@class='add-contact'])[2]")
    addPaymentManual = (By.XPATH, "(//p[normalize-space()='Create payment manually'])[1]")
    sendNow = (By.XPATH,"(//p[normalize-space()='Send now'])[1]")
    continueButton = (By.XPATH, "(//span[@class='mdc-button__label'])[1]")
    selectBeneficiary = (By.XPATH, "(//div[@class='mat-mdc-select-arrow-wrapper ng-tns-c81-67'])[1]")
    searchBeneficiary = (By.CSS_SELECTOR, "input[placeholder='Search']")
    clickSelected = (By.XPATH, "(//mat-option[@role='option'])[1]")
    letsContinue = (By.XPATH,"//span[contains(text(),'Let’s continue ')]")
    beneficiaryAmount = (By.ID, "beneficiaryAmount-field")
    feeText = (By.CSS_SELECTOR, "span[class='regular-text ng-star-inserted'] span")
    checkBox = (By.XPATH, "(//div[@class='mdc-checkbox'])[1]")
    confirmButton = (By.XPATH, "(//span[@class='mdc-button__label'])[2]")
    confirmSelectCheckBox = (By.XPATH, "(//div[@class='mdc-checkbox'])[2]")
    sendPaymentButton = (By.XPATH, "(//span[@class='mdc-button__label'])[3]")
    confirmPaymentText = (By.XPATH, "//h6[normalize-space()='You have sent a payment of']")
    backToMainPage = (By.CLASS_NAME, "form-link")
    tempBalance = (By.XPATH, "(//p[@id='wallet-price'])[1]")
    contactMenu = (By.XPATH, "(//span[normalize-space()='Accounts'])[1]")
    dashboard = (By.XPATH,"(//span[normalize-space()='Dashboard'])[1]")
    clickchoice = (By.XPATH, "(//div[@class='calender-header-right'])[1]")
    payment = ((By.XPATH,"(//span[@class='mdc-list-item__primary-text'][normalize-space()='Payment'])[1]"))

    def GetContactPage(self):
        return self.driver.find_element(*GetWalletPage.contactMenu)

    def CurrentBalance(self):
        return self.driver.find_element(*GetWalletPage.currentBalance)

    def GetWalletPage(self):
        return self.driver.find_element(*GetWalletPage.contactMenu)
    def GetWalletPage(self):
        return self.driver.find_element(*GetWalletPage.contactMenu)

    def MenueContact(self):
        return self.driver.find_element(*GetWalletPage.addContact)
    def ManualPayment(self):
        return self.driver.find_element(*GetWalletPage.addPaymentManual)

    def SendNowArea(self):
        return self.driver.find_element(*GetWalletPage.sendNow)

    def ContinueButton(self):
        return self.driver.find_element(*GetWalletPage.continueButton)

    def SelectBeneficiary(self):
        return self.driver.find_element(*GetWalletPage.selectBeneficiary)

    def SearchBeneficiary(self):
        return self.driver.find_element(*GetWalletPage.searchBeneficiary)

    def ClickSelected(self):
        return self.driver.find_element(*GetWalletPage.clickSelected)

    def LetsContinue(self):
        return self.driver.find_element(*GetWalletPage.letsContinue)

    def BeneficiaryAmount(self):
        return self.driver.find_element(*GetWalletPage.beneficiaryAmount)

    def FeeText(self):
        return self.driver.find_element(*GetWalletPage.feeText)

    def CheckBox(self):
        return self.driver.find_element(*GetWalletPage.checkBox)

    def ConfirmButton(self):
        return self.driver.find_element(*GetWalletPage.confirmButton)

    def ConfirmSelectCheckBox(self):
        return self.driver.find_element(*GetWalletPage.confirmSelectCheckBox)

    def SendPaymentButton(self):
        return self.driver.find_element(*GetWalletPage.sendPaymentButton)

    def ConfirmPaymentText(self):
        return self.driver.find_element(*GetWalletPage.confirmPaymentText)

    def BackToMainPage(self):
        return self.driver.find_element(*GetWalletPage.backToMainPage)

    def TempBalance(self):
        return self.driver.find_element(*GetWalletPage.tempBalance)

    def Dashboard(self):
        return self.driver.find_element(*GetWalletPage.dashboard)

    def ClickChoice(self):
        return self.driver.find_element(*GetWalletPage.clickchoice)

    def Payment(self):
        return self.driver.find_element(*GetWalletPage.payment)
