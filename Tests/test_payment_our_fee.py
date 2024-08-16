import asyncio
import json
import time
import pytest
import re

@pytest.mark.asyncio(scope='session')
@pytest.mark.regression
async def test_add_Paymnet_our_fee(page, sql_query, get_url):
    user_data = get_url
    user_id = user_data["user_id"]
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']
    sql = sql_query
    sql.add_free_fee(user_id)
    sql.change_outgoing_payments(user_id)
    sql.reset_outgoing_payments(user_id)
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

    async def on_chooser(file_chooser):
        await file_chooser.set_files("Upload.pdf")
        print("File uploaded")

    async def on_load(load):
        print(load)

    async for page in page:
        await page.goto(url)
        page.on("response", on_response)
        page.on("load", on_load)
        page.on("filechooser", on_chooser)

        await page.goto(url, wait_until="load")
        await page.locator("//input[@name='username']").type(user_mail)
        await page.locator("//input[@name='password']").fill(password)
        await page.get_by_role("button", name="Log In ").click()

        await page.wait_for_timeout(5000)

        await page.locator("//span[text()='Payments']").click()
        await page.locator("//button[starts-with(@class,'wallet-list-btn')]").click()
        await page.locator("//span/span[text()='ILS']").click()
        await page.locator("//button[text()='Switch']").click()
        await page.locator("(//a[@class='sidebar-item ng-star-inserted active'])[1]").click()
        balance_temp = await page.locator("//div[@class='wallet-amount']").inner_text()
        balance_before = re.sub('[$,€₪ USD ER IL]', "", balance_temp)
        print(float(balance_before))
        await page.wait_for_timeout(1000)
        await page.locator("//span[@class='sidebar-name'][text() = 'Payments']").click()
        await page.locator("//img[@alt='pay plus icon']").click()
        await page.locator("//span[text() = ' Single Payment ']").click()
        await page.wait_for_timeout(3000)
        await page.locator("//input[@id='beneficiaryInput']").click()
        await page.locator("//input[@id='beneficiaryInput']").type("Other")
        await page.locator("//div/p[text() =' Other']").click()
        await page.wait_for_timeout(2000)
        await page.locator("//button[contains(@class ,'clickedSelect')]").click()
        await page.locator("(//input[@placeholder='0'])[1]").click()
        await page.wait_for_timeout(1000)
        await page.locator("(//input[@placeholder='0'])[1]").type("100")

        await page.locator("//button[@class ='pay-next-btn']").dblclick(delay=2000)

        await page.wait_for_timeout(1000)
        upload_file = await page.get_by_text("Choose file")
        await upload_file.click()
        await page.locator("//div/textarea").fill("This is A test")
        await page.get_by_role("button", name="Next").click()
        await page.wait_for_timeout(1000)
        await page.locator("//input[@type='radio']").nth(1).click()
        fee = await page.locator("//div[@class='transfer-fee-wrap']/strong").nth(1).inner_text()
        new_fee = re.sub('[$,€₪ USD IL ER]', "", fee)
        print(float(new_fee))
        assert float(new_fee) > 3.0
        await page.locator("//input[@class='mdc-checkbox__native-control']").check()
        pay_amount_in_dollar = await page.locator("//li/strong").nth(2).inner_text()
        pay_amount_in_dollar_new = re.sub('[$,€₪ USD ER]', "", pay_amount_in_dollar)
        print(pay_amount_in_dollar_new)
        await page.locator("//button[starts-with(text(),' Pay')]").click()
        await page.reload()
        balance_temp = await page.locator("//div[@class='wallet-amount']").inner_text()
        balance_after = re.sub('[$,€₪ USD IL]', "", balance_temp)
        print(float(balance_after))
        payed_amount = float(new_fee) + float(pay_amount_in_dollar_new)
        assert round(float(balance_before) - (float(balance_after) + round(float(payed_amount), 2)), 1) == 0.0
