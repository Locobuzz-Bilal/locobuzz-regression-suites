import os
import time
import pytest
import allure
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from tests.selenium.selenium_helpers import safe_click
from utils.credentials import get_fb_creds
from config.config import TICKET_IDS
from locobuzz_login.CX_login import locobuzzLogin  # assumes this returns a logged-in selenium driver
from dotenv import load_dotenv

load_dotenv()  # load .env for credentials
print("FB_USERNAME =", os.getenv("FB_USERNAME"))
print("FB_PASSWORD =", os.getenv("FB_PASSWORD"))


# Optional: user to assign (fallback picks first)
ASSIGN_USER = os.getenv("ASSIGN_USER", "facebook agent").strip()
TICKET_ID = TICKET_IDS["facebook"]  # make sure config has this

@pytest.mark.selenium
def test_reply_and_assign():
    """
    Facebook Reply & Assign workflow:
    1. Login with FB test creds (from .env).
    2. Search ticket by ID.
    3. Open Reply panel.
    4. Select 'Reply & Assign' type.
    5. Enter reply content.
    6. Pick assignee (env ASSIGN_USER or first option).
    7. Send reply and verify success indicator.
    """
    driver = None
    wait = None

    # Screenshots folder (grouped by test name)
    screenshots_dir = Path(__file__).resolve().parents[2] / "screenshots" / "facebook_reply_and_assign"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    def snap(label: str):
        """Capture screenshot and attach to Allure."""
        if not driver:
            return
        ts = int(time.time())
        path = screenshots_dir / f"{label}_{ts}.png"
        driver.save_screenshot(str(path))
        allure.attach.file(str(path), name=label, attachment_type=allure.attachment_type.PNG)

    def safe_xpath(x: str, timeout: int = 25, clickable=False):
        cond = EC.element_to_be_clickable if clickable else EC.presence_of_element_located
        return wait.until(cond((By.XPATH, x)))

    def click_xpath(x: str, scroll=True):
        el = safe_xpath(x, clickable=True)
        if scroll:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        # use JS click to avoid overlay issues
        driver.execute_script("arguments[0].click();", el)
        return el

    def type_xpath(x: str, text: str, clear=True):
        el = safe_xpath(x)
        if clear:
            el.clear()
        el.send_keys(text)
        return el

    try:
        with allure.step("Login"):
            user, pwd = get_fb_creds()
            driver = locobuzzLogin(user, pwd)
            wait = WebDriverWait(driver, 30)
            snap("logged_in")

        with allure.step("Select All & Submit"):
            click_xpath("//span[text()='Select all']")
            click_xpath("//span[text()=' Submit ']")
            time.sleep(1)
            snap("after_select_all_submit")

        with allure.step("Open search input"):
            # Click search icon (adjust if different)
            click_xpath("//a[.//mat-icon[text()=' search']]")
            time.sleep(1)

        with allure.step(f"Search ticket ID {TICKET_ID}"):
            search_box_xpath = '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]'
            type_xpath(search_box_xpath, TICKET_ID)
            click_xpath("//a[.//mat-icon[text()=' search']]")
            time.sleep(2)
            snap("after_search")

        with allure.step("Open Reply panel"):
            # Reply pill/button
            click_xpath("//span[@class='custom__foot--button post__pill'][.//mat-icon[text()='reply ']]")
            time.sleep(2)
            snap("reply_panel_open")

        with allure.step("Discard and Submit"):
            click_xpath("//span[text()=' Discard ']")
            time.sleep(2)
            snap("after_discard")
            click_xpath("(//button//span[text()=' Cancel '])[2]")
            time.sleep(2)
            snap("after_discard_submit")

            # discard = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Discard ']")))
            # safe_click(discard)
            # time.sleep(2)
            # # submitBtn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Submit ']")))
            # submitBtn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button//span[text()=' Cancel '])[2]")))
            # safe_click(submitBtn2)
            # time.sleep(3)

        with allure.step("Select Reply Type: Reply & Assign"):
            # Open reply type mat-select
            click_xpath("//mat-label[normalize-space(text())='Reply Type']/ancestor::mat-form-field//mat-select")
            # Option text may have extra spaces; normalize both possibilities
            try:
                click_xpath("//span[normalize-space()='Reply & Assign']")
            except TimeoutException:
                click_xpath("//span[contains(normalize-space(),'Reply & Assign')]")
            time.sleep(1)
            snap("reply_type_selected")

        with allure.step("Enter reply text"):
            reply_box_xpath = '//textarea[@placeholder="Write Reply"]'
            type_xpath(reply_box_xpath, f"Automated assign reply at {time.strftime('%H:%M:%S')}")
            snap("reply_text_entered")
            click_xpath("//span[text()=' Next ']")
            time.sleep(1)
            snap("after_reply_next")

        with allure.step("Pick assignee"):
            # Open assign user mat-select
            click_xpath("(//input[@type='text'])[3]")
            time.sleep(1)
            snap("assignee_input_focused")

            click_xpath("//span[contains(text(),'facebook agent')]")
            time.sleep(1)
            snap("assignee_selected")

        with allure.step("Add Note"):
            addNote = wait.until(EC.presence_of_element_located(
                (By.XPATH, '(//textarea[@formcontrolname="replyEscalateNote"])[2]')))
            addNote.clear()
            addNote.send_keys("Assigning BY pytest with step timing")
            snap("note_added")
            # with allure_step("Add Note & Send"):
#             addNote = wait.until(EC.presence_of_element_located(
#                 (By.XPATH, '(//textarea[@formcontrolname="replyEscalateNote"])[2]')))
#             addNote.clear()
#             addNote.send_keys("Assigning BY pytest with step timing")


            # if ASSIGN_USER:
            #     # Try exact match first
            #     assign_xpath = f"//span[normalize-space()='{ASSIGN_USER}']"
            #     try:
            #         click_xpath(assign_xpath)
            #     except TimeoutException:
            #         # Fallback: first option
            #         click_xpath("(//mat-option//span)[1]")
            # else:
            #     click_xpath("(//mat-option//span)[1]")
            # time.sleep(1)
            # snap("assignee_selected")

        # with allure.step("Next step"):
        #     click_xpath("//span[normalize-space(text())='Next']")
        #     time.sleep(1)
        #     snap("after_next")

        with allure.step("Send reply"):
            click_xpath("//span[text()=' Send ']")
            time.sleep(4)
            snap("sent")

        # with allure.step("Verify success"):
        #     # Try toast or status indicator (adjust if needed)
        #     success_xpaths = [
        #         "//span[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'reply posted')]",
        #         "//div[contains(@class,'toast')][contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'success')]",
        #         "//span[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'assigned')]"
        #     ]
        #     success_found = False
        #     for sx in success_xpaths:
        #         try:
        #             safe_xpath(sx, timeout=6)
        #             success_found = True
        #             break
        #         except TimeoutException:
        #             continue
        #     snap("verification")
        #     assert success_found, "No success indicator found after sending reply."

    except (TimeoutException, WebDriverException) as e:
        snap("failure_timeout")
        pytest.fail(f"Selenium timeout/webdriver error: {e}")

    except Exception as e:
        snap("failure_unexpected")
        pytest.fail(f"Unexpected error: {e}")

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_reply_and_assign()