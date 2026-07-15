"""
Workflow Automation - Create New Workflow Test
"""

import os
import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from locobuzz_login.CX_login import locobuzzLogin
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from utils.credentials import get_twitter_creds, get_sa_creds
from elements.workflow_automation_page import WorkflowAutomationPageElements

@pytest.mark.selenium
@pytest.mark.no_rerun
def test_create_workflow_automation(headless_flag=None):
    driver = None
    wait = None
    shots_dir = os.path.join(os.path.dirname(__file__), "../../screenshots", "workflow_automation")
    os.makedirs(shots_dir, exist_ok=True)

    def snap(name):
        if not driver:
            return
        path = os.path.join(shots_dir, f"{name}_{int(time.time())}.png")
        driver.save_screenshot(path)
        allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)

    def click_xpath(xp, timeout=25):
        time.sleep(1)  # Wait 1 second before every click
        el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xp)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        driver.execute_script("arguments[0].click();", el)
        return el

    def type_xpath(xp, text, clear=True, timeout=25):
        time.sleep(1)  # Wait 1 second before every type action
        el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xp)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        if clear:
            try:
                el.clear()
            except Exception:
                pass
        el.send_keys(text)
        return el

    def switch_to_iframe_and_type(iframe_xpath, text, timeout=25):
        iframe = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
        driver.switch_to.frame(iframe)
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(text)
        driver.switch_to.default_content()

    try:
        with allure.step("Login"):
            user, pwd = get_sa_creds()
            driver = locobuzzLoginPreProd(user, pwd, headless=False)
            wait = WebDriverWait(driver, 30)
            snap("login_ok")

        with allure.step("Navigate to Account Settings"):
            click_xpath(WorkflowAutomationPageElements.ACCOUNT_SETTINGS_MENU)
            click_xpath(WorkflowAutomationPageElements.ACCOUNT_SETTINGS_OPTION)
            snap("account_settings_opened")

        with allure.step("Search for Workflow Automation"):
            type_xpath(WorkflowAutomationPageElements.SEARCH_INPUT, "workflow")
            click_xpath(WorkflowAutomationPageElements.WORKFLOW_LINK)
            time.sleep(2)
            snap("workflow_page_opened")

        with allure.step("Select Brand"):
            click_xpath(WorkflowAutomationPageElements.BRAND_DROPDOWN)
            click_xpath(WorkflowAutomationPageElements.BRAND_JUWS_OPTION)
            snap("brand_selected")

        with allure.step("Enable Workflow Feature Toggle"):
            click_xpath(WorkflowAutomationPageElements.FEATURE_TOGGLE)
            snap("feature_toggle_enabled")
            time.sleep(5)

        with allure.step("Create New Workflow"):
            click_xpath(WorkflowAutomationPageElements.CREATE_NEW_BUTTON)
            type_xpath(WorkflowAutomationPageElements.WORKFLOW_NAME_INPUT, "Testing Workflow_005")
            snap("workflow_name_entered")

        with allure.step("Add Trigger - New Ticket"):
            click_xpath(WorkflowAutomationPageElements.ADD_TRIGGER_BUTTON)
            click_xpath(WorkflowAutomationPageElements.NEW_TICKET_TRIGGER)
            snap("trigger_added")

        with allure.step("Add Step - Canned Response"):
            click_xpath(WorkflowAutomationPageElements.ADD_STEP_BUTTON)
            click_xpath(WorkflowAutomationPageElements.CANNED_RESPONSE_BUTTON)
            
            click_xpath(WorkflowAutomationPageElements.PERSONALIZE_BUTTON)
            click_xpath(WorkflowAutomationPageElements.FIRST_NAME_OPTION)
            
            type_xpath(WorkflowAutomationPageElements.MESSAGE_TEXTAREA, " {First Name} , thank you for reaching out")
            click_xpath(f"({WorkflowAutomationPageElements.ADD_RESPONSE_BUTTON})[2]")
            
            type_xpath(WorkflowAutomationPageElements.MESSAGE_TEXTAREA, "Hi, how are doing?")
            click_xpath(f"({WorkflowAutomationPageElements.ADD_RESPONSE_BUTTON})[2]")
            
            click_xpath(WorkflowAutomationPageElements.ADD_ATTRIBUTES_BUTTON)
            click_xpath(WorkflowAutomationPageElements.LOCATION_ATTRIBUTES)
            click_xpath(WorkflowAutomationPageElements.LOCATION_NAME)
            click_xpath(f"({WorkflowAutomationPageElements.ADD_RESPONSE_BUTTON})[2]")
            
            click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            snap("canned_response_added")

        # with allure.step("Configure Disposition - Ticket Shown"):
        #     click_xpath(WorkflowAutomationPageElements.DISPOSITION_DROPDOWN)
        #     click_xpath(WorkflowAutomationPageElements.TICKET_SHOWN_OPTION)
            
        #     click_xpath(WorkflowAutomationPageElements.CATEGORY_EDIT_BUTTON)
        #     click_xpath(WorkflowAutomationPageElements.EMAIL_TEST_CHECKBOX)
        #     click_xpath(WorkflowAutomationPageElements.POSITIVE_RADIO)
        #     type_xpath(WorkflowAutomationPageElements.NOTE_INPUT, "ticket dispo")
        #     click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
        #     snap("disposition_configured")

        with allure.step("Add Step - Mark as Closed"):
            click_xpath(WorkflowAutomationPageElements.ADD_STEP_BUTTON)
            click_xpath(WorkflowAutomationPageElements.MARK_CLOSED_BUTTON)
            
            # click_xpath(WorkflowAutomationPageElements.DISPOSITION_DROPDOWN)
            # click_xpath(WorkflowAutomationPageElements.ORDER_RELATED_OPTION)
            
            # click_xpath(WorkflowAutomationPageElements.CATEGORY_EDIT_BUTTON)
            # click_xpath(WorkflowAutomationPageElements.EMAIL_TEST_CHECKBOX)
            # click_xpath(WorkflowAutomationPageElements.NEGATIVE_RADIO)
            # click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            snap("mark_closed_added")

        with allure.step("Add Step - Send Alert"):
            click_xpath(WorkflowAutomationPageElements.ADD_STEP_BUTTON)
            time.sleep(0.5)
            
            # Scroll within the menu to make Send Alert visible
            try:
                # Find Canned Response button and scroll down from there
                canned_response = driver.find_element(By.XPATH, WorkflowAutomationPageElements.CANNED_RESPONSE_BUTTON)
                driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", canned_response)
                time.sleep(0.3)
                # Scroll down further to reveal Send Alert
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(0.5)
            except:
                pass
            
            click_xpath(WorkflowAutomationPageElements.SEND_ALERT_BUTTON)
            
            type_xpath(WorkflowAutomationPageElements.ALERT_SUBJECT_INPUT, "Trigger Alert")
            
            click_xpath(WorkflowAutomationPageElements.TO_EMAIL_COMBO)
            type_xpath(WorkflowAutomationPageElements.TO_EMAIL_COMBO, "juw@gmail.com")
            click_xpath(WorkflowAutomationPageElements.EMAIL_OPTION)
            
            switch_to_iframe_and_type(WorkflowAutomationPageElements.EDITOR_IFRAME, "workflow testing")
            
            click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            snap("send_alert_added")

        with allure.step("Add Step - Set Category"):
            click_xpath(WorkflowAutomationPageElements.ADD_STEP_BUTTON)
            click_xpath(WorkflowAutomationPageElements.SET_CATEGORY_BUTTON)
            
            click_xpath(WorkflowAutomationPageElements.UPPER_CATEGORY_DROPDOWN)
            click_xpath(WorkflowAutomationPageElements.HELLO_SHAIWAZ_OPTION)
            
            click_xpath(WorkflowAutomationPageElements.CATEGORY_EDIT_BUTTON)
            click_xpath(WorkflowAutomationPageElements.EMAIL_TEST_CHECKBOX)
            click_xpath(WorkflowAutomationPageElements.NEUTRAL_RADIO)
            click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            snap("set_category_added")

        with allure.step("Add Step - Set Priority"):
            click_xpath(WorkflowAutomationPageElements.ADD_STEP_BUTTON)
            click_xpath(WorkflowAutomationPageElements.SET_PRIORITY_BUTTON)
            click_xpath(WorkflowAutomationPageElements.MEDIUM_PRIORITY_BUTTON)
            click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            snap("set_priority_added")

        with allure.step("Add Step - Assign To"):
            click_xpath(WorkflowAutomationPageElements.ADD_STEP_BUTTON)
            click_xpath(WorkflowAutomationPageElements.ASSIGN_TO_BUTTON)
            click_xpath(WorkflowAutomationPageElements.USER_CHECKBOX)
            click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            snap("assign_to_added")

        with allure.step("Add Step - Add Delay"):
            click_xpath(WorkflowAutomationPageElements.ADD_STEP_BUTTON)
            click_xpath(WorkflowAutomationPageElements.ADD_DELAY_BUTTON)
            type_xpath(WorkflowAutomationPageElements.DELAY_INPUT, "2")
            click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            snap("delay_added")
            
            # Scroll to make next Add Step button visible
            time.sleep(1)
            try:
                add_step_btn = driver.find_element(By.XPATH, WorkflowAutomationPageElements.ADD_STEP_BUTTON)
                driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'smooth'});", add_step_btn)
                time.sleep(1)
            except:
                # Fallback: scroll by pixels
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)

        with allure.step("Add Step - Add Paths (then delete)"):
            click_xpath(WorkflowAutomationPageElements.ADD_STEP_BUTTON)
            click_xpath(WorkflowAutomationPageElements.ADD_PATHS_BUTTON)
            
            type_xpath(WorkflowAutomationPageElements.PATH_A_INPUT, "Path A", clear=False)
            click_xpath(WorkflowAutomationPageElements.SELECT_ATTRIBUTE)
            click_xpath(WorkflowAutomationPageElements.CHANNEL_ATTRIBUTE)
            click_xpath(WorkflowAutomationPageElements.SHOULD_CONTAIN)
            click_xpath(WorkflowAutomationPageElements.SHOULD_NOT_CONTAIN)
            click_xpath(WorkflowAutomationPageElements.SELECT_CHANNEL)
            click_xpath(WorkflowAutomationPageElements.TWITTER_CHECKBOX)
                             
            click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            
            # Delete path
            click_xpath(WorkflowAutomationPageElements.DELETE_PATH_MENU)
            click_xpath(WorkflowAutomationPageElements.DELETE_PATH_BUTTON)
            click_xpath(WorkflowAutomationPageElements.YES_BUTTON)
            snap("path_deleted")

        with allure.step("Configure Settings"):
            click_xpath(WorkflowAutomationPageElements.SETTINGS_ICON)
            time.sleep(2)  # Wait for settings modal to fully load
            
            # Find radio button, scroll to it, and click using JS
            try:
                radio_btn = driver.find_element(By.XPATH, WorkflowAutomationPageElements.SEND_DEFAULT_REPLY_RADIO)
                driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'smooth'});", radio_btn)
                time.sleep(1)
                # Click using JavaScript to ensure it works
                driver.execute_script("arguments[0].click();", radio_btn)
                time.sleep(2)
            except Exception as e:
                print(f"Failed to click radio button: {e}")
                # Fallback: try regular click
                click_xpath(WorkflowAutomationPageElements.SEND_DEFAULT_REPLY_RADIO)
            
            time.sleep(2)  # Wait for textarea to appear after selecting radio
            
            type_xpath(WorkflowAutomationPageElements.MESSAGE_TEXTAREA, "Thank You for reaching out ")
            
            click_xpath(WorkflowAutomationPageElements.PERSONALIZE_BUTTON)
            click_xpath(WorkflowAutomationPageElements.FULL_NAME_OPTION)
            click_xpath(WorkflowAutomationPageElements.ADD_RESPONSE_BUTTON)
            
            type_xpath(WorkflowAutomationPageElements.MESSAGE_TEXTAREA, "hope this helps")
            click_xpath(WorkflowAutomationPageElements.ADD_RESPONSE_BUTTON)
            
            click_xpath(WorkflowAutomationPageElements.PERSONALIZE_BUTTON)
            click_xpath(WorkflowAutomationPageElements.SCREEN_NAME_OPTION)
            click_xpath(WorkflowAutomationPageElements.ADD_RESPONSE_BUTTON)
            
            click_xpath(WorkflowAutomationPageElements.SAVE_BUTTON)
            snap("settings_configured")

        with allure.step("Save Workflow"):
            click_xpath(WorkflowAutomationPageElements.SAVE_WORKFLOW_BUTTON)
            time.sleep(3)
            snap("workflow_saved")

        assert True, "Workflow automation test completed"

    except (TimeoutException, WebDriverException) as e:
        snap("failure_timeout")
        pytest.fail(f"Timeout/WebDriver error: {e}")
    except Exception as e:
        snap("failure_unexpected")
        pytest.fail(f"Unexpected error: {e}")
    finally:
        if driver:
            driver.quit()