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
from utils.credentials import get_email_creds

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
def test_email_reply_escalate():
    test_name = "email_reply_escalate"
    driver = None
    try:
        with allure.step("Login"):
            print("\u25AA Login for Email Reply & Escalate...")
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

        with allure.step("(Optional) Navigate to On Hold tab"):
            # Some workflows escalate from On Hold; ignore if not present
            try:
                on_hold_tab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ON_HOLD_TAB)))
                safe_click(driver, on_hold_tab)
                time.sleep(2)
            except TimeoutException:
                pass

        with allure.step("Search Ticket"):
            search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(driver, search_btn)
            search_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
            search_field.clear()
            search_field.send_keys(EMAIL_TICKET_ID)
            safe_click(driver, search_btn)
            search_field.send_keys(Keys.ENTER)
            time.sleep(8)

        with allure.step("Open Reply Panel"):
            reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_BUTTON)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", reply_btn)
            time.sleep(0.5)
            safe_click(driver, reply_btn)
            time.sleep(2)

        with allure.step("Select Reply Type: Reply & Escalate"):
            reply_type_toggle = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_REPLY_TYPE_DROPDOWN)))
            safe_click(driver, reply_type_toggle)
            try:
                escalate_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_REPLY_AND_ESCALATE)))
            except TimeoutException:
                escalate_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_AND_ESCALATE_OPTION_ALTERNATE)))
            safe_click(driver, escalate_option)
            time.sleep(1)

        with allure.step("Write Reply Body"):
            iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='cke_1_contents']//iframe")))
            driver.switch_to.frame(iframe)
            editable = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body[@contenteditable='true']")))
            editable.clear()
            editable.send_keys("escalating to CSD")
            driver.switch_to.default_content()

        with allure.step("Click Next"):
            next_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_NEXT_BUTTON)))
            safe_click(driver, next_btn)
            time.sleep(2)

        with allure.step("Select Escalation Target (Juwairia CSD)"):
            # Dropdown might be similar to assign dropdown
            try:
                assign_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ASSIGN_TO_DROPDOWN)))
                safe_click(driver, assign_dropdown)
            except TimeoutException:
                pass
            csd_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.JUWAIRIA_CSD_OPTION)))
            safe_click(driver, csd_option)
            time.sleep(1)

        with allure.step("Enter Escalation Note"):
            note_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ESCALATION_NOTE_INPUT_BOX)))
            note_box.clear()
            note_box.send_keys("escalating")
            time.sleep(1)

        with allure.step("Send Escalated Reply"):
            send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_SEND_BTN)))
            safe_click(driver, send_btn)
            time.sleep(3)

        print("\u2705 Email Reply & Escalate completed")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"\u274C Test failed: {e}")
    finally:
        if driver:
            driver.quit()
