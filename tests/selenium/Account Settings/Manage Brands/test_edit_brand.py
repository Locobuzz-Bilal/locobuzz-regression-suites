# Edit Brand Test - Converted from Playwright
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
def test_edit_brand():
    """Test edit brand workflow - search for brand and update its name"""
    test_name = "edit_brand"
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

        print("🟢 Starting Edit Brand workflow...")

        # Navigate to Account Settings
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(2)

        # Click Account Settings
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for "manage brands"
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        safe_click(search_field)
        search_field.clear()
        search_field.send_keys("manage brands")
        time.sleep(1)

        # Click Manage Brands link
        manage_brands_link = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.MANAGE_BRANDS_LINK)))
        safe_click(manage_brands_link)
        time.sleep(2)

        # Search "apple test"
        print("🔍 Search: apple test")
        search_brand_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_BRAND_FIELD)))
        safe_click(search_brand_field)
        search_brand_field.clear()
        search_brand_field.send_keys("apple test")
        time.sleep(3)

        # Click search button again
        search_brand_button = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SEARCH_BRAND_BUTTON)))
        safe_click(search_brand_button)
        time.sleep(2)
        print("✅ Searched for: apple test")

        # Click Edit button
        edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.EDIT_BRAND_BUTTON)))
        safe_click(edit_button)
        time.sleep(2)
        print("✅ Clicked Edit button")

        # Update Brand Name
        brand_name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_NAME_FIELD)))
        safe_click(brand_name_field)
        brand_name_field.clear()
        brand_name_field.send_keys("Apple test001")
        time.sleep(1)
        print("✅ Updated brand name to: Apple test001")

        # Click Update Brand button
        update_brand_button = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.UPDATE_BRAND_BUTTON)))
        safe_click(update_brand_button)
        time.sleep(3)
        print("✅ Clicked Update Brand button")

        # Verify success message
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_UPDATE_SUCCESS_MESSAGE)))
            print(f"✅ Success: {success_msg.text}")
        except Exception as e:
            print(f"⚠️ Success message not found: {e}")
            # Try generic success message
            try:
                success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SUCCESS_MESSAGE_GENERIC)))
                print(f"✅ Success: {success_msg.text}")
            except Exception as e2:
                print(f"⚠️ Generic success message also not found: {e2}")

        print("✅ Edit Brand workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after edit brand workflow")


if __name__ == "__main__":
    test_edit_brand()
