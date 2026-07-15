import pytest
import time
import os
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements
from utils.credentials import get_email_creds
from selenium.webdriver.common.keys import Keys

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
def test_email_reply_await():

    test_name = "email_reply_await"
    driver = None
    try:
        with allure.step("Login"):
            print("\u25AA Login for Email Reply & Awaiting response from Customer...")
            try:
                username, password = get_email_creds()
            except RuntimeError as cred_err:
                pytest.skip(f"Skipping: {cred_err}")
            driver = locobuzzLogin(username, password)
            wait = WebDriverWait(driver, 25)

        with allure.step("Select All & Submit"):
            select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
            safe_click(driver, select_all)
            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
            safe_click(driver, submit_btn)
            time.sleep(2)

        with allure.step("Search Ticket"):
            search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(driver, search_btn)
            search_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
            search_field.clear()
            search_field.send_keys(EMAIL_TICKET_ID)
            safe_click(driver, search_btn)
            search_field.send_keys(Keys.ENTER)
            time.sleep(10)

        with allure.step("Open Reply Panel"):
            time.sleep(3)
            reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_BUTTON)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", reply_btn)
            time.sleep(0.5)
            safe_click(driver, reply_btn)
            time.sleep(2)

        with allure.step("Select Reply Type: Reply & Await"):
            reply_type = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_REPLY_TYPE_DROPDOWN)))
            safe_click(driver, reply_type)
            try:
                await_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_REPLY_AND_AWAIT)))
            except TimeoutException:
                await_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_AND_AWAIT_OPTION_ALTERNATE)))
            safe_click(driver, await_option)
            time.sleep(1)

# Wait for the iframe to be present
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='cke_1_contents']//iframe")))

# Switch into iframe
        driver.switch_to.frame(iframe)

# Wait for the editable body
        editable = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body[@contenteditable='true']")))

# Type your text
        editable.clear()
        editable.send_keys("email reply & awaiting response from customer")

# Switch back to the main page
        driver.switch_to.default_content()

        with allure.step("Click Next"):
            send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_SEND_BTN)))
            safe_click(driver, send_btn)
            time.sleep(3)

        print("\u2705 Email Reply & Await completed")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"\u274C Test failed: {e}")
    finally:
        if driver:
            driver.quit()
