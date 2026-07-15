import sys
import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
import allure

from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
TICKET_ID = TICKET_IDS["linkedin"]
from helpers.allure_utils import allure_step  # ✅ NEW IMPORT

@pytest.mark.selenium
def test_reply_and_assign():
    browser = None
    screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    test_name = "test_reply_and_assign"

    def capture_failure_screenshot(driver):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
        driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")
        allure.attach.file(path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

    print("🚀 Starting test_reply_and_assign.py...")

    try:
        print("🔹 Attempting to login...")
        try:
            browser = locobuzzLogin("juw_agent", "Buzz@1234")
            if browser:
                print("✅ Browser opened successfully!")
            else:
                raise Exception("Browser not returned from locobuzzLogin")
        except WebDriverException as e:
            print(f"❌ Selenium WebDriver failed to start: {e}")
            raise
        except Exception as e:
            print(f"❌ locobuzzLogin failed: {e}")
            raise

        wait = WebDriverWait(browser, 25)
        actions = ActionChains(browser)

        def safe_click(element):
            browser.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            browser.execute_script("arguments[0].click();", element)

        # --- STEP 1 ---
        with allure_step("Select All & Submit"):
            selectAll = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Select all']")))
            safe_click(selectAll)

            applyBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Submit ']")))
            safe_click(applyBtn)

        # --- STEP 2 ---
        with allure_step(f"Search Ticket ID: {TICKET_ID}"):
            searchBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//mat-icon[text()=' search']]")))
            safe_click(searchBtn)
            searchField = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')))
            searchField.clear()
            searchField.send_keys(TICKET_ID)
            safe_click(searchBtn)
            time.sleep(2)

        # --- STEP 3 ---
        with allure_step("Click Reply & Discard"):
            replyBtn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[@class='custom__foot--button post__pill'][.//mat-icon[text()='reply ']]")))
            safe_click(replyBtn)
            time.sleep(2)   

            discard = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Discard ']")))
            safe_click(discard)
            time.sleep(2)
            # submitBtn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Submit ']")))
            submitBtn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button//span[text()=' Cancel '])[2]")))
            safe_click(submitBtn2)
            time.sleep(3)

        # --- STEP 4 ---
        with allure_step("Select Reply Type → Reply & Assign"):
            reply_type_dropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")))
            safe_click(reply_type_dropdown)
            replyAssign = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Reply & Assign ']")))
            safe_click(replyAssign)

        # --- STEP 5 ---
        with allure_step("Write Reply"):
            writeReply = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write Reply"]')))
            writeReply.clear()
            writeReply.send_keys("Reply and assign11 test by pytest duration tracking")
            NextBtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()=" Next "]')))
            safe_click(NextBtn)

        # --- STEP 6 ---
        with allure_step("Assign User"):
            userDropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '(//input[@type="text"])[3]')))
            safe_click(userDropdown)
            time.sleep(1)
            juwAgent = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Juwairia Agent')]")))
            safe_click(juwAgent)

        # --- STEP 7 ---
        with allure_step("Add Note & Send"):
            addNote = wait.until(EC.presence_of_element_located(
                (By.XPATH, '(//textarea[@formcontrolname="replyEscalateNote"])[2]')))
            addNote.clear()
            addNote.send_keys("Assigning BY pytest with step timing")

            sendBtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()=" Send "]')))
            safe_click(sendBtn)
            time.sleep(5)

        print("✅ Reply and Assign completed successfully")

    except (TimeoutException, WebDriverException) as e:
        print(f"❌ Timeout or Selenium error: {e}")
        if browser:
            capture_failure_screenshot(browser)
        pytest.fail(f"Timeout or Selenium failure: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if browser:
            capture_failure_screenshot(browser)
        pytest.fail(f"Unexpected error: {e}")

    finally:
        if browser:
            print("🧹 Closing browser...")
            browser.quit()


if __name__ == "__main__":
    test_reply_and_assign()