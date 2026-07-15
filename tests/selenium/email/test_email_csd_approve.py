import pytest
import time
import os
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements
from utils.credentials import get_csd_creds

EMAIL_TICKET_ID = TICKET_IDS.get("email")


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/email"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"\U0001F4F8 Screenshot saved: {path}")
    allure.attach.file(path, name=test_name, attachment_type=allure.attachment_type.PNG)


def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    driver.execute_script("arguments[0].click();", element)


@pytest.mark.selenium
def test_email_csd_approve():
    test_name = "email_csd_approve"
    driver = None
    try:
        with allure.step("Login as CSD"):
            print("\u25AA Login for Email CSD Approve...")
            try:
                username, password = get_csd_creds()
            except RuntimeError as cred_err:
                pytest.skip(f"Skipping: {cred_err}")
            driver = locobuzzLogin(username, password)
            wait = WebDriverWait(driver, 25)

        with allure.step("Search Ticket"):
            search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(driver, search_btn)
            search_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
            search_field.clear()
            search_field.send_keys(EMAIL_TICKET_ID)
            safe_click(driver, search_btn)
            search_field.send_keys(Keys.ENTER)
            time.sleep(8)

        with allure.step("Click Approve Icon"):
            # Try primary locator first, then alternate
            try:
                approve_icon = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.APPROVE_ICON)))
            except TimeoutException:
                approve_icon = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CSD_APPROVE_ICON_ALTERNATE)))
            
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", approve_icon)
            time.sleep(0.5)
            safe_click(driver, approve_icon)
            time.sleep(2)

        with allure.step("Enter Approval Note"):
            note_input = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CSD_APPROVAL_NOTE_INPUT)))
            note_input.clear()
            note_input.send_keys("approved")
            time.sleep(1)

        with allure.step("Save Approval"):
            save_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CSD_SAVE_BUTTON)))
            safe_click(driver, save_btn)
            time.sleep(3)

        print("\u2705 Email CSD Approve completed")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"\u274C Test failed: {e}")
    finally:
        if driver:
            driver.quit()
