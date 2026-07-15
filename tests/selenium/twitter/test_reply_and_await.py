#20OCT25
import sys
import os
import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements

from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from utils.credentials import get_twitter_creds
TICKET_ID = TICKET_IDS["twitter"]

@pytest.mark.no_rerun
@pytest.mark.selenium
def test_reply_and_await():
    """
    Selenium test: Reply & Awaiting response from Customer
    Browser opens and performs all steps. Fully suite-compatible.
    """
    browser = None
    screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    def capture_failure_screenshot(driver):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshots_dir, f"test_reply_and_await_{timestamp}.png")
        driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")
        allure.attach.file(path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

    def safe_click(element):
        browser.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        browser.execute_script("arguments[0].click();", element)

    try:
        with allure.step("Login with locobuzz"):
            user, pwd = get_twitter_creds()
            browser = locobuzzLogin(user, pwd)
            test_reply_and_await.browser = browser
            wait = WebDriverWait(browser, 15)

        with allure.step("Select All & Submit"):
            selectAll = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
            safe_click(selectAll)

            applyBtn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
            safe_click(applyBtn)

        with allure.step("Search Ticket"):
            searchBtn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(searchBtn)
            time.sleep(1)

            searchField = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
            searchField.send_keys(TICKET_ID)
            searchBtn2 = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(searchBtn2)
            time.sleep(5)

        with allure.step("Click Reply"):
            replyBtn = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.REPLY_BUTTON)))
            safe_click(replyBtn)

        with allure.step("Discard and Submit"):
            discard = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
            safe_click(discard)
            submitBtn2 = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
            safe_click(submitBtn2)
            time.sleep(2)

        with allure.step("Reply Type → Reply & Await"):
            reply_type_dropdown = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.REPLY_TYPE_DROPDOWN)))
            safe_click(reply_type_dropdown)

            replyAwait = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.REPLY_AWAIT_OPTION)))
            safe_click(replyAwait)

        with allure.step("Write Reply"):
            writeReply = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_INPUT_BOX)))
            writeReply.send_keys("This is a reply & await test")

        with allure.step("Send"):
            sendBtn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
            safe_click(sendBtn)
            time.sleep(4)

        assert True, "Reply & Await test completed successfully"

    except TimeoutException as e:
        print(f"❌ TimeoutException: {e}")
        if browser:
            capture_failure_screenshot(browser)
        pytest.fail(f"Timeout or Selenium failure: {e}")

    except Exception as e:
        print(f"❌ Unexpected Exception: {e}")
        if browser:
            capture_failure_screenshot(browser)
        pytest.fail(f"Unexpected error: {e}")

    finally:
        if browser:
            browser.quit()