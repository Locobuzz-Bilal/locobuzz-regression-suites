#20OCT25
import sys
import os
# Add project root for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import time
import re
import pytest
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
TICKET_ID = TICKET_IDS["linkedin"]


@pytest.mark.selenium
def test_csd_approve():
    browser = None
    screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    def take_screenshot(step_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_step_name = re.sub(r'[<>:"/\\|?*]', '_', step_name)
        file_path = os.path.join(screenshots_dir, f"csd_{safe_step_name}_{timestamp}.png")
        browser.save_screenshot(file_path)
        print(f"📸 Screenshot captured: {file_path}")
        return file_path

    def safe_click(element):
        browser.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        browser.execute_script("arguments[0].click();", element)

    try:
        # ---- LOGIN ----
        browser = locobuzzLogin("juw_csd", "Buzz@123")
        test_csd_approve.browser = browser
        wait = WebDriverWait(browser, 15)

        print("🟢 Performing CSD Approve workflow...")

        # ---- Search Ticket ----
        searchBtn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[.//mat-icon[text()=' search']]")))
        safe_click(searchBtn)

        searchField = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')))
        searchField.clear()
        searchField.send_keys(TICKET_ID)
        safe_click(searchBtn)
        time.sleep(5)

        # ---- Click Approve ----
        approveBtn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@mattooltip='Approve']")))
        safe_click(approveBtn)
       

        # ---- Enter note ----
        noteBox = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//textarea[@placeholder='Enter note here']")))
        noteBox.send_keys("Approving by pytest")

        # ---- Attach media ----
        attachBtn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[.//mat-icon[text()='insert_photo']]")))
        safe_click(attachBtn)

        imageThumb = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//img[contains(@src,'002c68f8-4ff7-4678-b064-e6322f903bb8.png')]")))
        safe_click(imageThumb)

        attachConfirm = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button//span[normalize-space(text())='Attach']")))
        safe_click(attachConfirm)

        # ---- Save ----
        saveBtn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button//span[normalize-space(text())='Save']")))
        safe_click(saveBtn)

        time.sleep(2)
        print("✅ Ticket approved successfully!")

    except TimeoutException as e:
        take_screenshot("Timeout_or_Failure")
        pytest.fail(f"Timeout while approving: {e}")

    finally:
        if browser:
            browser.quit()
            print("🧹 Browser closed safely")


if __name__ == "__main__":
    test_csd_approve()