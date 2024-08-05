from selenium.webdriver.common.by import By



class GetConvertFlow:
    def __init__(self,driver):
        self.driver = driver

    contactMenu = (By.XPATH, "(//span[normalize-space()='Accounts'])[1]")
    chargedWallet = (By.XPATH , "//div[@class='wallet-amount']")
    convertButtonName = (By.XPATH,"(//button[normalize-space()='Convert'])[1]")
    convertMoney = (By.XPATH,"(//h5[normalize-space()='Convert Money'])[1]")
    convertNowArea = (By.XPATH,"(//p[normalize-space()='Now'])[1]")
    makeItNowButton = (By.XPATH,"(//div[@class='stepper-action'])[1]")
    requestConvertAmountField = (By.CSS_SELECTOR,"input[class='disabled ng-untouched ng-pristine ng-valid ng-star-inserted']")
    countryDropDown = (By.XPATH,"(//div[@class='country-dropdown ng-star-inserted'])[1]")
    countries = (By.CLASS_NAME,"mdc-list-item__primary-text")
    convertButton = (By.XPATH,"(//button[@class='next-button mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base'])[1]")
    summary = (By.CLASS_NAME, "(//div[@class='summary-iteam'])/span[contains(@class,'value')]")
    summaryValue = (By.CLASS_NAME, "summary-iteam")
    checkBox = (By.CLASS_NAME,"mdc-checkbox")
    summaryButton = (By.CSS_SELECTOR , "div[class='stepper-body conver-first-step covert-summary-step-sec loader-wrapper'] button[class='next-button mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base']")
    summaryMessage = (By.XPATH,"(//p[@class='form-description ng-star-inserted'])[1]")
    backToWallet = (By.CLASS_NAME,"form-link")
    totalBalance = (By.XPATH, "(//p[@id='totalBalance-value'])[1]")
    dashboard = (By.XPATH,"(//span[normalize-space()='Dashboard'])[1]")
    clickchoice = (By.XPATH, "(//div[@class='calender-header-right'])[1]")
    convert = ((By.XPATH,"(//span[@class='mdc-list-item__primary-text'][normalize-space()='Convert'])[1]"))
    def GetContactPage(self):
        return self.driver.find_element(*GetConvertFlow.contactMenu)

    def ChargedWallet(self):
        return self.driver.find_element(*GetConvertFlow.chargedWallet)

    def ConvertButtonName(self):
        return self.driver.find_element(*GetConvertFlow.convertButtonName)

    def ConvertMoney(self):
        return self.driver.find_element(*GetConvertFlow.convertMoney)

    def ConvertNowArea(self):
        return self.driver.find_element(*GetConvertFlow.convertNowArea)

    def MakeItNowButton(self):
        return self.driver.find_element(*GetConvertFlow.makeItNowButton)

    def CountryDropDown(self):
        return self.driver.find_element(*GetConvertFlow.countryDropDown)

    def RequestConvertAmountField(self):
        return self.driver.find_element(*GetConvertFlow.requestConvertAmountField)

    def Countries(self):
        return self.driver.find_elements(*GetConvertFlow.countries)

    def ConvertButton(self):
        return self.driver.find_element(*GetConvertFlow.convertButton)

    def Summary(self):
        return self.driver.find_elements(*GetConvertFlow.summary)

    def SummaryValue(self):
        return self.driver.find_elements(*GetConvertFlow.summaryValue)

    def CheckBox(self):
        return self.driver.find_element(*GetConvertFlow.checkBox)

    def SummaryButton(self):
        return self.driver.find_element(*GetConvertFlow.summaryButton)

    def SummaryMessage(self):
        return self.driver.find_element(*GetConvertFlow.summaryMessage)

    def BackToWallet(self):
        return self.driver.find_element(*GetConvertFlow.backToWallet)

    def TotalBalance(self):
        return self.driver.find_element(*GetConvertFlow.totalBalance)

    def Dashboard(self):
        return self.driver.find_element(*GetConvertFlow.dashboard)

    def ClickChoice(self):
        return self.driver.find_element(*GetConvertFlow.clickchoice)

    def Convert(self):
        return self.driver.find_element(*GetConvertFlow.convert)