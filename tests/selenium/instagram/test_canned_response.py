#13NOV25 - Creating a canned response with attachment
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
TICKET_ID = TICKET_IDS["instagram"]
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements
from elements.accountSettings_page import AccountSettingsPageElements

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/canned_response"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_canned_response():
    test_name = "instagram_canned_response"
    driver = None
    try:
        print("🔹 Creating canned response with workflow credentials...")
        from utils.credentials import get_workflow_creds, get_instagram_creds
        workflow_username, workflow_password = get_workflow_creds()
        agent_username, agent_password = get_instagram_creds()
        
        # Login with workflow credentials (supervisor/admin)
        driver = locobuzzLogin(workflow_username, workflow_password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Navigating to Account Settings...")

        # Click profile menu - wait for it to be clickable
        time.sleep(2)  # Wait for page to fully load
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        try:
            profile_menu.click()
        except:
            safe_click(profile_menu)
        time.sleep(2)

        # Click Account Settings
        account_settings = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for "canned" in search field
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        search_field.click()
        search_field.send_keys("canned")
        time.sleep(1)

        # Click Canned Responses
        canned_responses_link = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.CANNED_RESPONSES_LINK)))
        safe_click(canned_responses_link)
        time.sleep(2)

        print("🟢 Creating new canned response...")

        # Select Brand dropdown
        brand_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_DROPDOWN)))
        safe_click(brand_dropdown)
        time.sleep(1)

        # Select "Juws" brand
        juws_option = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.JUWS_BRAND_OPTION)))
        safe_click(juws_option)
        time.sleep(1)

        # Click Add Responses
        add_response_btn = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ADD_RESPONSES_BUTTON)))
        safe_click(add_response_btn)
        time.sleep(3)

        # Fill Response Name
        response_name = f"testingtesting_"
        response_name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.RESPONSE_NAME_FIELD)))
        response_name_field.click()
        response_name_field.send_keys(response_name)
        time.sleep(1)

        # Fill Response Text
        response_text_area = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.RESPONSE_PREVIEW)))
        response_text_area.click()
        response_text_area.send_keys("canned response with attachment")
        time.sleep(1)

        # Click Attachment button
        attachment_btn = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ATTACHMENT_BUTTON)))
        safe_click(attachment_btn)
        time.sleep(2)

        # Select first image
        first_image = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.FIRST_IMAGE)))
        safe_click(first_image)
        time.sleep(1)

        # Click Attach button
        attach_btn = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ATTACH_BUTTON)))
        safe_click(attach_btn)
        time.sleep(2)

        # Click Save Response
        save_response_btn = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SAVE_RESPONSE_BUTTON)))
        safe_click(save_response_btn)
        time.sleep(3)

        print("🟢 Logging out and switching to agent account...")

        # Click profile menu to logout
        profile_menu = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(1)

        # Click Logout
        logout_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.LOGOUT_BUTTON)))
        safe_click(logout_btn)
        time.sleep(1)

        # Confirm Logout
        confirm_logout_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.CONFIRM_LOGOUT_BUTTON)))
        safe_click(confirm_logout_btn)
        time.sleep(3)

        print("🟢 Logging in as agent...")

        # Login with agent credentials
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.USERNAME_FIELD)))
        username_field.click()
        username_field.send_keys(agent_username)
        time.sleep(1)

        continue_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.CONTINUE_BUTTON)))
        safe_click(continue_btn)
        time.sleep(1)

        password_field = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.PASSWORD_FIELD)))
        password_field.click()
        password_field.send_keys(agent_password)
        time.sleep(1)

        login_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.LOGIN_BUTTON)))
        safe_click(login_btn)
        time.sleep(3)

        # Select all & Submit
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
        safe_click(select_all)
        submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
        safe_click(submit_btn)
        time.sleep(2)

        print("🟢 Searching for ticket and using canned response...")

        # Search Ticket
        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_FIELD)))
        search_field.send_keys(TICKET_ID)
        search_field.send_keys(Keys.RETURN)
        time.sleep(3)

        # Click Reply button
        reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_BUTTON)))
        safe_click(reply_btn)
        time.sleep(2)

        # Click "Discard"
        discard_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
        safe_click(discard_btn)
        time.sleep(1)
        submit_btn2 = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
        safe_click(submit_btn2)
        time.sleep(2)

        # Click canned response icon (3rd image icon)
        canned_icon = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CANNED_RESPONSE_ICON)))
        safe_click(canned_icon)
        time.sleep(2)

        # Select the canned response we just created
        canned_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CANNED_RESPONSE_DROPDOWN)))
        safe_click(canned_dropdown)
        time.sleep(1)

        # Select the response by name 
        canned_option = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), 'testingtesting')]")))
        safe_click(canned_option)
        time.sleep(1)

        # Click Select button
        select_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SELECT_CANNED_BUTTON)))
        safe_click(select_btn)
        time.sleep(2)

        # Click Send button
        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
        safe_click(send_btn)
        time.sleep(3)

        print("✅ Canned response test completed successfully")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        if driver:
            capture_failure_screenshot(driver, test_name)
        raise

    finally:
        if driver:
            print("🧹 Browser closed safely after canned response test")
            driver.quit()
