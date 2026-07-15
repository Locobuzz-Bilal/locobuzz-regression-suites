#23DEC2025
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from locobuzz_login.CX_login import locobuzzLogin
from elements.accountSettings_page import AccountSettingsPageElements
from elements.listening_settings_page import ListeningSettingsPageElements
from utils.credentials import get_sa_creds

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/location_profile"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_edit_delete_location():
    """Test Location Profile edit and delete functionality"""
    test_name = "edit_delete_location"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        def safe_type(element, text):
            element.clear()
            element.send_keys(text)

        print("🟢 Testing Location Profile edit and delete...")

        # Navigate to Account Settings
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for location
        search_field = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        safe_click(search_field)
        safe_type(search_field, "location")
        time.sleep(1)

        # Click on Location Profile
        location_profile = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.LOCATION_PROFILE_LINK)))
        safe_click(location_profile)
        time.sleep(2)

        # Search for "testing" location
        search_location = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SEARCH_LOCATION_FIELD)))
        safe_click(search_location)
        safe_type(search_location, "testing")
        time.sleep(1)

        # Click search button
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SEARCH_BUTTON)))
        safe_click(search_btn)
        time.sleep(2)

        # Click edit button
        edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.EDIT_LOCATION_BUTTON)))
        safe_click(edit_btn)
        time.sleep(2)

        # Update address field
        address_field = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ADDRESS_FIELD)))
        safe_click(address_field)
        safe_type(address_field, "123, @qwerasdfg")
        time.sleep(1)

        # Click Update Location button
        update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.UPDATE_LOCATION_BUTTON)))
        safe_click(update_btn)
        time.sleep(2)

        print("✓ Location updated successfully")

        # Search again to verify update
        search_location = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SEARCH_LOCATION_FIELD)))
        safe_click(search_location)
        time.sleep(1)

        # Click search button
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SEARCH_BUTTON)))
        safe_click(search_btn)
        time.sleep(2)

        # Click delete button
        delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.DELETE_LOCATION_BUTTON)))
        safe_click(delete_btn)
        time.sleep(1)

        # Confirm deletion
        confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CONFIRM_DELETE_BUTTON)))
        safe_click(confirm_btn)
        time.sleep(2)

        # Verify delete success message
        delete_success = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.DELETE_SUCCESS_MESSAGE)))
        assert delete_success.is_displayed(), "Delete success message not displayed"
        print("✅ Location deleted successfully!")

        time.sleep(2)
        print("✅ Test completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        if driver:
            capture_failure_screenshot(driver, test_name)
        raise

    finally:
        if driver:
            driver.quit()
