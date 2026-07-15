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
from config.config import TICKET_IDS
from tests.selenium.linkedin.test_otherActions_closedTicket import click_with_retry
TICKET_ID = TICKET_IDS["twitter"]
from elements.login_page import LoginPageElements
from elements.reply_panel_page import ReplyPanelPageElements
from utils.credentials import get_twitter_creds

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
            user, pwd = get_twitter_creds()
            browser = locobuzzLogin(user, pwd)
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
            time.sleep(3)

        with allure.step("Reply Type → Reply & On Hold"):
            replyTypeDropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, ReplyPanelPageElements.REPLY_TYPE_DROPDOWN)))
            safe_click(replyTypeDropdown)

            replyOnHold = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.REPLY_AND_ONHOLD)))
            safe_click(replyOnHold)

        with allure.step("Write reply"):
            writeReply = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_INPUT_BOX)))
            writeReply.send_keys("Replying and On Hold wviwa peytehtd")

        with allure.step("Send"):
            sendBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
            safe_click(sendBtn)
            print("✅ Send button clicked")
            time.sleep(5)  # Wait for ticket to move to On Hold

        with allure.step("Navigate to On Hold tab"):
            onHoldTab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.ON_HOLD_TAB2)))
            safe_click(onHoldTab)
            time.sleep(3)

        with allure.step("Search Ticket"):
            searchBtn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(searchBtn)

            searchField = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
            searchField.clear()
            searchField.send_keys(TICKET_ID)
            safe_click(searchBtn)
            time.sleep(2)

            # Scroll to and click account box icon
            account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
            browser.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
            time.sleep(1)
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON))
            time.sleep(1)

            nextArrow = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.NEXT_ARROW)))
            safe_click(nextArrow)
            safe_click(nextArrow)
            time.sleep(1)
            timelineTab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.TIMELINE_TAB)))
            safe_click(timelineTab)
            time.sleep(2)

        with allure.step("Verify Timeline Message"):
            print("\n" + "="*80, flush=True)
            print("🔍 VERIFYING TIMELINE MESSAGE", flush=True)
            print("="*80, flush=True)
            
            timeline_text_xpath = ("//span[contains(@class, 'post-timeline__label') "
                                  "and .//span[normalize-space(.)='Juwairia Agent'] "
                                  "and .//a[normalize-space(.)='this mention'] "
                                  "and contains(., 'has replied on') "
                                  "and contains(., 'kept ticket on hold')]")
            
            timeline_element = wait.until(EC.presence_of_element_located((By.XPATH, timeline_text_xpath)))
            timeline_text = timeline_element.text
            
            print(f"\n✅ Timeline element found!", flush=True)
            print(f"📝 Timeline text: {timeline_text}", flush=True)
            print("="*80, flush=True)
            
            # Verify the text contains expected elements
            assert "Juwairia Agent" in timeline_text, "Juwairia Agent not found in timeline"
            print("✓ 'Juwairia Agent' found", flush=True)
            
            assert "has replied on" in timeline_text, "'has replied on' not found in timeline"
            print("✓ 'has replied on' found", flush=True)
            
            assert "kept ticket on hold" in timeline_text, "'kept ticket on hold' not found in timeline"
            print("✓ 'kept ticket on hold' found", flush=True)
            
            print("\n✅ TIMELINE VERIFICATION SUCCESSFUL!", flush=True)
            print("="*80 + "\n", flush=True)

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