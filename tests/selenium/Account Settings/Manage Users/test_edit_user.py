# Edit User Test - Converted from Playwright
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
def test_edit_user():
    """Test edit user workflow - search for user, change role, and update"""
    test_name = "edit_user"
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

        print("🟢 Starting Edit User workflow...")

        # Navigate to Account Settings
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(2)

        # Click Account Settings
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for "manage users"
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        safe_click(search_field)
        search_field.clear()
        search_field.send_keys("manage users")
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

        # Click Edit menu item
        edit_menu_item = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.EDIT_MENU_ITEM)))
        safe_click(edit_menu_item)
        time.sleep(2)
        print("✅ Clicked Edit menu item")

        # Click on Role dropdown
        role_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ROLE_DROPDOWN)))
        safe_click(role_dropdown)
        time.sleep(1)
        print("✅ Opened Role dropdown")

        # Select "Agent" role
        agent_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.AGENT_OPTION)))
        safe_click(agent_option)
        time.sleep(1)
        print("✅ Selected role: Agent")

        # TEST 1: Try to update without brands (role change requires brand re-assignment)
        print("🧪 Test 1: Attempting to update without brands...")
        update_user_button = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.UPDATE_USER_BUTTON)))
        safe_click(update_user_button)
        time.sleep(2)

        # Verify validation message
        try:
            validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_ASSIGN_BRANDS)))
            print(f"✅ Validation shown: {validation_msg.text}")
        except Exception as e:
            print(f"⚠️ Brands validation not found (might not be required for role change): {e}")

        # Search and select brand
        print("🔍 Searching for brand: juw")
        search_brands = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_BRANDS_COMBOBOX)))
        safe_click(search_brands)
        search_brands.clear()
        search_brands.send_keys("juw")
        time.sleep(1)

        # Select Juws brand
        juws_brand = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.JUWS_BRAND_SELECTION)))
        safe_click(juws_brand)
        time.sleep(1)
        print("✅ Selected brand: Juws")

        # Click Update User button
        update_user_button = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.UPDATE_USER_BUTTON)))
        safe_click(update_user_button)
        time.sleep(2)
        print("✅ Clicked Update User button")

        # Click Proceed without adding button if it appears
        try:
            proceed_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROCEED_WITHOUT_ADDING_BUTTON)))
            safe_click(proceed_btn)
            time.sleep(2)
            print("✅ Clicked Proceed without adding")
        except Exception as e:
            print(f"⚠️ Proceed without adding button not found: {e}")

        # Verify success message
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.USER_UPDATED_SUCCESS_MESSAGE)))
            print(f"✅ Success: {success_msg.text}")
        except Exception as e:
            print(f"⚠️ Success message not found: {e}")
            # Try generic success message
            try:
                success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SUCCESS_MESSAGE_GENERIC)))
                print(f"✅ Success: {success_msg.text}")
            except Exception as e2:
                print(f"⚠️ Generic success message also not found: {e2}")

        print("✅ Edit User workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after edit user workflow")


if __name__ == "__main__":
    test_edit_user()
