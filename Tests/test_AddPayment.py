import json
import time
import pytest
import re
import asyncio


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
        await page.locator("(//a[@class='sidebar-item ng-star-inserted active'])[1]").click()
        balance_temp = await page.locator("//div[@class='wallet-amount']").inner_text()
        balance_before = re.sub('[$,€₪ USD ER]', "", balance_temp)
        print(float(balance_before))
        await asyncio.sleep(1)
        await page.locator("//span[@class='sidebar-name'][text() = 'Payments']").click()
        await page.locator("//img[@alt='pay plus icon']").click()
        await page.locator("//span[text() = ' Single Payment ']").click()
        await asyncio.sleep(3)
        await page.locator("//input[@id='beneficiaryInput']").click()
        await page.locator("//input[@id='beneficiaryInput']").type("Test USD")
        await page.locator("//div/p[text() =' Test USD']").click()
        await asyncio.sleep(2)
        await page.locator("//button[contains(@class ,'clickedSelect')]").click()
        await page.locator("(//input[@placeholder='0'])[1]").click()
        await asyncio.sleep(1)
        await page.locator("(//input[@placeholder='0'])[1]").type("100")

        await page.locator("//button[@class ='pay-next-btn']").dblclick(delay=2000)

        await asyncio.sleep(1)
        await page.locator("//div/textarea").fill("This is A test")
        await page.get_by_role("button", name="Next").click()
        await asyncio.sleep(1)
        temp_amount = await page.locator("//li[2]//strong[1]").inner_text()
        amount = re.sub('[$,€₪ USD ER]', "", temp_amount)
        print(float(amount))
        await page.locator("//input[@class='mdc-radio__native-control']").nth(0).check()
        fee = await page.locator("//div[@class='transfer-fee-wrap']/strong").nth(0).inner_text()
        new_fee = re.sub('[$,€₪ USD ER]', "", fee)
        print(float(new_fee))
        await page.locator("//input[@type='checkbox']").check()

        await page.locator("//button[starts-with(text(),' Pay')]").click()
        await page.reload()
        balance_temp = await page.locator("//div[@class='wallet-amount']").inner_text()
        balance_after = re.sub('[$,€₪ USD ER]', "", balance_temp)
        print(float(balance_after))
        delta_wallet = round(float(balance_before) - float(balance_after), 2)
        payed_amount = round(float(new_fee) + float(amount),2)
        assert delta_wallet - payed_amount == 0.0

