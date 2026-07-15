#20OCT25
import os
import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locobuzz_login.CX_login import locobuzzLogin
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from config.config import TICKET_IDS
TICKET_ID = TICKET_IDS["twitter"]
from elements.login_page import LoginPageElements
from elements.reply_panel_page import ReplyPanelPageElements

# ---------------------- Test ----------------------
@pytest.mark.selenium
def test_reply_and_onHold():
    browser = None
    screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    def capture_failure_screenshot(driver):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshots_dir, f"test_reply_and_onHold_{timestamp}.png")
        driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")
        allure.attach.file(path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

    def safe_click(element):
        browser.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        browser.execute_script("arguments[0].click();", element)

    try:
        with allure.step("Login with locobuzz"):
            browser = locobuzzLoginPreProd("juw_agent", "Buzz@1234")
            test_reply_and_onHold.browser = browser
            wait = WebDriverWait(browser, 15)

        with allure.step("Select All & Submit"):
            selectAll = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
            safe_click(selectAll)

            applyBtn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
            safe_click(applyBtn)

        with allure.step("More → Awaiting From Customer tab"):
            # try:
            moreBtn = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, ReplyPanelPageElements.More_ICON)
                )
            )
            safe_click(moreBtn)
            # except TimeoutException:
            #     fallbackBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.INBOX)))
            #     safe_click(fallbackBtn)

            awaitingTab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.AWAITING_FROM_CUSTOMER_TAB)))
            safe_click(awaitingTab)
            time.sleep(2)

        with allure.step("Search Ticket"):
            searchBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(searchBtn)

            searchField = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
            searchField.clear()
            searchField.send_keys(TICKET_ID)
            safe_click(searchBtn)
            time.sleep(3)

        with allure.step("Click Reply"):
            replyBtn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, ReplyPanelPageElements.REPLY_BUTTON)))
            safe_click(replyBtn)

        with allure.step("Discard & Submit to reset dialog"):
            discardBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
            safe_click(discardBtn)

            submitBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
            safe_click(submitBtn)
            time.sleep(1)

        with allure.step("Reply Type → Reply & On Hold"):
            replyTypeDropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, ReplyPanelPageElements.REPLY_TYPE_DROPDOWN)))
            safe_click(replyTypeDropdown)

            replyOnHold = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.REPLY_AND_ONHOLD)))
            safe_click(replyOnHold)

        with allure.step("Write reply"):
            writeReply = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_INPUT_BOX)))
            writeReply.send_keys("Replying and On Hold via pytest")

        with allure.step("Send"):
            sendBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
            safe_click(sendBtn)

        time.sleep(2)
        assert True, "Reply & On Hold test completed successfully"

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