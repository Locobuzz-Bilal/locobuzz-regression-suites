#20OCT25
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
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


@pytest.mark.selenium
def test_reply_and_escalate():
    browser = None
    screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    def capture_failure_screenshot(driver):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshots_dir, f"test_reply_and_escalate_{timestamp}.png")
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
            test_reply_and_escalate.browser = browser
            wait = WebDriverWait(browser, 15)

        with allure.step("Select All & Submit"):
            selectAll = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
            safe_click(selectAll)

            submitBtn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
            safe_click(submitBtn)
            time.sleep(5)

        # with allure.step("More → On Hold tab"):
        #     moreBtn = wait.until(EC.element_to_be_clickable(
        #         (By.XPATH, "(//a[@aria-haspopup='menu' and contains(normalize-space(.), 'More')])[1]")))
        #     safe_click(moreBtn)

        with allure.step("On Hold tab"):
            onHoldTab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.ON_HOLD_TAB)))
            safe_click(onHoldTab)

        with allure.step("Search Ticket"):
            searchBtn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(searchBtn)

            searchField = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
            searchField.clear()
            searchField.send_keys(TICKET_ID)
            safe_click(searchBtn)
            time.sleep(2)

        with allure.step("Click Reply"):
            replyBtn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, ReplyPanelPageElements.REPLY_BUTTON)))
            safe_click(replyBtn)

        with allure.step("Discard & Submit to reset dialog"):
            discardBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
            safe_click(discardBtn)

            submitBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
            safe_click(submitBtn)

        time.sleep(5)  # wait for any overlay/backdrop to disappear

        with allure.step("Reply Type → Reply & Escalate"):
            replyTypeDropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, ReplyPanelPageElements.REPLY_TYPE_DROPDOWN)))
            safe_click(replyTypeDropdown)

            replyEscalate = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.REPLY_AND_ESCALATE_OPTION)))
            safe_click(replyEscalate)

        with allure.step("Write reply"):
            writeReply = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_INPUT_BOX)))
            writeReply.send_keys("Reply & Escalate via pytest")

        with allure.step("Next & Escalation note"):
            nextBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.REPLY_NEXT_BUTTON)))
            safe_click(nextBtn)

            # userDropdown = wait.until(EC.element_to_be_clickable(By.XPATH, '//input[@aria-haspopup="menu"]'))
            # userDropdown.click()
            # time.sleep(1)  # wait for options to render

            writeEscNote = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.ESCALATION_NOTE_INPUT_BOX)))
            writeEscNote.send_keys("Escalating via pytest")
            time.sleep(3)

        with allure.step("Send"):
            sendBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
            safe_click(sendBtn)

        time.sleep(2)
        assert True, "Reply & Escalate test completed successfully"

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


if __name__ == "__main__":
    test_reply_and_escalate()