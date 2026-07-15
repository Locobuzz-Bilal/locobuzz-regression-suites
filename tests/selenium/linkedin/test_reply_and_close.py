#20OCT25
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
TICKET_ID = TICKET_IDS["linkedin"]

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/reply_and_close"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_reply_and_close():
    test_name = "reply_and_close"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        driver = locobuzzLogin("juw_agent", "Buzz@1234")
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Reply & Close actions...")

        # Select all & Submit
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Select all']")))
        safe_click(select_all)
        submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Submit ']")))
        safe_click(submit_btn)
        time.sleep(2)
        pendingTab = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Pending ']")))
        safe_click(pendingTab)
        safe_click(pendingTab)
        time.sleep(2)
        # Search Ticket
        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//a[.//mat-icon[text()=' search']]")))
        safe_click(search_btn)
        search_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')
        ))
        search_field.clear()
        search_field.send_keys(TICKET_ID)
        safe_click(search_btn)
        time.sleep(3)


        # Click Reply
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(., '{TICKET_ID}')]//span[normalize-space(text())='Reply']"))))
        time.sleep(2)
        discard_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Discard ']")))
        safe_click(discard_btn)
        submit_btn2 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Submit ']")))
        safe_click(submit_btn2)
        time.sleep(2)

        dismiss = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Dismiss']")))
        safe_click(dismiss)
        time.sleep(2)

        # Reply Type
        reply_type = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
        ))
        safe_click(reply_type)
        reply_close_option = wait.until(EC.presence_of_element_located((By.XPATH, "//mat-option//span[normalize-space()='Reply & Close']")))
        safe_click(reply_close_option)

        # Write reply & Send
        reply_box = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Write Reply']")))
        reply_box.click()
        reply_box.clear()
        reply_box.send_keys("Closing ticket by Selenium")
        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, " //span[text()=' Send ']")))
        safe_click(send_btn)
        time.sleep(3)

        print("✅ Reply & Close completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after reply & close")