import json
import re
import time
import pytest
import asyncio
from playwright.async_api import async_playwright, expect

@pytest.mark.regression
@pytest.mark.asyncio(scope='session')
async def test_mass_payment(page,get_url):
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']
    start = time.perf_counter()

    async def on_chooser(file_chooser):
        await file_chooser.set_files("Upload.pdf")
        print("File uploaded")

    async def on_response(response):
        result = await response.json()
        try:
            if "BalanceList" in response.url:
                print("Waiting for response...")
                result = await asyncio.wait_for(response.json(), timeout=5.0)
                print("Response received.")
        except asyncio.TimeoutError:
            print("Response took more than 5 seconds.")

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
        await page.locator("//span[(text()='Other')]").last.click()
        await page.locator("//button[text()='Selected (2)']").click()
        await page.get_by_role("button", name=" Wallet balance: ").click()
        switch_wallet = page.locator("//span[@class = 'balance-currency' and text()='ILS']")
        await switch_wallet.click()
        switch_button = page.get_by_role("button", name="Switch")
        await switch_button.click()

        amount1 = page.locator("//div[@class='input-container']/div/input[@type='text']").nth(0)
        await amount1.type("100")
        amount2 = page.locator("//div[@class='input-container']/div/input[@type='text']").nth(1)
        await amount2.type("100")
        await page.locator("//div[@class='input-container']").last.click()
        drop_down = page.get_by_role("button", name="Select").nth(0)
        await drop_down.click()
        regular = page.get_by_text("Regular Transfer")
        await regular.click()
        drop_down1 = page.get_by_role("button", name="Select").last
        await drop_down1.click()
        regular = page.get_by_text("Regular Transfer")
        await regular.click()
        amount1 = await page.locator("//div[@class='input-container']/span[@class='ng-star-inserted']").nth(0).inner_text()
        amount2 = await page.locator("//div[@class='input-container']/span[@class='ng-star-inserted']").nth(1).inner_text()
        converted_amount1 = float(re.sub('[$₪€,]', "", amount1))
        converted_amount2 = float(re.sub('[$₪€,]', "", amount2))
        total_amount = converted_amount1 + converted_amount2
        file_input = page.locator("//button[@class='ng-star-inserted']")
        await file_input.click()
        upload_file = page.get_by_text("Choose file")
        await upload_file.click()
        await page.locator("//button[@type='submit' and text()='Next']").click()
        print(total_amount)

        save_button = page.locator("//button[@id='gotoNext_btn_mass_payment']")
        await save_button.click()

        check_box = page.locator("span:text('I Approve the Policy')")
        await check_box.check()
        pay_button = page.locator("button.pay-button")
        await pay_button.click()
        payment_detail = page.locator("//button[text()='Payment details']")
        await payment_detail.click()
        end_time = time.perf_counter() - start
        await asyncio.sleep(5)
        plus_button = page.get_by_alt_text("pay plus icon")
        await plus_button.click()
        await page.get_by_text("Mass Payment").click()
        await asyncio.sleep(5)
        old_payment = page.locator("//td/button[@class='custom-dropdown-button']")
        await expect(old_payment).not_to_be_visible()  # check issue https://okoora.atlassian.net/browse/DV-1496

        await page.reload()
        await page.locator("//span[text()='Dashboard']").click()
        ils_wallet = await page.locator("//p[@id='wallet-price']").nth(0).inner_text()
        wallet_after = float(re.sub('[$₪€,USD ER]', "", ils_wallet))
        new_wallet = (wallet_before - wallet_after)
        assert round(new_wallet, 2) > total_amount
        print(f"...Test finished at {round(end_time, 2)}")

