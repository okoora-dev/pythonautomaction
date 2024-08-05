import asyncio
import datetime
import json
import pytest

@pytest.mark.asyncio(scope='session')
@pytest.mark.regression
async def test_travel_cash(page, get_url):
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']

    def todayAt(hr, min=0, sec=0, micros=0):
        now = datetime.datetime.now()
        return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)

    timeNow = datetime.datetime.now()
    if timeNow > todayAt(16):
        pytest.skip("Skipping Cash Travel test the time is after 16:00")

    async def on_chooser(file_chooser):
        await file_chooser.set_files("Upload.pdf")
        print("File uploaded")

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
        page.on("filechooser", on_chooser)
        page.on("response", on_response)
        page.on("load", on_load)

        await page.goto(url, wait_until="load")
        await page.locator("//input[@name='username']").type(user_mail)
        await page.locator("//input[@name='password']").fill(password)
        await page.get_by_role("button", name="Log In ").click()
        await page.get_by_text("Travel Cash").click()
        await page.wait_for_timeout(2000)
        await page.locator("//mat-datepicker-toggle[@id='datepicker-toggle-id']").click()
        await page.locator("//span[contains(@class,'mat-calendar-body-today')]").click()
        await page.locator("//input[@id= 'amountIdTCF']").type("100")
        await page.get_by_role("button", name=" Next ").click()
        await page.locator("//input[@id='hebrewNamecTof']").type("אטוטמציה")
        await page.locator("//input[@id='idNumbercTof']").type("999999998")
        await page.locator("//input[@id='englishFirstNamecTof']").type("Automation Test")
        await page.locator("//input[@id='englishLastNamecTof']").type("Python")
        await page.locator("//input[@id='mobileNcTof']").type("0531231234")
        await page.locator("//input[@id='emailIdcTof']").type("auto@gmai.com")
        await page.locator("//button[@id='nextBtnStep2CtoF']").click()
        await page.locator("//span").get_by_text("Confirm & order ").click()
        await page.get_by_role("link", name="Back to my wallet").click()
