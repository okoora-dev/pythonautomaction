import asyncio
import json
import pytest

@pytest.mark.regression
@pytest.mark.asyncio(scope='session')

async def test_action_user_role(page, get_url):
    user_enter_detail = {"manager_mail": "tiwoti5085@meogl.com", "manager_password": "Okoora1!"}
    user_data = get_url
    url = user_data['url']
    user_mail = user_enter_detail['manager_mail']
    password = user_enter_detail['manager_password']

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
                result =  response.json()
                raise Exception(response.url, response.status, json.dumps(result, indent=2))
            result =  response.json()
            print(response.url, response.status, json.dumps(result, indent=2))

    # Set up event handlers
    # page.on("response", on_response)
    async for page in page:
        page.on("response", on_response)
        await page.goto(url)
# await page.goto(url)
        await page.locator("//input[@name='username']").type(user_mail)
        await page.locator("//input[@name='password']").fill(password)
        await page.get_by_role("button", name="Log In ").click()

        await asyncio.sleep(5)
        menu = page.locator("//button[@id='calendarAddAction']")
        await menu.click()
        assert await page.is_disabled("//button/span[text()='Exchange']")
        assert await page.is_disabled("//button/span[text()='Hedge']")
        await page.keyboard.down("Escape")

        await page.locator("//a[text()='View all']").nth(3).click()
        await page.locator("//span[text()='Exchange']").click()
        assert await page.get_by_role("button", name="+ New Exchange").is_disabled()

        await page.locator("//span[text()='Hedging']").click()
        assert await page.get_by_role("button", name="+ New Hedge").is_disabled()
