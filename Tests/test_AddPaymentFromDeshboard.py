import asyncio
import json
import time
import pytest
import re
from playwright.async_api import async_playwright, expect

@pytest.mark.regression
@pytest.mark.qa
@pytest.mark.asyncio(scope='session')
async def test_add_payment(page,get_url):
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

        await asyncio.sleep(5)
        await page.locator("//button[@id='calendarAddAction']").click()
        await page.locator("//button/span[text()='Payment']").click()

        await page.locator("//img[@alt='pay plus icon']").click()
        await asyncio.sleep(3)

