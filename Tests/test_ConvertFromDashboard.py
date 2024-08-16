import re
import time
import pytest
import json
import asyncio

summery_list = []

@pytest.mark.regression
@pytest.mark.asyncio(scope='session')
@pytest.mark.qa

async def test_convert_from_dashboard(page,get_url):
    start = time.perf_counter()
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']

    async def on_response(response):
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
        await page.locator("//button/span[text()='Exchange']").click()
        await page.locator("//input[@formcontrolname='firstExchangeAmount']").type("100")
        await page.locator("//button[@class='swap-background']").click()
        await asyncio.sleep(2)
        exchange_rate = await page.locator("//span[starts-with(@class,'exchange-rates')]").inner_text()
        cleaned_exchange_rate = float(exchange_rate.replace("€1 = $", ""))
        print(cleaned_exchange_rate)
        await asyncio.sleep(2)
        await page.locator("//button[@class='pay-next-btn']").click()
        sell_amount = await page.locator("//li/span[contains(@class,'ng-star-inserted')]").nth(0).inner_text()
        clean_sell_amount = float(re.sub('[$,€₪ USD ER]', "", sell_amount))

        buy_amount = await page.locator("//li/span[contains(@class,'ng-star-inserted')]").nth(1).inner_text()
        clean_buy_amount = float(re.sub('[$,€₪ USD ER]', "", buy_amount))

        print(clean_buy_amount)
        print(clean_sell_amount)
        if round(clean_buy_amount, 2) - round(cleaned_exchange_rate * clean_sell_amount, 2) > 1.0:
            raise Exception("Wrong convert Calculation")
        await page.locator("//input[@type='checkbox']").check()
        await page.locator("//button[@class='confirm-exchange-btn']").click()
        await page.locator("//button[@class='close-btn']").click()

