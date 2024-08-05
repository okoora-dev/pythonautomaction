import json
import re
import time
import pytest
import asyncio

@pytest.mark.regression
@pytest.mark.asyncio(scope='session')
async def test_edit_beneficiary(page,get_url):
    start = time.perf_counter()
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']

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

        await page.locator("//div[@class='account-detail']/span[@class='holder-name ng-star-inserted' and text()='EEEE']").click()
        await asyncio.sleep(1)

        await page.locator("div[class='date-action'] span[class='mat-mdc-button-touch-target']").click()
        await page.locator("//span[text()='Edit']").click()
        await page.locator("//span[text()='Next']").click()
        await asyncio.sleep(1)
        await page.locator("(//span[@class='mdc-button__label'][normalize-space()='Next'])[2]").click()
        await page.locator("//span[text()='Make it now']").click()
        await page.locator("//span[text()='Continue ']").click()

