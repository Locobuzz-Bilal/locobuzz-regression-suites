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
from config.config import TICKET_IDS
TICKET_ID = TICKET_IDS["facebook"]
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


@allure.title("Closed Ticket Flow - bilal_superadmin & facebook_agent")
@allure.description(
    "fbsuperadmin disables/enables ticket disposition, facebook_agent opens and closes ticket, "
    "then fbsuperadmin enables disposition if needed."
)
@pytest.mark.regression
def test_closed_ticket_flow():
    # ---------------- STEP 1: fbsuperadmin login ----------------
    with allure.step("Login as fbsuperadmin (check/disable feature if needed)"):
        driver = locobuzzLogin("fbsuperadmin", "Locobuzz@123")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="fbsuperadmin_login", attachment_type=allure.attachment_type.PNG)

        try:
            # Navigate to Account Settings → Ticket Disposition
            profile = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//img[@src='assets/images/agentimages/sample-image.svg']")))
            profile.click()
            time.sleep(2)
            accountSettings = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Account Settings']")))
            accountSettings.click()
            time.sleep(2)

            search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
            search_box.send_keys("ticket disposition")
            safe_click(driver, wait, (By.XPATH, "//a[@href='/account/ticketdisposition']"))
            time.sleep(2)

            # Toggle off if active
            feature_active = driver.find_elements(By.XPATH, "//p[contains(text(),'Feature Active')]")
            if feature_active:
                toggle_label = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[@class='rounded-toggle-switch']/label[@for='rounded-toggle-switch-ticketDispositions']")))
                safe_click(driver, wait, toggle_label)
                yesBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Yes']")))
                safe_click(driver, wait, yesBtn)
                print("✅ Feature was active, now disabled.")
                time.sleep(2)
            else:
                print("ℹ️ Feature already inactive, skipping toggle.")

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="fbsuperadmin_error", attachment_type=allure.attachment_type.PNG)
            driver.quit()
            pytest.fail(f"fbsuperadmin initial flow failed: {e}")
        finally:
            driver.quit()
            time.sleep(1)

    # ---------------- STEP 2: facebook_agent login ----------------
    with allure.step("Login as facebook_agent and perform ticket actions"):
        driver = locobuzzLogin("facebook_agent", "Locobuzz@123")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="facebook_agent_login", attachment_type=allure.attachment_type.PNG)

        try:
            # Select all and submit
            click_with_retry(wait, (By.XPATH, "//span[text()='Select all']"))
            click_with_retry(wait, (By.XPATH, "//span[text()=' Submit ']"))

            # Search ticket
            search_btn = (By.XPATH, "//a[.//mat-icon[text()=' search']]")
            search_field = (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')
            click_with_retry(wait, search_btn)
            search_input = wait.until(EC.presence_of_element_located(search_field))
            search_input.clear()
            search_input.send_keys(TICKET_ID)
            click_with_retry(wait, search_btn)
            print(f"🔍 Searched ticket: {TICKET_ID}")
            time.sleep(2)

            # Open closed tickets
            click_with_retry(wait, (By.XPATH, "//span[contains(text(),'Closed Tickets')]"))
            click_with_retry(wait, (By.XPATH, "//mat-icon[text()='account_box']"))
            time.sleep(1)

            # Overview & ticket status
            click_with_retry(wait, (By.XPATH, "//div[@role='tab' and .='Overview']"))
            ticket_status = (By.XPATH,
                "//mat-label[normalize-space()='Ticket Status']/ancestor::mat-form-field//div[contains(@class,'mat-mdc-select-trigger')]")
            click_with_retry(wait, ticket_status)
            click_with_retry(wait, (By.XPATH, "//mat-option//span[normalize-space()='Open']"))
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.5)

            # Open tab → Direct Close
            open_tab = (By.XPATH, "//li[.//span[@class='post-option__name' and normalize-space(text())='Open']]")
            click_with_retry(wait, open_tab)
            click_with_retry(wait, (By.XPATH, "//span[text()='Direct Close']"))
            click_with_retry(wait, (By.XPATH, "//span[text()='Yes']"))

            allure.attach(driver.get_screenshot_as_png(), name="facebook_agent_actions", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="facebook_agent_error", attachment_type=allure.attachment_type.PNG)
            driver.quit()
            pytest.fail(f"facebook_agent flow failed: {e}")
        finally:
            driver.quit()
            time.sleep(1)

    # ---------------- STEP 3: fbsuperadmin login again ----------------
    with allure.step("Login as fbsuperadmin to enable feature if needed"):
        driver = locobuzzLogin("fbsuperadmin", "Locobuzz@123")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="fbsuperadmin_login_2", attachment_type=allure.attachment_type.PNG)

        try:
            profile = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//img[@src='assets/images/agentimages/sample-image.svg']")))
            profile.click()
            time.sleep(2)
            accountSettings = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Account Settings']")))
            accountSettings.click()
            time.sleep(2)

            search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
            search_box.send_keys("ticket disposition")
            safe_click(driver, wait, (By.XPATH, "//a[@href='/account/ticketdisposition']"))
            time.sleep(2)

            feature_inactive = driver.find_elements(By.XPATH, "//p[contains(text(),'Feature Inactive')]")
            if feature_inactive:
                toggle_label = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[@class='rounded-toggle-switch']/label[@for='rounded-toggle-switch-ticketDispositions']")))
                safe_click(driver, wait, toggle_label)
                print("✅ Feature was inactive, now activated.")
                time.sleep(2)
            else:
                print("ℹ️ Feature already active, skipping toggle.")

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="fbsuperadmin_error_2", attachment_type=allure.attachment_type.PNG)
            driver.quit()
            pytest.fail(f"fbsuperadmin second flow failed: {e}")
        finally:
            driver.quit()
            time.sleep(1)

    # ---------------- STEP 4: facebook_agent login for next steps ----------------
    with allure.step("Login as facebook_agent (ready for next steps)"):
        driver = locobuzzLogin("facebook_agent", "Locobuzz@123")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="facebook_agent_login_final", attachment_type=allure.attachment_type.PNG)

        print("ℹ️ facebook_agent logged in and ready for next steps.")

        try:
            # Select all and submit
            click_with_retry(wait, (By.XPATH, "//span[text()='Select all']"))
            click_with_retry(wait, (By.XPATH, "//span[text()=' Submit ']"))

            # Search ticket
            search_btn = (By.XPATH, "//a[.//mat-icon[text()=' search']]")
            search_field = (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')
            click_with_retry(wait, search_btn)
            search_input = wait.until(EC.presence_of_element_located(search_field))
            search_input.clear()
            search_input.send_keys(TICKET_ID)
            click_with_retry(wait, search_btn)
            print(f"🔍 Searched ticket: {TICKET_ID}")
            time.sleep(2)

            # Open closed tickets
            click_with_retry(wait, (By.XPATH, "//span[contains(text(),'Closed Tickets')]"))
            click_with_retry(wait, (By.XPATH, "//mat-icon[text()='account_box']"))
            time.sleep(1)

            # Overview & ticket status
            click_with_retry(wait, (By.XPATH, "//div[@role='tab' and .='Overview']"))
            ticket_status = (By.XPATH,
                "//mat-label[normalize-space()='Ticket Status']/ancestor::mat-form-field//div[contains(@class,'mat-mdc-select-trigger')]")
            click_with_retry(wait, ticket_status)
            click_with_retry(wait, (By.XPATH, "//mat-option//span[normalize-space()='Open']"))
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.5)

            # Open tab → Direct Close
            open_tab = (By.XPATH, "//li[.//span[@class='post-option__name' and normalize-space(text())='Open']]")
            click_with_retry(wait, open_tab)
            click_with_retry(wait, (By.XPATH, "//span[text()='Direct Close']"))

            # Disposition selection
            dispositionName = (By.XPATH, "//mat-select[@formcontrolname='dispositionName']")
            click_with_retry(wait, dispositionName)
            productRelated = (By.XPATH, "//mat-option[.//span[text()='Product Related']]")
            click_with_retry(wait, productRelated)

            # Note and Save & Close
            noteField = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Enter note']")))
            noteField.clear()
            noteField.send_keys("Closing ticket with disposition on")
            click_with_retry(wait, (By.XPATH, "//span[text()=' Save & Close ']"))

            allure.attach(driver.get_screenshot_as_png(), name="facebook_agent_actions_final", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(driver.get_screenshot_as_png(), name="facebook_agent_error_final", attachment_type=allure.attachment_type.PNG)
            driver.quit()
            pytest.fail(f"facebook_agent final flow failed: {e}")
        finally:
            driver.quit()
            time.sleep(1)