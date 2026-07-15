import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from utils.credentials import get_youtube_creds
TICKET_ID = TICKET_IDS["youtube"]
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/youtube_regression"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_youtube_regression():
    test_name = "youtube_regression_reply_and_close"
    driver = None
    try:
        print("🔹 Logging in using Selenium for YouTube regression test...")
        from utils.credentials import get_twitter_creds  # YouTube uses Twitter credentials
        username, password = get_youtube_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Reply & Close actions...")

        # Select all & Submit
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
        safe_click(select_all)
        submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
        safe_click(submit_btn)
        time.sleep(2)

        # Search Ticket
        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)
        search_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)
        ))
        search_field.clear()
        search_field.send_keys(TICKET_ID)
        safe_click(search_btn)
        time.sleep(3)

        # Click Reply
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_BUTTON))))
        time.sleep(2)
        discard_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
        safe_click(discard_btn)
        submit_btn2 = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
        safe_click(submit_btn2)
        time.sleep(2)

        dismiss = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISMISS)))
        safe_click(dismiss)
        time.sleep(2)

        # Reply Type
        reply_type = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.REPLY_TYPE_DROPDOWN)
        ))
        safe_click(reply_type)
        reply_close_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_AND_CLOSE_OPTION)))
        safe_click(reply_close_option)

        # Write reply & Send
        reply_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_INPUT_BOX)))
        reply_box.click()
        reply_box.clear()
        reply_box.send_keys("Closing YouTube ticket by Selenium automation")
        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
        safe_click(send_btn)
        time.sleep(3)

        print("✅ YouTube Reply & Close completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after YouTube reply & close")
