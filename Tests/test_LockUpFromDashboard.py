import json
import re
import time
from datetime import date
import pytest
import asyncio
from playwright.async_api import async_playwright


@pytest.mark.regression
@pytest.mark.asyncio(scope='session')
async def test_LockUp_from_Dash(page,get_url):
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']
    start = time.perf_counter()

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
        await asyncio.sleep(1)

        await asyncio.sleep(5)
        wallet_amount = await page.locator("//mat-list-option[@id='wallet-ILS']//p[@id='wallet-price']").inner_text()
        print(wallet_amount)
        current_amount_wallet = float(re.sub('[$₪,]', "", wallet_amount))
        print(current_amount_wallet)

        await page.locator("(//span[contains(text(),'Lock & Up')])[1]").click()
        await asyncio.sleep(1)

        await page.locator("//div/span[contains(@class,'ng-tns') and contains(text(),'Select time frame')]").click()
        await page.locator("//span[text()='1 Month']").click()
        await page.locator("//button[text()='Execute']").click()
        await page.locator("//input[@type='checkbox']").click()
        await page.locator("//button[@class='continue']").click()
        await page.locator("//input[starts-with(@class,'pd-left-icon')]").fill('100')
        await page.locator("//input[@class='disable-input']").click()
        await asyncio.sleep(1)
        await page.locator("//div[@class='lock-up-popup-btn-group']/button[text()='Continue']").click()
        amount_to_charge = await page.locator("div[class='box-approval'] div:nth-child(5) span:nth-child(2)").inner_text()
        clean_amount = float(re.sub('[$₪,]', "", amount_to_charge))
        print(clean_amount)
        await page.locator("//input[@type='checkbox' and @id='apf-conf-check-input']").click()
        await page.locator("//button[text()='המשך']").click()
        await page.locator("//*[@id='mat-mdc-dialog-2']/div/div/app-calling-modal/div/div/div[1]/div/div/shared-purchase-success/div/div[6]/a").click()

        await page.locator("//span[text()='Dashboard']").click()
        await page.reload()
        await asyncio.sleep(1)
        await page.locator("//span[text()='Dashboard']").click()
        amount_after = await page.locator("//mat-list-option[@id='wallet-ILS']//p[@id='wallet-price']").inner_text()
        new_wallet = float(re.sub('[$₪,]', "", amount_after))
        result = round(float(current_amount_wallet) - float(new_wallet), 2)
        try:
            assert clean_amount == result
        except:
            raise Exception("User was not charged")

