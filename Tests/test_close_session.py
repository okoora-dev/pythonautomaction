import asyncio
import json
import logging
import os
import sys
import warnings

import pytest

sys.stderr = open(os.devnull, 'w')
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore", category=ResourceWarning)


@pytest.mark.regression
@pytest.mark.asyncio(scope='session')


async def test_check_session_end(page,get_url):
    async def on_response(response):
        if response.status != 200:
            if "RefreshToken?refreshToken=undefined" not in response.url:
                result = await response.json()
                print(response.url, response.status, json.dumps(result, indent=2))
    user_data = get_url
    url = user_data['url']
    user_mail = user_data['mail']
    password = user_data['password']

    async for page in page:
        page.set_default_timeout(610000)
        page.on("response", on_response)
        await page.goto(url)
        await page.goto(url, wait_until="load")
        await page.locator("//input[@name='username']").type(user_mail)
        await page.locator("//input[@name='password']").fill(password)

        await page.get_by_role("button", name="Log In ").click()
        print("Session started. Monitoring for 10 minutes...")

        await monitor_session(page, 600, 900)
        # Close browser context and browser after checking (optional)

async def check_logged_out(page):
    try:
        # Replace this with the actual selector that indicates the user is logged out
        logout_indicator = await page.query_selector("text='Log In'")  # Example selector for a login button
        return logout_indicator is not None
    except Exception as e:
        print("Error checking logout status:", e)
        return False

async def monitor_session(page, min_duration, max_duration):
    start_time = asyncio.get_event_loop().time()
    min_end_time = start_time + min_duration
    max_end_time = start_time + max_duration

    while asyncio.get_event_loop().time() < max_end_time:
        logged_out = await check_logged_out(page)
        current_time = asyncio.get_event_loop().time()

        if logged_out:
            if current_time < min_end_time:
                pytest.fail(f"Alert: User logged out before 10 minutes. {current_time-start_time}")
            elif current_time >= min_end_time:
                pytest.fail(f"Alert: User logged out after 10 minutes.{current_time-start_time}")
        await asyncio.sleep(10)  # Check every 10 seconds

    print("User remained logged in for the full duration (10 minutes). ")
