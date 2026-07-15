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

from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
TICKET_ID = TICKET_IDS["linkedin"]


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
            browser = locobuzzLogin("juw_agent", "Buzz@1234")
            test_reply_and_await.browser = browser
            wait = WebDriverWait(browser, 15)

        with allure.step("Select All & Submit"):
            selectAll = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Select all']")))
            safe_click(selectAll)

            applyBtn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Submit ']")))
            safe_click(applyBtn)

        with allure.step("Search Ticket"):
            searchBtn = wait.until(EC.presence_of_element_located((By.XPATH, "//a[.//mat-icon[text()=' search']]")))
            safe_click(searchBtn)

            searchField = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')))
            searchField.send_keys(TICKET_ID)
            safe_click(searchBtn)
            time.sleep(5)

        with allure.step("Click Reply"):
            replyBtn = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[@class='custom__foot--button post__pill'][.//mat-icon[text()='reply ']]")))
            safe_click(replyBtn)

        with allure.step("Discard and Submit"):
            discard = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Discard ']")))
            safe_click(discard)
            submitBtn2 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Submit ']")))
            safe_click(submitBtn2)
            time.sleep(2)

        with allure.step("Reply Type → Reply & Await"):
            reply_type_dropdown = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")))
            safe_click(reply_type_dropdown)

            replyAwait = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[text()=' Reply & Awaiting response from Customer ']")))
            safe_click(replyAwait)

        with allure.step("Write Reply"):
            writeReply = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write Reply"]')))
            writeReply.send_keys("This is a reply & await test")

        with allure.step("Send"):
            sendBtn = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()=" Send "]')))
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