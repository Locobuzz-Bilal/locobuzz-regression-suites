import sys
import os
import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from utils.credentials import get_fb_creds

TICKET_ID = TICKET_IDS["facebook"]


@pytest.mark.selenium
def test_reply_and_escalate():
    browser = None
    screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    def capture_failure_screenshot(driver):
        ts = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshots_dir, f"test_reply_and_escalate_{ts}.png")
        driver.save_screenshot(path)
        print(f"� Screenshot saved: {path}")
        try:
            allure.attach.file(path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

    def safe_click(xpath, wait: WebDriverWait):
        el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        browser.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        browser.execute_script("arguments[0].click();", el)

    try:
        with allure.step("Login with Locobuzz (facebook agent)"):
            user, pwd = get_fb_creds()
            browser = locobuzzLogin(user, pwd)
            test_reply_and_escalate.browser = browser
            wait = WebDriverWait(browser, 15)

        with allure.step("Select All & Submit"):
            safe_click("//span[text()='Select all']", wait)
            safe_click("//span[text()=' Submit ']", wait)
            time.sleep(3)

        with allure.step("Open 'On Hold' tab"):
            safe_click("//a[text()='On Hold ']", wait)

        with allure.step("Search Ticket"):
            safe_click("//a[.//mat-icon[text()=' search']]", wait)
            field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')))
            field.clear()
            field.send_keys(TICKET_ID)
            safe_click("//a[.//mat-icon[text()=' search']]", wait)
            time.sleep(2)

        with allure.step("Click Reply"):
            safe_click("//span[@class='custom__foot--button post__pill'][.//mat-icon[text()='reply ']]", wait)

        with allure.step("Discard & Submit"):
            safe_click("//span[text()=' Discard ']", wait)
            safe_click("//span[text()=' Submit ']", wait)
            time.sleep(4)

        with allure.step("Select Reply & Escalate"):
            safe_click("//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select", wait)
            safe_click("//span[normalize-space()='  Reply & Escalate ']", wait)

        with allure.step("Compose Reply"):
            reply_box = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write Reply"]')))
            reply_box.send_keys("Reply & Escalate via pytest (facebook)")

        with allure.step("Next & choose escalation target"):
            safe_click("//span[normalize-space()=' Next ']", wait)
            # Open Escalate To input (focus triggers panel)
            safe_click('//mat-label[normalize-space()="Escalate To"]/ancestor::mat-form-field//input', wait)
            # Select facebook csd (case-insensitive)
            safe_click('//span[contains(translate(normalize-space(.), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "facebook csd")]', wait)

        with allure.step("Add escalation note & Send"):
            esc_note = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write escalation note here..."]')))
            esc_note.send_keys("Escalating via pytest")
            safe_click('//span[text()=" Send "]', wait)
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


if __name__ == "__main__":  # Manual run
    test_reply_and_escalate()
#         print(f"❌ Timeout: Element not found for XPath {xpath}")
#         take_screenshot(page, "safe_click_failure")
#         raise


# # ---------------------- Main Function ----------------------
# def run(playwright):
#     start_time = time.time()

#     # ---------------- FIRST LOGIN (juw_agent) ----------------
#     user1_start = time.time()
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context(viewport={"width": 1920, "height": 1080})
#     page = context.new_page()

#     try:
"""Facebook: Reply & Escalate Selenium test (final cleaned version)."""

import sys
import os
import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from utils.credentials import get_fb_creds

TICKET_ID = TICKET_IDS["facebook"]


@pytest.mark.selenium
def test_reply_and_escalate():
    browser = None
    screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    def snap_fail():
        if not browser:
            return
        ts = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshots_dir, f"test_reply_and_escalate_{ts}.png")
        try:
            browser.save_screenshot(path)
            print(f"📸 Saved failure screenshot: {path}")
            allure.attach.file(path, name="Failure", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

    def click_xpath(wait: WebDriverWait, xpath: str):
        el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        browser.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        browser.execute_script("arguments[0].click();", el)

    try:
        with allure.step("Login"):
            user, pwd = get_fb_creds()
            browser = locobuzzLogin(user, pwd)
            wait = WebDriverWait(browser, 15)

        with allure.step("Select all & submit"):
            click_xpath(wait, "//span[text()='Select all']")
            click_xpath(wait, "//span[text()=' Submit ']")
            time.sleep(2)

        with allure.step("Open On Hold tab"):
            click_xpath(wait, "//a[text()='On Hold ']")

        with allure.step("Search ticket"):
            click_xpath(wait, "//a[.//mat-icon[text()=' search']]")
            field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')))
            field.clear(); field.send_keys(TICKET_ID)
            click_xpath(wait, "//a[.//mat-icon[text()=' search']]")
            time.sleep(2)

        with allure.step("Reply action"):
            click_xpath(wait, "//span[@class='custom__foot--button post__pill'][.//mat-icon[text()='reply ']]")
            click_xpath(wait, "//span[text()=' Discard ']")
            click_xpath(wait, "//span[text()=' Submit ']")
            time.sleep(2)

        with allure.step("Select Reply & Escalate"):
            click_xpath(wait, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
            click_xpath(wait, "//span[contains(normalize-space(),'Reply & Escalate')]")

        with allure.step("Compose reply"):
            reply_box = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write Reply"]')))
            reply_box.send_keys("Reply & Escalate via pytest (facebook)")

        with allure.step("Escalation target"):
            click_xpath(wait, "//span[text()=' Next ']")
            click_xpath(wait, '//mat-label[normalize-space()="Escalate To"]/ancestor::mat-form-field//input')
            click_xpath(wait, '//span[contains(translate(normalize-space(.), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "facebook csd")]')

        with allure.step("Note & send"):
            esc_note = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write escalation note here..."]')))
            esc_note.send_keys("Escalating via pytest")
            click_xpath(wait, '//span[text()=" Send "]')
            time.sleep(2)

        assert True

    except TimeoutException as e:
        print(f"❌ Timeout: {e}")
        snap_fail()
        pytest.fail(str(e))
    except Exception as e:
        print(f"❌ Unexpected: {e}")
        snap_fail()
        pytest.fail(str(e))
    finally:
        if browser:
            browser.quit()


if __name__ == "__main__":
    test_reply_and_escalate()
# WORKING CODE  
#-----------------------------------------------------------------------------------------------------------

"""import re
import time
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config.config import TICKET_ID

SCRIPT_NAME = "reply_and_escalate"

# ---------------------- Helper: Take Screenshot ----------------------
def take_screenshot(page, step_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)
    file_path = f"{folder}/{SCRIPT_NAME}_{step_name}_{timestamp}.png"
    page.screenshot(path=file_path, full_page=True)
    print(f"📸 Screenshot captured: {file_path}")
    return file_path

# ---------------------- Helper: Safe Click ----------------------
def safe_click(page, xpath, timeout=10000):
    try:
        page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
        page.locator(f"xpath={xpath}").click()
        print(f"✅ Clicked: {xpath}")
    except PlaywrightTimeoutError:
        print(f"❌ Timeout: Element not found for XPath {xpath}")
        take_screenshot(page, f"safe_click_failure_{xpath.replace('/', '_')}")
        raise

# ---------------------- Main Function ----------------------
def run(playwright):
    start_time = time.time()

    # ---------------- FIRST LOGIN (juw_agent) ----------------
    user1_start = time.time()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    try:
        print("🔹 Logging in as juw_agent...")
        page.goto("https://cx.locobuzz.com/login")

        # Fill username
        try:
            page.wait_for_selector('input[formcontrolname="username"]:not([readonly])', timeout=8000)
            page.fill('input[formcontrolname="username"]', "juw_agent")
        except PlaywrightTimeoutError:
            print("⚠️ Username field readonly — removing attribute manually...")
            page.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
            page.fill('input[formcontrolname="username"]', "juw_agent")

        page.get_by_role("button", name="Continue").click()
        page.wait_for_selector('input[formcontrolname="password"]', timeout=10000)
        page.fill('input[formcontrolname="password"]', "Buzz@1234")
        page.get_by_role("button", name="Login").click()
        page.wait_for_timeout(4000)

        print("🟢 Performing Reply & Escalate actions...")
        page.get_by_text("check_circleSelect all").click()
        page.get_by_role("button", name="Submit").click()
        page.get_by_text("On Hold ").click()

        # Search Ticket
        safe_click(page, "//a[.//mat-icon[text()=' search']]")
        page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
        safe_click(page, "//a[.//mat-icon[text()=' search']]")
        page.wait_for_timeout(3000)

        page.locator("#Post_3773015").get_by_text("Reply", exact=True).click()
        page.get_by_role("button", name="Discard").click()
        page.get_by_role("button", name="Submit").click()

        safe_click(page, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
        page.get_by_role("option", name="Reply & Escalate").click()
        page.get_by_role("textbox", name="Write Reply").fill("Reply & Escalate by IDE")
        page.get_by_role("button", name="Next").click()
        page.get_by_role("textbox", name="Write escalation note here...").fill("Escalate")
        page.get_by_role("button", name="Send").click()

        # Logout
        print("🔸 Logging out juw_agent...")
        page.wait_for_timeout(2000)
        page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).locator("a").click()
        page.get_by_role("menuitem", name="Logout").click()
        page.get_by_role("button", name="Logout").click()

        user1_time = round(time.time() - user1_start, 2)
        print(f"✅ juw_agent flow completed in {user1_time} seconds\n")

    except Exception as e:
        print(f"❌ ERROR during juw_agent flow: {e}")
        take_screenshot(page, "juw_agent_failure")
        raise

    finally:
        context.close()
        browser.close()
        print("🧹 Closed first browser session after juw_agent logout.\n")

    # ---------------- SECOND LOGIN (juw_csd) ----------------
    user2_start = time.time()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    try:
        print("🔹 Logging in as juw_csd...")
        page.goto("https://cx.locobuzz.com/login")

        try:
            page.wait_for_selector('input[formcontrolname="username"]:not([readonly])', timeout=8000)
            page.fill('input[formcontrolname="username"]', "juw_csd")
        except PlaywrightTimeoutError:
            print("⚠️ Username field readonly — removing attribute manually...")
            page.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
            page.fill('input[formcontrolname="username"]', "juw_csd")

        page.get_by_role("button", name="Continue").click()
        page.wait_for_selector('input[formcontrolname="password"]', timeout=10000)
        page.fill('input[formcontrolname="password"]', "Buzz@123")
        page.get_by_role("button", name="Login").click()
        page.wait_for_timeout(4000)

        print("🟢 Performing Approve actions...")
        page.locator("a", has_text="search").click()
        page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
        page.locator("a", has_text="search").click()
        page.locator("#Post_3773015").get_by_text("Approve").click()
        page.get_by_role("textbox", name="Enter note here").fill("Approving by IDE")
        page.get_by_role("link", name="Attach Media").click()
        time.sleep(3)
        safe_click(page, "//img[@src='https://images.locobuzz.com/LocoBuzzImages/SocialPostTriggerScheduling/reliancejiodb/002c68f8-4ff7-4678-b064-e6322f903bb8.png']")
        time.sleep(3)
        page.get_by_role("button", name="Attach").click()
        page.get_by_role("button", name="Save").click()

        user2_time = round(time.time() - user2_start, 2)
        total_time = round(time.time() - start_time, 2)
        print(f"✅ juw_csd flow completed in {user2_time} seconds\n")
        print("🎯 Execution Summary:")
        print(f"   🔹 juw_agent  → {user1_time} sec")
        print(f"   🔹 juw_csd    → {user2_time} sec")
        print(f"   ⏱️ Total time → {total_time} sec")

    except Exception as e:
        print(f"❌ ERROR during juw_csd flow: {e}")
        take_screenshot(page, "juw_csd_failure")
        raise

    finally:
        context.close()
        browser.close()
        print("🧹 Browser closed safely at end of run.")

# ---------------------- Entry Point ----------------------
if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)"""



# Perplexity Code 
# tests/playwright/test_reply_and_escalate.py
###------------------------------------------------------------------------------------------------------last edited 13october2025 at 4:39PM`-------------------------------------------------------------------------------------------------`
"""import pytest
import re
import time
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config.config import TICKET_ID
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.mark.playwright
def test_reply_and_escalate():
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    def take_screenshot(page, step_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"{screenshots_dir}/reply_and_escalate_{step_name}_{timestamp}.png"
        page.screenshot(path=file_path, full_page=True)
        print(f"📸 Screenshot captured: {file_path}")
        return file_path

    def safe_click(page, xpath, timeout=10000):
        try:
            page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
            page.locator(f"xpath={xpath}").click()
            print(f"✅ Clicked: {xpath}")
        except PlaywrightTimeoutError as e:
            print(f"❌ Timeout: Element not found for XPath {xpath}")
            take_screenshot(page, f"safe_click_failure_{xpath.replace('/', '_')}")
            raise e

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        try:
            start_time = time.time()

            # First login with juw_agent
            print("🔹 Logging in as juw_agent...")
            page.goto("https://cx.locobuzz.com/login")

            try:
                page.wait_for_selector('input[formcontrolname="username"]:not([readonly])', timeout=8000)
                page.fill('input[formcontrolname="username"]', "juw_agent")
            except PlaywrightTimeoutError:
                print("⚠️ Username field readonly — removing attribute manually...")
                page.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
                page.fill('input[formcontrolname="username"]', "juw_agent")

            page.get_by_role("button", name="Continue").click()
            page.wait_for_selector('input[formcontrolname="password"]', timeout=10000)
            page.fill('input[formcontrolname="password"]', "Buzz@1234")
            page.get_by_role("button", name="Login").click()
            page.wait_for_timeout(4000)

            print("🟢 Performing Reply & Escalate actions...")

            page.get_by_text("check_circleSelect all").click()
            page.get_by_role("button", name="Submit").click()
            page.get_by_text("On Hold ").click()

            safe_click(page, "//a[.//mat-icon[text()=' search']]")
            page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
            safe_click(page, "//a[.//mat-icon[text()=' search']]")
            page.wait_for_timeout(3000)


            replyBtn1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space(text())='Reply']")), timeout=10) 
            page.locator("#Post_3773015").get_by_text("Reply", exact=True).click()
            page.get_by_role("button", name="Discard").click()
            page.get_by_role("button", name="Submit").click()

            safe_click(page, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
            page.get_by_role("option", name="Reply & Escalate").click()
            page.get_by_role("textbox", name="Write Reply").fill("Reply & Escalate by pytest")
            page.get_by_role("button", name="Next").click()
            page.get_by_role("textbox", name="Write escalation note here...").fill("Escalate")
            page.get_by_role("button", name="Send").click()

            print("🔸 Logging out juw_agent...")
            page.wait_for_timeout(2000)
            page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).locator("a").click()
            page.get_by_role("menuitem", name="Logout").click()
            page.get_by_role("button", name="Logout").click()

            user1_time = round(time.time() - start_time, 2)
            print(f"✅ juw_agent flow completed in {user1_time} seconds\n")

            # Second login with juw_csd
            start_csd = time.time()
            browser2 = playwright.chromium.launch(headless=False)
            context2 = browser2.new_context(viewport={"width": 1920, "height": 1080})
            page2 = context2.new_page()

            print("🔹 Logging in as juw_csd...")
            page2.goto("https://cx.locobuzz.com/login")

            try:
                page2.wait_for_selector('input[formcontrolname="username"]:not([readonly])', timeout=8000)
                page2.fill('input[formcontrolname="username"]', "juw_csd")
            except PlaywrightTimeoutError:
                print("⚠️ Username field readonly — removing attribute manually...")
                page2.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
                page2.fill('input[formcontrolname="username"]', "juw_csd")

            page2.get_by_role("button", name="Continue").click()
            page2.wait_for_selector('input[formcontrolname="password"]', timeout=10000)
            page2.fill('input[formcontrolname="password"]', "Buzz@123")
            page2.get_by_role("button", name="Login").click()
            page2.wait_for_timeout(4000)

            print("🟢 Performing Approve actions...")
            page2.locator("a", has_text="search").click()
            page2.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
            page2.locator("a", has_text="search").click()
            page2.locator("#Post_3773015").get_by_text("Approve").click()
            page2.get_by_role("textbox", name="Enter note here").fill("Approving by pytest")
            page2.get_by_role("link", name="Attach Media").click()
            time.sleep(3)
            safe_click(page2, "//img[@src='https://images.locobuzz.com/LocoBuzzImages/SocialPostTriggerScheduling/reliancejiodb/002c68f8-4ff7-4678-b064-e6322f903bb8.png']")
            time.sleep(3)
            page2.get_by_role("button", name="Attach").click()
            page2.get_by_role("button", name="Save").click()

            user2_time = round(time.time() - start_csd, 2)
            total_time = round(time.time() - start_time, 2)
            print(f"✅ juw_csd flow completed in {user2_time} seconds\n")
            print("🎯 Execution Summary:")
            print(f"   🔹 juw_agent  → {user1_time} sec")
            print(f"   🔹 juw_csd    → {user2_time} sec")
            print(f"   ⏱️ Total time → {total_time} sec")

            assert True

        except Exception as e:
            take_screenshot(page, "test_failure")
            pytest.fail(f"Test failed: {e}")

        finally:
            context.close()
            browser.close()
            context2.close()
            browser2.close()
            print("🧹 Browser(s) closed safely for test_reply_and_escalate")"""
            ###------------------------------------------------------------------------------------------------------last edited 13october2025 at 4:39PM`-------------------------------------------------------------------------------------------------`


# tests/playwright/test_reply_and_escalate.py

#-------------------------------------------------------LATEST________________________________________________________________________________________
'''import pytest
import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config.config import TICKET_ID


@pytest.mark.playwright
def test_reply_and_escalate():
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    def snap(page, tag):
        path = os.path.join(
            screenshots_dir,
            f"reply_and_escalate_{tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        )
        page.screenshot(path=path, full_page=True)
        return path

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--force-device-scale-factor=1",
                "--no-sandbox",
                "--disable-infobars",
                "--disable-extensions",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        # ✅ Make sure viewport is unlocked
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # ✅ Force fullscreen window & reset zoom
        page.evaluate("""
            window.moveTo(0, 0);
            window.resizeTo(screen.width, screen.height);
            document.body.style.zoom = '100%';
        """)

        # --- LOGIN ---
        page.goto("https://cx.locobuzz.com/login")
        try:
            page.wait_for_selector('input[formcontrolname="username"]:not([readonly])', timeout=8000)
            page.fill('input[formcontrolname="username"]', "juw_agent")
        except PlaywrightTimeoutError:
            page.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
            page.fill('input[formcontrolname="username"]', "juw_agent")

        page.get_by_role("button", name="Continue").click()
        page.wait_for_selector('input[formcontrolname="password"]', timeout=10000)
        page.fill('input[formcontrolname="password"]', "Buzz@1234")
        page.get_by_role("button", name="Login").click()
        page.wait_for_timeout(2000)
        
        # Continue your existing steps below...
        try:
            print("🟢 Performing Reply & Escalate actions...")

            # --- SELECT ALL + SUBMIT ---
            page.locator("//span[text()='Select all']").click()
            page.locator("//button[contains(.,'Submit')]").click()

            # --- ON HOLD ---
            page.get_by_text("check_circleSelect all").click()
            page.get_by_role("button", name="Submit").click()
            page.locator("//a[contains(normalize-space(.),'On Hold')]").click()

            time.sleep(2)

            # --- SEARCH TICKET ---
            page.locator("//a[.//mat-icon[text()=' search']]").click()
            page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
            page.locator("//a[.//mat-icon[text()=' search']]").click()
            page.wait_for_timeout(1500)
            time.sleep(2)

            # --- REPLY ---
            page.locator("//span[@class='custom__foot--button post__pill'][.//mat-icon[text()='reply ']]").click()

            # --- Reset dialog if needed ---
           # --- Reset dialog if needed (optional discard popup) ---
            try:
                page.wait_for_selector("//span[contains(.,'Discard')]", timeout=5000)
                page.locator("//span[contains(.,'Discard')]").click()
                page.wait_for_selector("//span[contains(.,'Submit')]", timeout=5000)
                page.locator("//span[contains(.,'Submit')]").click()
                print("🟡 Discard dialog handled")
            except Exception:
                print("⚪ No discard dialog appeared, continuing...")

# --- Open Reply again ---
            page.locator("//span[@class='custom__foot--button post__pill'][.//mat-icon[normalize-space()='reply']]").click()


            # --- Reply Type: Reply & Escalate ---
            page.locator("//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select").click()
            page.locator("//span[normalize-space()=' Reply & Escalate ']").click()

            # --- Write reply ---
            page.get_by_role("textbox", name="Write Reply").fill("Replying and Escalating via pytest")

            # --- Next → choose assignee/team ---
            page.locator("//span[normalize-space()=' Next ']").click()
            page.locator("(//input[@type='text' and @role='combobox'])[1]").click()
            page.wait_for_timeout(500)
            page.locator("//span[contains(normalize-space(),'Juwairia Agent') or contains(normalize-space(),'Support')]").click()

            # --- Add note and Send ---
            page.locator("(//textarea[@formcontrolname='replyEscalateNote'])[1]").fill("Escalating by pytest")
            page.locator("//span[normalize-space()=' Send ']").click()

            assert True

        except Exception as e:
            snap(page, "failure")
            pytest.fail(f"Test failed: {e}")

        finally:
            context.close()
            browser.close()'''

#-------------------------------------------------------LATEST________________________________________________________________________________________





''' works
import pytest
import re
import time
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config.config import TICKET_ID


@pytest.mark.playwright
def test_reply_and_escalate():
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    def take_screenshot(page, step_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"{screenshots_dir}/reply_and_escalate_{step_name}_{timestamp}.png"
        page.screenshot(path=file_path, full_page=True)
        print(f"📸 Screenshot captured: {file_path}")
        return file_path

    def safe_click(page, xpath, timeout=10000):
        try:
            page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
            page.locator(f"xpath={xpath}").click()
            print(f"✅ Clicked: {xpath}")
        except PlaywrightTimeoutError as e:
            print(f"❌ Timeout: Element not found for XPath {xpath}")
            take_screenshot(page, f"safe_click_failure_{xpath.replace('/', '_')}")
            raise e

    browser = context = browser2 = context2 = None  # Initialize to avoid UnboundLocalError

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

            # ---------------- Login juw_agent ----------------
            page.goto("https://cx.locobuzz.com/login")
            try:
                page.wait_for_selector('input[formcontrolname="username"]:not([readonly])', timeout=8000)
            except PlaywrightTimeoutError:
                page.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
            page.fill('input[formcontrolname="username"]', "juw_agent")
            page.get_by_role("button", name="Continue").click()
            page.fill('input[formcontrolname="password"]', "Buzz@1234")
            page.get_by_role("button", name="Login").click()
            page.wait_for_timeout(4000)

            print("🟢 Performing Reply & Escalate actions...")

            # Example actions
            page.get_by_text("check_circleSelect all").click()
            page.get_by_role("button", name="Submit").click()
            page.get_by_text("On Hold ").click()

            safe_click(page, "//a[.//mat-icon[text()=' search']]")
            page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
            safe_click(page, "//a[.//mat-icon[text()=' search']]")
            page.wait_for_timeout(3000)

            # --------- Robust Reply click ----------
            safe_click(page, "//span[normalize-space(text())='Reply']")  # ignores extra spaces
            page.get_by_role("button", name="Discard").click()
            page.get_by_role("button", name="Submit").click()

            safe_click(page, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
            page.get_by_role("option", name="Reply & Escalate").click()
            page.get_by_role("textbox", name="Write Reply").fill("Reply & Escalate by pytest")
            page.get_by_role("button", name="Next").click()
            page.get_by_role("textbox", name="Write escalation note here...").fill("Escalate")
            page.get_by_role("button", name="Send").click()

            print("🔸 Logging out juw_agent...")
            page.wait_for_timeout(2000)
            page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).locator("a").click()
            page.get_by_role("menuitem", name="Logout").click()
            page.get_by_role("button", name="Logout").click()

            # ---------------- Login juw_csd ----------------
            browser2 = playwright.chromium.launch(headless=False)
            context2 = browser2.new_context(viewport={"width": 1920, "height": 1080})
            page2 = context2.new_page()

            page2.goto("https://cx.locobuzz.com/login")
            try:
                page2.wait_for_selector('input[formcontrolname="username"]:not([readonly])', timeout=8000)
            except PlaywrightTimeoutError:
                page2.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
            page2.fill('input[formcontrolname="username"]', "juw_csd")
            page2.get_by_role("button", name="Continue").click()
            page2.fill('input[formcontrolname="password"]', "Buzz@123")
            page2.get_by_role("button", name="Login").click()
            page2.wait_for_timeout(4000)

            print("🟢 Performing Approve actions...")
            page2.locator("a", has_text="search").click()
            page2.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
            page2.locator("a", has_text="search").click()
            page2.locator("#Post_3773015").get_by_text("Approve").click()
            page2.get_by_role("textbox", name="Enter note here").fill("Approving by pytest")
            page2.get_by_role("link", name="Attach Media").click()
            time.sleep(3)
            safe_click(page2, "//img[@src='https://images.locobuzz.com/LocoBuzzImages/SocialPostTriggerScheduling/reliancejiodb/002c68f8-4ff7-4678-b064-e6322f903bb8.png']")
            time.sleep(3)
            page2.get_by_role("button", name="Attach").click()
            page2.get_by_role("button", name="Save").click()

            print("✅ Both flows completed successfully!")

    except Exception as e:
        if 'page' in locals():
            take_screenshot(page, "test_failure")
        pytest.fail(f"Test failed: {e}")

    finally:
        if context: context.close()
        if browser: browser.close()
        if context2: context2.close()
        if browser2: browser2.close()
        print("🧹 Browser(s) closed safely for test_reply_and_escalate")
'''
# #works too
# import pytest
# import re
# import time
# import os
# from datetime import datetime
# from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
# from config.config import TICKET_ID

# # ---------------- Helper Functions ----------------
# def take_screenshot(page, step_name, screenshots_dir="screenshots"):
#     os.makedirs(screenshots_dir, exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     file_path = f"{screenshots_dir}/{step_name}_{timestamp}.png"
#     page.screenshot(path=file_path, full_page=True)
#     print(f"📸 Screenshot captured: {file_path}")
#     return file_path

# def safe_click(page, xpath, timeout=15000):
#     try:
#         page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
#         page.locator(f"xpath={xpath}").click()
#         print(f"✅ Clicked: {xpath}")
#     except PlaywrightTimeoutError as e:
#         print(f"❌ Timeout: Element not found for XPath {xpath}")
#         take_screenshot(page, f"safe_click_failure_{xpath.replace('/', '_')}")
#         raise e

# # ---------------- Agent Workflow ----------------
# @pytest.mark.playwright
# def test_agent_reply_and_escalate():
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)
#         context = browser.new_context(viewport={"width": 1920, "height": 1080})
#         page = context.new_page()

#         page.goto("https://cx.locobuzz.com/login")

#         # ---- Fill Username with Retry ----
#         page.wait_for_selector('input[formcontrolname="username"]', timeout=20000)
#         for attempt in range(5):
#             try:
#                 page.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
#                 page.fill('input[formcontrolname="username"]', "juw_agent")
#                 print("✅ Username filled successfully")
#                 break
#             except Exception:
#                 print(f"⚠️ Attempt {attempt+1}: Username input not editable yet, retrying...")
#                 page.wait_for_timeout(1000)
#         else:
#             raise Exception("❌ Failed to fill username after multiple attempts")

#         # ---- Click Continue to render password field ----
#         page.get_by_role("button", name="Continue").click()
#         page.wait_for_timeout(1000)  # wait for password field to render

#         # ---- Fill Password with Retry ----
#         page.wait_for_selector('input[formcontrolname="password"]', timeout=20000)
#         for attempt in range(5):
#             try:
#                 page.eval_on_selector('input[formcontrolname="password"]', "el => el.removeAttribute('readonly')")
#                 page.fill('input[formcontrolname="password"]', "Buzz@1234")
#                 print("✅ Password filled successfully")
#                 break
#             except Exception:
#                 print(f"⚠️ Attempt {attempt+1}: Password input not editable yet, retrying...")
#                 page.wait_for_timeout(1000)
#         else:
#             raise Exception("❌ Failed to fill password after multiple attempts")

#         # ---- Click Login ----
#         page.get_by_role("button", name="Login").click()
#         page.wait_for_timeout(4000)

#         # ---------------- Reply & Escalate ----------------
#         print("🟢 Performing Reply & Escalate actions...")
#         page.get_by_text("check_circleSelect all").click()
#         page.get_by_role("button", name="Submit").click()
#         page.get_by_text("On Hold ").click()

#         safe_click(page, "//a[.//mat-icon[text()=' search']]")
#         page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
#         safe_click(page, "//a[.//mat-icon[text()=' search']]")
#         page.wait_for_timeout(3000)

#         safe_click(page, "//span[normalize-space(text())='Reply']")
#         page.get_by_role("button", name="Discard").click()
#         page.get_by_role("button", name="Submit").click()

#         safe_click(page, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
#         page.get_by_role("option", name="Reply & Escalate").click()
#         page.get_by_role("textbox", name="Write Reply").fill("Reply & Escalate by pytest")
#         page.get_by_role("button", name="Next").click()
#         page.get_by_role("textbox", name="Write escalation note here...").fill("Escalate")
#         page.get_by_role("button", name="Send").click()

#         # ---------------- Logout ----------------
#         print("🔸 Logging out juw_agent...")
#         page.wait_for_timeout(2000)
#         page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).locator("a").click()
#         page.get_by_role("menuitem", name="Logout").click()
#         page.get_by_role("button", name="Logout").click()

#         context.close()
#         browser.close()
#         print("✅ Agent workflow completed successfully.")
# #-----------W2
# FINAL VERSION
"""import pytest
import re
import time
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config.config import TICKET_ID

@pytest.mark.playwright
def test_agent_reply_and_escalate():
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    def take_screenshot(page, step_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Remove characters not allowed in filenames
        safe_step_name = re.sub(r'[<>:"/\\|?*]', '_', step_name)
        file_path = f"{screenshots_dir}/{safe_step_name}_{timestamp}.png"
        page.screenshot(path=file_path, full_page=True)
        print(f"📸 Screenshot captured: {file_path}")
        return file_path

    def safe_click(page, xpath, timeout=15000):
        try:
            page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
            page.locator(f"xpath={xpath}").click()
            print(f"✅ Clicked: {xpath}")
        except PlaywrightTimeoutError as e:
            print(f"❌ Timeout: Element not found for XPath {xpath}")
            take_screenshot(page, f"safe_click_failure_{xpath}")
            raise e

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

            page.goto("https://cx.locobuzz.com/login")

            # ---- Fill Username ----
            page.wait_for_selector('input[formcontrolname="username"]', timeout=20000)
            for attempt in range(5):
                try:
                    page.eval_on_selector('input[formcontrolname="username"]', "el => el.removeAttribute('readonly')")
                    page.fill('input[formcontrolname="username"]', "juw_agent")
                    print("✅ Username filled successfully")
                    break
                except Exception:
                    print(f"⚠️ Attempt {attempt+1}: Username input not editable yet, retrying...")
                    page.wait_for_timeout(1000)
            else:
                raise Exception("❌ Failed to fill username after multiple attempts")

            # ---- Click Continue to show password ----
            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(1000)

            # ---- Fill Password ----
            page.wait_for_selector('input[formcontrolname="password"]', timeout=20000)
            for attempt in range(5):
                try:
                    page.eval_on_selector('input[formcontrolname="password"]', "el => el.removeAttribute('readonly')")
                    page.fill('input[formcontrolname="password"]', "Buzz@1234")
                    print("✅ Password filled successfully")
                    break
                except Exception:
                    print(f"⚠️ Attempt {attempt+1}: Password input not editable yet, retrying...")
                    page.wait_for_timeout(1000)
            else:
                raise Exception("❌ Failed to fill password after multiple attempts")

            # ---- Click Login ----
            page.get_by_role("button", name="Login").click()
            page.wait_for_timeout(4000)

            # ---------------- Reply & Escalate ----------------
            print("🟢 Performing Reply & Escalate actions...")

            # Select all & Submit
            page.get_by_text("check_circleSelect all").click()
            page.get_by_role("button", name="Submit").click()
            page.get_by_text("On Hold ").click()

            # Search Ticket
            safe_click(page, "//a[.//mat-icon[text()=' search']]")
            page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
            safe_click(page, "//a[.//mat-icon[text()=' search']]")
            page.wait_for_timeout(3000)

            # Reply
            safe_click(page, "//span[normalize-space(text())='Reply']")
            page.get_by_role("button", name="Discard").click()
            page.get_by_role("button", name="Submit").click()

            # Wait for any overlay/backdrop to disappear
            page.wait_for_selector("div.cdk-overlay-backdrop", state="detached", timeout=10000)

            # Reply Type selection
            safe_click(page, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
            page.get_by_role("option", name="Reply & Escalate").click()
            page.get_by_role("textbox", name="Write Reply").fill("Reply & Escalate by1 pytest")
            page.get_by_role("button", name="Next").click()

            # Escalation note
            page.get_by_role("textbox", name="Write escalation note here...").fill("Escalate")
            page.get_by_role("button", name="Send").click()

            # Logout
            print("🔸 Logging out juw_agent...")
            page.wait_for_timeout(2000)
            page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).locator("a").click()
            page.get_by_role("menuitem", name="Logout").click()
            page.get_by_role("button", name="Logout").click()

            print("✅ Agent workflow completed successfully!")

    except Exception as e:
        if 'page' in locals():
            take_screenshot(page, "test_failure")
        pytest.fail(f"Test failed: {e}")

    # No manual context/browser closing needed when using `with sync_playwright()`
    print("🧹 Browser closed safely for test_agent_reply_and_escalate")"""


# import sys
# import os
# # Add project root if needed (for config imports)
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# import re
# import time
# from datetime import datetime
# import pytest
# from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
# from config.config import TICKET_ID


# @pytest.mark.playwright
# def test_agent_reply_and_escalate():
#     screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
#     os.makedirs(screenshots_dir, exist_ok=True)

#     def take_screenshot(page, step_name):
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         safe_step_name = re.sub(r'[<>:"/\\|?*]', '_', step_name)
#         file_path = os.path.join(screenshots_dir, f"{safe_step_name}_{timestamp}.png")
#         page.screenshot(path=file_path, full_page=True)
#         print(f"📸 Screenshot captured: {file_path}")
#         return file_path

#     def safe_click(page, xpath, timeout=15000):
#         try:
#             page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
#             page.locator(f"xpath={xpath}").click()
#             print(f"✅ Clicked: {xpath}")
#         except PlaywrightTimeoutError as e:
#             print(f"❌ Timeout: Element not found for XPath {xpath}")
#             take_screenshot(page, f"safe_click_failure_{xpath}")
#             raise e

#     try:
#         with sync_playwright() as playwright:
#             browser = playwright.chromium.launch(headless=False)
#             context = browser.new_context(viewport={"width": 1920, "height": 1080})
#             page = context.new_page()
#             test_agent_reply_and_escalate.page = page  # conftest hook

#             # ---- Login ----
#             page.goto("https://cx.locobuzz.com/login")
#             for field, value in [("username", "juw_agent"), ("password", "Buzz@1234")]:
#                 page.wait_for_selector(f'input[formcontrolname="{field}"]', timeout=20000)
#                 for attempt in range(5):
#                     try:
#                         page.eval_on_selector(f'input[formcontrolname="{field}"]', "el => el.removeAttribute('readonly')")
#                         page.fill(f'input[formcontrolname="{field}"]', value)
#                         print(f"✅ {field} filled successfully")
#                         break
#                     except Exception:
#                         print(f"⚠️ Attempt {attempt+1}: {field} input not editable yet, retrying...")
#                         page.wait_for_timeout(1000)
#                 else:
#                     raise Exception(f"❌ Failed to fill {field} after multiple attempts")
#             page.get_by_role("button", name="Continue").click()
#             page.wait_for_timeout(1000)
#             page.get_by_role("button", name="Login").click()
#             page.wait_for_timeout(4000)

#             # ---- Reply & Escalate Workflow ----
#             print("🟢 Performing Reply & Escalate actions...")
#             page.get_by_text("check_circleSelect all").click()
#             page.get_by_role("button", name="Submit").click()
#             page.get_by_text("On Hold ").click()

#             # Search Ticket
#             safe_click(page, "//a[.//mat-icon[text()=' search']]")
#             page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
#             safe_click(page, "//a[.//mat-icon[text()=' search']]")
#             page.wait_for_timeout(3000)

#             # Reply
#             safe_click(page, "//span[normalize-space(text())='Reply']")
#             page.get_by_role("button", name="Discard").click()
#             page.get_by_role("button", name="Submit").click()
#             page.wait_for_selector("div.cdk-overlay-backdrop", state="detached", timeout=10000)

#             # Reply Type → Reply & Escalate
#             safe_click(page, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
#             page.get_by_role("option", name="Reply & Escalate").click()
#             page.get_by_role("textbox", name="Write Reply").fill("Reply & Escalate by pytest")
#             page.get_by_role("button", name="Next").click()

#             # Escalation note
#             page.get_by_role("textbox", name="Write escalation note here...").fill("Escalate")
#             page.get_by_role("button", name="Send").click()

#             # Logout
#             print("🔸 Logging out juw_agent...")
#             page.get_by_role("button", name="Account").click()
#             page.get_by_role("menuitem", name="Logout").click()

#             print("✅ Agent workflow completed successfully!")

#     except Exception as e:
#         if 'page' in locals():
#             take_screenshot(page, "test_failure")
#         pytest.fail(f"Test failed: {e}")

#     finally:
#         if 'browser' in locals():
#             browser.close()
#             print("🧹 Browser closed safely")
#         if __name__ == "__main__":
#                 test_agent_reply_and_escalate()















# # tests/playwright/test_reply_and_escalate.py
# import sys
# import os
# # Add project root to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# import re

# import time
# from datetime import datetime
# from locobuzz_login import locobuzzLogin
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# import pytest
# from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
# from config.config import TICKET_ID


# @pytest.mark.playwright
# def test_reply_and_escalate():
#     screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
#     os.makedirs(screenshots_dir, exist_ok=True)

#     def take_screenshot(page, step_name):
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         safe_step_name = re.sub(r'[<>:"/\\|?*]', '_', step_name)
#         file_path = os.path.join(screenshots_dir, f"escalate_{safe_step_name}_{timestamp}.png")
#         page.screenshot(path=file_path, full_page=True)
#         print(f"📸 Screenshot captured: {file_path}")
#         return file_path

#     def safe_click(page, xpath, timeout=15000):
#         try:
#             page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
#             page.locator(f"xpath={xpath}").click()
#             print(f"✅ Clicked: {xpath}")
#         except PlaywrightTimeoutError:
#             print(f"❌ Timeout: Element not found for XPath {xpath}")
#             take_screenshot(page, f"safe_click_failure_{xpath}")
#             raise

#     try:
#         with sync_playwright() as playwright:
#             browser = playwright.chromium.launch(headless=False)
#             context = browser.new_context(viewport={"width": 1920, "height": 1080})
#             page = context.new_page()
#             test_reply_and_escalate.page = page

#             # ---- Login ----
#             # browser = locobuzzLogin("juw_agent", "Buzz@1234")
#             # test_reply_and_escalate.browser = browser  # attach browser for conftest screenshot hook
#             # wait = WebDriverWait(browser, 15)
#             page.goto("https://cx.locobuzz.com/login")
#             # page.wait_for_selector('input[formcontrolname="username"]', timeout=10000)
#             page.evaluate("document.querySelector('input[formcontrolname=\"username\"]').value = 'juw_agent'")
#             page.fill('input[formcontrolname="username"]', "juw_agent")
#             page.get_by_role("button", name="Continue").click()
#             page.wait_for_selector('input[formcontrolname="password"]', timeout=10000)
#             page.fill('input[formcontrolname="password"]', "Buzz@1234")
#             page.get_by_role("button", name="Login").click()
#             page.wait_for_timeout(4000)

#             print("🟢 Performing Reply & Escalate actions...")

#             # Select all & Submit → On Hold
#             page.get_by_text("check_circleSelect all").click()
#             page.get_by_role("button", name="Submit").click()
#             page.get_by_text("On Hold ").click()

#             # Search Ticket
#             safe_click(page, "//a[.//mat-icon[text()=' search']]")
#             page.get_by_role("textbox", name="Search for a Ticket ID,").fill(TICKET_ID)
#             safe_click(page, "//a[.//mat-icon[text()=' search']]")
#             page.wait_for_timeout(3000)

#             # Click Reply
#             safe_click(page, f"//div[contains(., '{TICKET_ID}')]//span[normalize-space(text())='Reply']")
#             page.get_by_role("button", name="Discard").click()
#             page.get_by_role("button", name="Submit").click()
#             page.wait_for_selector("div.cdk-overlay-backdrop", state="detached", timeout=10000)

#             # Reply Type → Reply & Escalate
#             safe_click(page, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")
#             page.get_by_role("option", name="Reply & Escalate").click()
#             page.get_by_role("textbox", name="Write Reply").fill("Reply & Escalate by pytest")
#             page.get_by_role("button", name="Next").click()

#             # Escalation note
#             page.get_by_role("textbox", name="Write escalation note here...").fill("Escalate")
#             page.get_by_role("button", name="Send").click()

#             print("✅ Reply & Escalate completed successfully!")

#     except Exception as e:
#         if 'page' in locals():
#             take_screenshot(page, "test_failure")
#         pytest.fail(f"Test failed: {e}")

#     finally:
#         if 'browser' in locals():
#             browser.close()
#             print("🧹 Browser closed safely")

# if __name__ == "__main__":
#     test_reply_and_escalate()





#LAST WORKING CODE
# import sys
# import os
# # Add project root for imports
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# import time
# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# from locobuzz_login import locobuzzLogin
# from config.config import TICKET_ID

# @pytest.mark.selenium
# def test_reply_and_escalate():
#     browser = None
#     screenshots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots")
#     os.makedirs(screenshots_dir, exist_ok=True)

#     def safe_click(element):
#         browser.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
#         browser.execute_script("arguments[0].click();", element)

#     try:
#         # ---- LOGIN ----
#         browser = locobuzzLogin("juw_agent", "Buzz@1234")
#         test_reply_and_escalate.browser = browser
#         wait = WebDriverWait(browser, 15)

#         # ---- Select All & Submit ----
#         selectAll = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Select all']")))
#         safe_click(selectAll)

#         applyBtn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Submit ']")))
#         safe_click(applyBtn)

#         # ---- More → On Hold tab ----
#         # moreBtn = wait.until(EC.element_to_be_clickable(
#         #     (By.XPATH, "(//a[@aria-haspopup='menu' and contains(normalize-space(.), 'More')])[1]")))
#         # safe_click(moreBtn)

#         onHoldTab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='On Hold ']")))
#         safe_click(onHoldTab)

#         # ---- Search Ticket ----
#         searchBtn = wait.until(EC.presence_of_element_located((By.XPATH, "//a[.//mat-icon[text()=' search']]")))
#         safe_click(searchBtn)

#         searchField = wait.until(EC.presence_of_element_located(
#             (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')))
#         searchField.clear()
#         searchField.send_keys(TICKET_ID)
#         safe_click(searchBtn)
#         time.sleep(2)

#         # ---- Click Reply ----
#         replyBtn = wait.until(EC.element_to_be_clickable(
#             (By.XPATH, "//span[@class='custom__foot--button post__pill'][.//mat-icon[text()='reply ']]")))
#         safe_click(replyBtn)

#         # ---- Discard & Submit to reset dialog ----
#         discardBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Discard ']")))
#         safe_click(discardBtn)

#         submitBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Submit ']")))
#         safe_click(submitBtn)

#         time.sleep(5)  # wait for any overlay/backdrop to disappear

#         # ---- Reply Type → Reply & Escalate ----
#         replyTypeDropdown = wait.until(EC.element_to_be_clickable(
#             (By.XPATH, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")))
#         safe_click(replyTypeDropdown)

#         replyEscalate = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='  Reply & Escalate ']")))
#         safe_click(replyEscalate)

#         # ---- Write reply ----
#         writeReply = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write Reply"]')))
#         writeReply.send_keys("Reply & Escalate via pytest")

#         # ---- Next & Escalation note ----
#         nextBtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()=" Next "]')))
#         safe_click(nextBtn)

#         # userDropdown = wait.until(EC.element_to_be_clickable(By.XPATH, '//input[@aria-haspopup="menu"]'))
#         # userDropdown.click()
#         # time.sleep(1)  # wait for options to render

#         writeEscNote = wait.until(EC.presence_of_element_located(
#             (By.XPATH, '//textarea[@placeholder="Write escalation note here..."]')))
#         writeEscNote.send_keys("Escalating via pytest")
#         time.sleep(3)

#         sendBtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()=" Send "]')))
#         safe_click(sendBtn)

#         time.sleep(2)
#         assert True, "Reply & Escalate test completed successfully"

#     except TimeoutException as e:
#         pytest.fail(f"Timeout or Selenium failure: {e}")

#     finally:
#         if browser:
#             browser.quit()

# if __name__ == "__main__":
#     test_reply_and_escalate()




#20OCT25
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
TICKET_ID = TICKET_IDS["facebook"]


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
            browser = locobuzzLogin("facebook_agent", "Locobuzz@123")
            test_reply_and_escalate.browser = browser
            wait = WebDriverWait(browser, 15)

        with allure.step("Select All & Submit"):
            selectAll = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Select all']")))
            safe_click(selectAll)

            applyBtn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Submit ']")))
            safe_click(applyBtn)
            time.sleep(5)

        # with allure.step("More → On Hold tab"):
        #     moreBtn = wait.until(EC.element_to_be_clickable(
        #         (By.XPATH, "(//a[@aria-haspopup='menu' and contains(normalize-space(.), 'More')])[1]")))
        #     safe_click(moreBtn)

        with allure.step("On Hold tab"):
            onHoldTab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='On Hold ']")))
            safe_click(onHoldTab)

        with allure.step("Search Ticket"):
            searchBtn = wait.until(EC.presence_of_element_located((By.XPATH, "//a[.//mat-icon[text()=' search']]")))
            safe_click(searchBtn)

            searchField = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')))
            searchField.clear()
            searchField.send_keys(TICKET_ID)
            safe_click(searchBtn)
            time.sleep(2)

        with allure.step("Click Reply"):
            replyBtn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[@class='custom__foot--button post__pill'][.//mat-icon[text()='reply ']]")))
            safe_click(replyBtn)

        with allure.step("Discard & Submit to reset dialog"):
            discardBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Discard ']")))
            safe_click(discardBtn)

            submitBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Submit ']")))
            safe_click(submitBtn)

        time.sleep(5)  # wait for any overlay/backdrop to disappear

        with allure.step("Reply Type → Reply & Escalate"):
            replyTypeDropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//mat-label[text()='Reply Type']/ancestor::mat-form-field//mat-select")))
            safe_click(replyTypeDropdown)

            replyEscalate = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='  Reply & Escalate ']")))
            safe_click(replyEscalate)

        with allure.step("Write reply"):
            writeReply = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Write Reply"]')))
            writeReply.send_keys("Reply & Escalate via pytest")

        with allure.step("Next & Escalation note"):
            nextBtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()=" Next "]')))
            safe_click(nextBtn)

            # userDropdown = wait.until(EC.element_to_be_clickable(By.XPATH, '//mat-label[normalize-space()="Escalate To"]/ancestor::mat-form-field//input'))
            # safe_click(userDropdown)
            # time.sleep(1)  # wait for options to render

            # facebookCSD = wait.until(EC.element_to_be_clickable(By.XPATH, '//span[contains(text(),"facebook csd")]'))
            # safe_click(facebookCSD)
            # time.sleep(1)

            writeEscNote = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//textarea[@placeholder="Write escalation note here..."]')))
            writeEscNote.send_keys("Escalating via pytest")
            time.sleep(3)

        with allure.step("Send"):
            sendBtn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()=" Send "]')))
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
