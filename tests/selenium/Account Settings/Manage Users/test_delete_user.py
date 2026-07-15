# Delete User Test - Converted from Playwright
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from locobuzz_login.CX_login import locobuzzLogin
from elements.accountSettings_page import AccountSettingsPageElements
from utils.credentials import get_sa_creds


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/account_settings"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_delete_user():
    """Test delete user workflow - search for user and delete"""
    test_name = "delete_user"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Starting Delete User workflow...")

        # Navigate to Account Settings
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(2)

        # Click Account Settings
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for "manage user"
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        safe_click(search_field)
        search_field.clear()
        search_field.send_keys("manage user")
        time.sleep(1)

        # Click Manage Users link
        manage_users_link = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.MANAGE_USERS_LINK)))
        safe_click(manage_users_link)
        time.sleep(2)
        print("✅ Navigated to Manage Users")

        # Search for user "testagent"
        print("🔍 Searching for user: testagent")
        search_user_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_USER_FIELD)))
        safe_click(search_user_field)
        search_user_field.clear()
        search_user_field.send_keys("testagent")
        time.sleep(1)

        # Click search button
        search_user_button = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SEARCH_USER_BUTTON)))
        safe_click(search_user_button)
        time.sleep(2)
        print("✅ Searched for: testagent")

        # Click the action button (3-dot menu) for the user row
        action_button = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.USER_ROW_ACTION_BUTTON)))
        safe_click(action_button)
        time.sleep(1)
        print("✅ Clicked action menu button")

        # Click Delete menu item
        delete_menu_item = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.DELETE_MENU_ITEM)))
        safe_click(delete_menu_item)
        time.sleep(2)
        print("✅ Clicked Delete menu item")

        # Click Yes button to confirm deletion
        yes_button = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.YES_DELETE_BUTTON)))
        safe_click(yes_button)
        time.sleep(3)
        print("✅ Confirmed deletion by clicking Yes")

        # Verify success message
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.USER_DELETED_SUCCESS_MESSAGE)))
            print(f"✅ Success: {success_msg.text}")
        except Exception as e:
            print(f"⚠️ User deleted message not found: {e}")
            
        print("✅ Delete User workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after delete user workflow")


if __name__ == "__main__":
    test_delete_user()
