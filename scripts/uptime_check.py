"""Checks that the Streamlit viewer is up, and wakes it if it has gone to sleep."""

import os
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

APP_URL = os.environ["STREAMLIT_APP_URL"]
WAKE_BUTTON = "//button[contains(., 'get this app back up')]"
SLEEP_TEXT = "get this app back up"
DWELL_SECONDS = 30


def main():
    """
    Visits the app in a headless browser, wakes it if asleep, and stays briefly.

    Exits with status 1 if the app still shows the sleep screen at the end.
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(APP_URL)

        try:
            button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, WAKE_BUTTON))
            )
            print("app was asleep, clicking wake button")
            button.click()
            WebDriverWait(driver, 240).until(
                EC.invisibility_of_element_located((By.XPATH, WAKE_BUTTON))
            )
            print("wake button gone, app is booting")
        except TimeoutException:
            print("no wake button found, app looks awake")

        # Stay on the page so the browser session registers as a visit.
        time.sleep(DWELL_SECONDS)

        if SLEEP_TEXT in driver.page_source:
            print("app still shows the sleep screen")
            sys.exit(1)

        print("done")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
