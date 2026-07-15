#canned response with attachment in reply and close
import pytest
import time
import os
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements

TICKET_ID = TICKET_IDS["facebook"]

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/facebook"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"[SCREENSHOT] Screenshot saved: {path}")
    allure.attach.file(path, name=test_name, attachment_type=allure.attachment_type.PNG)

def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    driver.execute_script("arguments[0].click();", element)

@pytest.mark.selenium
def test_reply_and_close():
    test_name = "fb_reply_and_close"
    driver = None
    try:
        with allure.step("Login"):
            print(">> Logging in for Facebook Reply & Close...")
            from utils.credentials import get_facebook_creds
            username, password = get_facebook_creds()
            driver = locobuzzLogin(username, password)
            wait = WebDriverWait(driver, 20)

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
            search_field.send_keys(TICKET_ID)
            safe_click(driver, search_btn)
            time.sleep(2)
            safe_click(driver, search_btn)
            time.sleep(3)

        with allure.step("Click Reply"):
            reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_BUTTON)))
            safe_click(driver, reply_btn)
            time.sleep(2)

        with allure.step("Discard & Submit"):
            discard_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
            safe_click(driver, discard_btn)
            submit_btn2 = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
            safe_click(driver, submit_btn2)
            time.sleep(2)

        with allure.step("Select Reply Type: Reply & Close"):
            reply_type = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_TYPE_DROPDOWN)))
            safe_click(driver, reply_type)
            reply_close_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_AND_CLOSE_OPTION)))
            safe_click(driver, reply_close_option)

        # with allure.step("Write Reply & Send"):
        #     time.sleep(2)  # Wait for snackbar to disappear
        #     reply_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_INPUT_BOX)))
        #     safe_click(driver, reply_box)
        #     reply_box.clear()
        #     reply_box.send_keys("Closing Facebook ticket via automation")
        #     send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
        #     safe_click(driver, send_btn)
        #     time.sleep(3)

        with allure.step("Canned response with attachment"):
            # Select Canned Response
            canned_response_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CANNED_RESPONSE)))
            safe_click(driver, canned_response_btn)
            time.sleep(2)
            
            safe_click(driver,wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SELECT))))
            time.sleep(2)

            # Attach a file
            safe_click(driver,wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_MEDIA))))
            time.sleep(2)
            safe_click(driver,wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MEDIA))))
            time.sleep(2)
            safe_click(driver,wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_BUTTON_MEDIA))))
            time.sleep(2)

            # Send Reply & Close
            send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
            safe_click(driver, send_btn)
            time.sleep(3)


        print("[SUCCESS] Facebook Reply & Close completed")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"[FAILED] Test failed: {e}")
    finally:
        if driver:
            driver.quit()

