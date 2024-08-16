import asyncio
import json
import re
import time
import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.regression
@pytest.mark.asyncio(scope='session')
@pytest.mark.qa
async def test_add_money(page,get_url):
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']
    start = time.perf_counter()

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
        await page.get_by_text("Settings").click()
        await asyncio.sleep(3)
        await page.get_by_role("button", name="+ Add Money").click()
        await page.get_by_placeholder("10,000").fill("10000")
        await page.locator("//input[@id='goldTransfer']").click()
        await page.get_by_role("button", name="Next").click()
        await page.locator("span.switch").nth(0).click()
        await asyncio.sleep(2)
        await page.locator("//span[contains(text(),'10,000.00')]").click()
        await asyncio.sleep(1)
        await page.locator("//span[contains(text(),'10,000.00')]").nth(1).click()
        flow_result = await page.locator("//div/h2[text()='Sent Successfully']").inner_text()

        assert flow_result == "Sent Successfully"

        await page.get_by_role("button", name=" Close ").click()
