#20OCT25
import time
import pytest
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.selenium.selenium_helpers import safe_click, safe_fill
from locobuzz_login.CX_login import locobuzzLogin
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from config.config import TICKET_IDS
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements
TICKET_ID = TICKET_IDS["twitter"]
from selenium.common.exceptions import StaleElementReferenceException


def click_with_retry(wait, locator, retries=3, delay=0.5):
    """Helper function to retry clicks on stale elements."""
    for attempt in range(retries):
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return
        except StaleElementReferenceException:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise


@allure.title("Closed Ticket Flow - bilal_superadmin & juw_agent")
@allure.description(
    "Bilal_superadmin disables/enables ticket disposition, juw_agent opens and closes ticket, "
    "then bilal_superadmin enables disposition if needed."
)
@pytest.mark.regression
def test_closed_ticket_flow():
    # ---------------- STEP 1: bilal_superadmin login ----------------
    with allure.step("Login as bilal_superadmin (check/disable feature if needed)"):
        driver = locobuzzLoginPreProd("bilal_superadmin", "Buzz@1234")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="bilal_superadmin_login", attachment_type=allure.attachment_type.PNG)

        try:
            # Wait for any overlays to disappear
            time.sleep(3)
            try:
                wait.until(EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".cdk-overlay-backdrop")))
            except:
                pass  # Overlay might not exist
            
            # Navigate to Account Settings → Ticket Disposition
            profile = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.PROFILE_IMAGE)))
            profile.click()
            time.sleep(2)
            accountSettings = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.ACCOUNT_SETTINGS)))
            accountSettings.click()
            time.sleep(2)

            search_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_BOX)))
            search_box.send_keys("ticket disposition")
            safe_click(driver, wait, (By.XPATH, ReplyPanelPageElements.TICKET_DISPOSITION_LINK))
            time.sleep(2)

            # Toggle off if active
            feature_active = driver.find_elements(By.XPATH, ReplyPanelPageElements.FEATURE_ACTIVE)
            if feature_active:
                toggle_label = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, ReplyPanelPageElements.TOGGLE_SWITCH_LABEL)))
                safe_click(driver, wait, toggle_label)
                yesBtn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.YES_BUTTON)))
                safe_click(driver, wait, yesBtn)
                print("✅ Feature was active, now disabled.")
                time.sleep(2)
            else:
                print("ℹ️ Feature already inactive, skipping toggle.")

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="bilal_superadmin_error", attachment_type=allure.attachment_type.PNG)
            driver.quit()
            pytest.fail(f"bilal_superadmin initial flow failed: {e}")
        finally:
            driver.quit()
            time.sleep(1)

    # ---------------- STEP 2: juw_agent login ----------------
    with allure.step("Login as juw_agent and perform ticket actions"):
        driver = locobuzzLoginPreProd("juw_agent", "Buzz@1234")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="juw_agent_login", attachment_type=allure.attachment_type.PNG)

        try:
            # Select all and submit
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.SELECT_ALL_BUTTON))
            click_with_retry(wait, (By.XPATH, LoginPageElements.SUBMIT_BUTTON))

            # Search ticket
            search_btn = (By.XPATH, ReplyPanelPageElements.SEARCH_ICON)
            search_field = (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)
            click_with_retry(wait, search_btn)
            search_input = wait.until(EC.presence_of_element_located(search_field))
            search_input.clear()
            search_input.send_keys(TICKET_ID)
            click_with_retry(wait, search_btn)
            print(f"🔍 Searched ticket: {TICKET_ID}")
            time.sleep(2)

            # Open closed tickets
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.MORE_OPTIONS_ICON))
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.CLOSED_TICKETS_TAB))
            time.sleep(3)  # Wait for closed tickets to load
            
            # Scroll to and click account box icon
            account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
            time.sleep(1)
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON))
            time.sleep(1)

            # Overview & ticket status
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.OVERVIEW_TAB))
            ticket_status = (By.XPATH, ReplyPanelPageElements.TICKET_STATUS_DROPDOWN)
            click_with_retry(wait, ticket_status)
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.OPEN_STATUS_OPTION))
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)
            # Open tab → Direct Close
            driver.refresh()
            time.sleep(3)
            # open_tab = (By.XPATH, ReplyPanelPageElements.OPEN_TAB)
            # click_with_retry(wait, open_tab)
            click_with_retry(wait, (By.XPATH, "//span[text()='Direct Close']"))
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.YES_BUTTON))

            allure.attach(driver.get_screenshot_as_png(), name="juw_agent_actions", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="juw_agent_error", attachment_type=allure.attachment_type.PNG)
            driver.quit()
            pytest.fail(f"juw_agent flow failed: {e}")
        finally:
            driver.quit()
            time.sleep(1)

    # ---------------- STEP 3: bilal_superadmin login again ----------------
    with allure.step("Login as bilal_superadmin to enable feature if needed"):
        driver = locobuzzLoginPreProd("bilal_superadmin", "Buzz@1234")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="bilal_superadmin_login_2", attachment_type=allure.attachment_type.PNG)

        try:
            profile = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.PROFILE_IMAGE)))
            profile.click()
            time.sleep(2)
            accountSettings = wait.until(EC.presence_of_element_located(
                (By.XPATH, ReplyPanelPageElements.ACCOUNT_SETTINGS)))
            accountSettings.click()
            time.sleep(2)

            search_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_BOX)))
            search_box.send_keys("ticket disposition")
            safe_click(driver, wait, (By.XPATH, ReplyPanelPageElements.TICKET_DISPOSITION_LINK))
            time.sleep(2)

            feature_inactive = driver.find_elements(By.XPATH, ReplyPanelPageElements.FEATURE_INACTIVE)
            if feature_inactive:
                toggle_label = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, ReplyPanelPageElements.TOGGLE_SWITCH_LABEL)))
                safe_click(driver, wait, toggle_label)
                print("✅ Feature was inactive, now activated.")
                time.sleep(2)
            else:
                print("ℹ️ Feature already active, skipping toggle.")

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="bilal_superadmin_error_2", attachment_type=allure.attachment_type.PNG)
            driver.quit()
            pytest.fail(f"bilal_superadmin second flow failed: {e}")
        finally:
            driver.quit()
            time.sleep(1)

    # ---------------- STEP 4: juw_agent login for next steps ----------------
    with allure.step("Login as juw_agent (ready for next steps)"):
        driver = locobuzzLoginPreProd("juw_agent", "Buzz@1234")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="juw_agent_login_final", attachment_type=allure.attachment_type.PNG)

        print("ℹ️ juw_agent logged in and ready for next steps.")

        try:
            # Select all and submit
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.SELECT_ALL_BUTTON))
            click_with_retry(wait, (By.XPATH, LoginPageElements.SUBMIT_BUTTON))

            # Search ticket
            search_btn = (By.XPATH, ReplyPanelPageElements.SEARCH_ICON)
            search_field = (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)
            click_with_retry(wait, search_btn)
            search_input = wait.until(EC.presence_of_element_located(search_field))
            search_input.clear()
            search_input.send_keys(TICKET_ID)
            click_with_retry(wait, search_btn)
            print(f"🔍 Searched ticket: {TICKET_ID}")
            time.sleep(2)

            # Open closed tickets
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.MORE_OPTIONS_ICON))
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.CLOSED_TICKETS_TAB))
            time.sleep(3)  # Wait for closed tickets to load
            
            # Scroll to and click account box icon
            account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
            time.sleep(1)
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON))
            time.sleep(1)

            # Overview & ticket status
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.OVERVIEW_TAB))
            ticket_status = (By.XPATH, ReplyPanelPageElements.TICKET_STATUS_DROPDOWN)
            click_with_retry(wait, ticket_status)
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.OPEN_STATUS_OPTION))
            time.sleep(2)
            # click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.CLOSE_ICON))
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)

            # Refresh and reopen ticket
            driver.refresh()
            time.sleep(3)
            
            # # Click on the ticket again after refresh
            # account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
            # driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
            # time.sleep(1)
            # click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON))
            # time.sleep(2)

            # Open tab → Direct Close
            click_with_retry(wait, (By.XPATH, "//span[text()='Direct Close']"))

            # Disposition selection
            dispositionName = (By.XPATH, ReplyPanelPageElements.DISPOSITION_NAME_DROPDOWN)
            click_with_retry(wait, dispositionName)
            productRelated = (By.XPATH, ReplyPanelPageElements.PRODUCT_RELATED_OPTION)
            click_with_retry(wait, productRelated)

            # Note and Save & Close
            noteField = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ENTER_NOTE_TEXTAREA)))
            noteField.clear()
            noteField.send_keys("Closing ticket with disposition on")
            click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.SAVE_AND_CLOSE_BUTTON))

            allure.attach(driver.get_screenshot_as_png(), name="juw_agent_actions_final", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="juw_agent_error_final", attachment_type=allure.attachment_type.PNG)
            driver.quit()
            pytest.fail(f"juw_agent final flow failed: {e}")
        finally:
            driver.quit()
            time.sleep(1)

        

