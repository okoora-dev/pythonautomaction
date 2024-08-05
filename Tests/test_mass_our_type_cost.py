import json
import re
import time
import pytest
import asyncio


req_id = ""

#################This Test cover HOT FIX https://okoora.atlassian.net/browse/DV-2070###################################
@pytest.mark.regression
@pytest.mark.asyncio(scope='session')
async def test_mass_our_payment_type(page,get_url, sql_query):
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']
    global req_id
    user_id = user_data["user_id"]
    query = sql_query
    query.add_free_fee(user_id)
    query.change_outgoing_payments(user_id)
    query.reset_outgoing_payments(user_id)

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
        global req_id
        result = await response.json()
        if "UpdateCostType" in response.url:
            req_id = result['requestId']

        if result[0]['apiErrorMessage'][0] == 'Cost is Missing':
            print((response.url, response.status, json.dumps(result, indent=2)))

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
        wallet = await page.locator("//p[@id='wallet-price']").nth(0).inner_text()
        wallet_before = float(re.sub('[$₪€,ER USD]', "", wallet))
        print(wallet_before)
        payment_button = page.get_by_text("Payments")
        await payment_button.click()

        plus_button = page.get_by_alt_text("pay plus icon")
        await plus_button.click()
        await page.get_by_text("Mass Payment").click()
        await asyncio.sleep(5)
        if await page.locator("//td/button[@class='custom-dropdown-button']").is_visible():
            await page.locator("//img[contains(@src,'delete')]").click()
            await page.locator("//button[@class='delete']").click()

        await page.get_by_role("button", name="+ Add").nth(0).click()
        await asyncio.sleep(2)

        await page.locator("//span[(text()='Test USD')]").last.click()
        await page.locator("//button[text()='Selected (1)']").click()
        await page.get_by_role("button", name=" Wallet balance: ").click()
        switch_wallet = page.locator("//span[@class = 'balance-currency' and text()='ILS']")
        await switch_wallet.click()
        switch_button = page.get_by_role("button", name="Switch")
        await switch_button.click()

        amount1 = page.locator("//div[@class='input-container']/div/input[@type='text']")
        await amount1.type("100")
        await page.locator("//span[@class = 'ng-star-inserted']").nth(0).click()
        await page.locator("//button[@class='dropbtn']").click()
        our = page.get_by_text("Our Transfer")
        await our.click()
        await page.locator("//button[text()='Next']").click()
        check_box = page.locator("span:text('I Approve the Policy')")
        await check_box.check()
        await asyncio.sleep(32)

        pay_button = page.locator("button.pay-button")
        await pay_button.click()
        payment_detail = page.locator("//button[text()='Payment details']")
        await payment_detail.click()
        row_num = query.find_quote(str(req_id))
        fee_amount = query.get_fee_payed(user_id)
        assert fee_amount != 0.00, f"Fee amount is {fee_amount}"
        assert row_num == 1

