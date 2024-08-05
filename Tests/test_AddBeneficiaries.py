import asyncio
import json
import time
import pytest
from playwright.async_api import async_playwright, expect

country_list = []


@pytest.mark.regression
@pytest.mark.qa
@pytest.mark.asyncio(scope='session')
async def test_add_beneficiary(page,get_url, sql_query):
    user_data = get_url
    print(user_data)
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']
    start = time.perf_counter()
    user = 'auto@auto.com'
    status = sql_query.delete(user)
    assert "executed" in status

    async def on_response(response):
        try:
            if "BalanceList" in response.url:
                print("Waiting for response...")
                result = await asyncio.wait_for(response.json(), timeout=5.0)
                print("Response received.")
        except asyncio.TimeoutError:
            print("Response took more than 5 seconds.")
        if response.status != 200:
            if response.status == 500:
                result = await response.json()
                raise Exception(response.url, response.status, json.dumps(result, indent=2))
            result = await response.json()
            print(response.url, response.status, json.dumps(result, indent=2))

    async def on_load(load):
        print(load)

    async for page in page:
        await page.goto(url)
        page.on("response", on_response)
        page.on("load", on_load)

        await page.goto(url, wait_until="load")
        await page.locator("//input[@name='username']").type(user_mail)
        await page.locator("//input[@name='password']").fill(password)
        await page.get_by_role("button", name="Log In ").click()

        await page.locator("(//span[normalize-space()='Contacts'])[1]").click()

        await asyncio.sleep(1)
        await page.locator("(//span[contains(text(),'Beneficiary')])[1]").click()
        await page.get_by_text(" Add new contact ").click()

        await page.locator("(//label[@for='beniciary'])[1]").click()
        await page.locator("(//span[@class='mdc-button__label'][normalize-space()='Next'])[1]").click()
        await asyncio.sleep(1)
        await page.locator(
            "(//button[@class='mat-stepper-next skip-btn mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base ng-star-inserted'])[1]").click()

        bankAccountHolderName = page.locator("//input[@id='bankAccountHolderName']")
        await bankAccountHolderName.click()
        await bankAccountHolderName.fill("Automation holder")
        bankAccountHolderEmail = page.locator("//input[@id='bankAccountHolderEmail']")
        await bankAccountHolderEmail.click()
        await bankAccountHolderEmail.fill("auto@auto.com")

        await asyncio.sleep(3)
        beneficiaryCountry = page.locator("//mat-select[@name='beneficiaryCountry']")
        await beneficiaryCountry.click()
        await asyncio.sleep(3)

        await page.locator("//span[text()='Israel ']").click()

        # await page.get_by_label("Bank account holder name (Hebrew only)").text_content()

        await page.locator("//input[@name='bankAccountHolderHebrewName']").fill("אוטומציה")
        await page.locator("//mat-select[@name='beneficiaryAccountType']").click()
        await asyncio.sleep(1)
        await page.locator("//span[text()='Company']").click()
        await asyncio.sleep(2)

        await page.locator("//mat-select[@name='beneficiaryState']").click()
        await page.locator("//span[text()='Central District']").click()
        await asyncio.sleep(1)
        await page.locator("//mat-select[@name='beneficiaryCity']").click()
        await asyncio.sleep(1)
        await page.locator("//span[text()='`Alma']").click()

        await page.locator("//input[@name='beneficiaryStreet']").fill("this my street")
        await page.locator("//input[@name='beneficiaryHouseNumber']").fill("01")
        await page.locator("//input[@name='beneficiaryZipCode']").fill("12345")
        await page.locator("//input[@name='beneficiaryIdNumber']").fill("133345679")
        await asyncio.sleep(2)
        await page.locator("(//button[@type='submit'])[4]").click()

        await page.locator("(//label[@for='swift'])[1]").click()

        await asyncio.sleep(1)
        input_swift = page.locator("//input[@id='swiftCode']")
        await asyncio.sleep(1)
        await input_swift.fill("POALILIT")

        await asyncio.sleep(1)
        bank_number = page.locator("//input[@id='bankNumber']")
        await bank_number.fill("122344")
        account_number = page.locator("//input[@id='accountNumber']")
        await account_number.fill("45454545")

        await page.locator("//mat-select[@name='currency']").click()
        await page.locator("//span[text()=' USD ']").click()
        next_button = page.locator("(//button[@type='submit'])[5]")
        await expect(next_button).to_be_visible()
        await page.locator("//mat-select[@name='currency']").click()
        await page.locator("//span[text()=' EUR ']").click()
        await next_button.click()

        await asyncio.sleep(1)

        await page.locator("(//label[@for='paymentOfService'])[1]").click()
        await asyncio.sleep(1)
        await page.get_by_placeholder("Select from list").click()
        await asyncio.sleep(1)
        await page.locator("//span[text()=' Third Party Transfer ']").click()
        await asyncio.sleep(1)
        await page.locator("(//span[normalize-space()='Make it now'])[1]").click()
        await page.locator("(//button[@type='submit'])[6]").click()
        await page.locator("(//a[normalize-space()='Back to my contacts'])[1]").click()

