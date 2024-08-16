import asyncio
from playwright.async_api import async_playwright
import pytest
from utilities.DB import TestSqlQuery

hit_data = {
    "access_Token": "",
    "spot": 0.0,
    "exposureID": ""
}


@pytest.mark.regression
@pytest.mark.asyncio(scope='session')
async def test_hit_payment(page, get_url, sql_query):
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']

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

        if response.url == "https://okoora-demo-api2023.azurewebsites.net/api/Authentication/login":
            result = await response.json()
            hit_data['access_Token'] = str(result['accessToken'])
            print(hit_data['access_Token'])
        if response.url == "https://okoora-demo-api2023.azurewebsites.net/api/Rates/AlertSpotAndRate?pair=EURUSD&direction=2":
            temp_spot = await response.json()
            hit_data['spot'] = round(float(temp_spot), 2) + 0.01
            print(hit_data['spot'])
        if response.url == "https://okoora-demo-api2023.azurewebsites.net/api/Exposures/CreateExposure":
            exposureID_result = await response.json()
            hit_data['exposureID'] = exposureID_result['exposureID']
            print(hit_data['exposureID'])

    async def on_load(load):
        print(load)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}  # Maximize window size
        )
        page = await context.new_page()

        page.on("filechooser", on_chooser)
        page.on("response", on_response)
        page.on("load", on_load)

        await page.goto(url, wait_until="load")
        await page.locator("//input[@name='username']").type(user_mail)
        await page.locator("//input[@name='password']").fill(password)
        await page.get_by_role("button", name="Log In ").click()

        await page.locator("//span[text()='Payments']").click()
        await page.get_by_role("button", name="Exchange").click()
        await page.get_by_text("Future exchange").click()
        await page.locator("//button[@aria-label='Open calendar']").nth(1).click()
        await page.locator("button.mat-calendar-body-active").click()
        await page.get_by_text("Next").click()
        await asyncio.sleep(2)
        await page.locator("//mat-select[@name='currency']").nth(0).click()
        await page.locator("//span[text()=' EUR']").click()

        await page.locator("//input[@formcontrolname='buyAmount']").click()
        await page.locator("//input[@formcontrolname='buyAmount']").type("100")
        await page.keyboard.press('Tab')

        await asyncio.sleep(2)

        await page.locator("//input[@formcontrolname='spotRate']").click()
        await page.locator("//input[@formcontrolname='spotRate']").fill(str(hit_data['spot']))
        await asyncio.sleep(2)
        await page.locator("//input[@id='termsCondition-checkbox-input']").click()
        await page.locator("//label[@for='mat-mdc-checkbox-3-input']").click()
        await page.locator("//button[@id='nextBtn']").click()
        await asyncio.sleep(2)
        await run(playwright)
        sql = sql_query
        raw_num = sql.check_status(str(hit_data['exposureID']))
        assert raw_num == 1



async def run(playwright):
    global hit_data
    api_context = await playwright.request.new_context(
        base_url="https://okoora-demo-api2023.azurewebsites.net/api/",
        extra_http_headers={
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {hit_data['access_Token']}"
        }
    )

    target_rate = float(hit_data['spot']) - 0.3
    url = f"Exposures/UpdateExposureTarget?exposureId={hit_data['exposureID']}&newTargetRate={target_rate}"
    print(f"Request URL: {url}")
    print(f"Authorization Token: {hit_data['access_Token']}")

    response = await api_context.post(url)
    assert response.status == 200
    print(f"Response Status: {response.status}")
    response_text = await response.text()
    print(f"Response Text: {response_text}")

    await asyncio.sleep(5)
