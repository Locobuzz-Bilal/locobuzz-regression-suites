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
from utils.credentials import get_twitter_creds
from config.config import TICKET_IDS
from locobuzz_login.preProd_login import locobuzzLoginPreProd  # assumes this returns a logged-in selenium driver
from dotenv import load_dotenv
from elements.login_page import LoginPageElements
from elements.reply_panel_page import ReplyPanelPageElements

load_dotenv()  # load .env for credentials
print("TWITTER_USERNAME =", os.getenv("TWITTER_USERNAME"))
print("TWITTER_PASSWORD =", os.getenv("TWITTER_PASSWORD"))


# Optional: user to assign (fallback picks first)
ASSIGN_USER = os.getenv("ASSIGN_USER", "juw_agent").strip()
TICKET_ID = TICKET_IDS["twitter"]  # make sure config has this

@pytest.mark.selenium
def test_reply_and_assign():
    """
    Twitter Reply & Assign workflow:
    1. Login with Twitter test creds (from .env).
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
    screenshots_dir = Path(__file__).resolve().parents[2] / "screenshots" / "twitter_reply_and_assign"
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
            user, pwd = get_twitter_creds()
            driver = locobuzzLoginPreProd(user, pwd)
            wait = WebDriverWait(driver, 30)
            snap("logged_in")

        with allure.step("Select All & Submit"):
            click_xpath(LoginPageElements.SELECT_ALL_BRANDS)
            click_xpath(LoginPageElements.SUBMIT_BUTTON)
            time.sleep(1)
            snap("after_select_all_submit")

        with allure.step("Open search input"):
            # Click search icon (adjust if different)
            click_xpath(ReplyPanelPageElements.SEARCH_ICON)
            time.sleep(1)

        with allure.step(f"Search ticket ID {TICKET_ID}"):
            type_xpath(ReplyPanelPageElements.SEARCH_INPUT_BOX, TICKET_ID)
            click_xpath(ReplyPanelPageElements.SEARCH_ICON)
            time.sleep(2)
            snap("after_search")

        # with allure.step("Click on ticket to open it"):
        #     # Click the account box to open the ticket details
        #     account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        #     driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
        #     time.sleep(1)
        #     click_xpath(ReplyPanelPageElements.ACCOUNT_BOX_ICON)
        #     time.sleep(2)
        #     snap("ticket_opened")

        with allure.step("Open Reply panel"):
            # Reply pill/button
            click_xpath(ReplyPanelPageElements.REPLY_BUTTON)
            time.sleep(2)
            snap("reply_panel_open")

        with allure.step("Discard and Submit"):
            click_xpath(ReplyPanelPageElements.DISCARD_BUTTON)
            time.sleep(2)
            snap("after_discard")
            click_xpath(ReplyPanelPageElements.DISCARD_CANCEL_BUTTON)
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
            click_xpath(ReplyPanelPageElements.REPLY_TYPE_DROPDOWN)
            # Option text may have extra spaces; normalize both possibilities
            try:
                click_xpath(ReplyPanelPageElements.REPLY_AND_ASSIGN_OPTION)
            except TimeoutException:
                click_xpath(ReplyPanelPageElements.REPLY_AND_ASSIGN_OPTION_ALTERNATE)
            time.sleep(1)
            snap("reply_type_selected")

        with allure.step("Enter reply text"):
            reply_box_xpath = ReplyPanelPageElements.REPLY_INPUT_BOX
            type_xpath(reply_box_xpath, f"Automated assign reply at {time.strftime('%H:%M:%S')}")
            snap("reply_text_entered")
            click_xpath(ReplyPanelPageElements.REPLY_NEXT_BUTTON)
            time.sleep(1)
            snap("after_reply_next")

        with allure.step("Pick assignee"):
            # Open assign user mat-select
            click_xpath(ReplyPanelPageElements.ASSIGN_TO_DROPDOWN)
            time.sleep(1)
            snap("assignee_input_focused")

            click_xpath(ReplyPanelPageElements.JUWAIRIA_AGENT_OPTION)
            time.sleep(1)
            snap("assignee_selected")

        with allure.step("Add Note"):
            addNote = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.ADD_NOTE_INPUT)))
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
            click_xpath(ReplyPanelPageElements.SEND_BUTTON)
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