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
def test_location_profile():
    """Test Location Profile creation with validation"""
    test_name = "location_profile"
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

        print("🟢 Testing Location Profile creation...")

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

        # Click Add New Location
        add_location_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ADD_NEW_LOCATION_BUTTON)))
        safe_click(add_location_btn)
        time.sleep(1)

        # Enter Location Name
        location_name = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.LOCATION_NAME_FIELD)))
        safe_click(location_name)
        safe_type(location_name, "Testing")

        # Try to save - should show validation for Address
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SAVE_LOCATION_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)

        # Verify Address validation message
        address_validation = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.VALIDATION_ADDRESS)))
        assert address_validation.is_displayed(), "Address validation message not displayed"
        print("✓ Address validation passed")

        # Enter Address
        address_field = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ADDRESS_FIELD)))
        safe_click(address_field)
        safe_type(address_field, "123, @qwer")

        # Try to save - should show validation for City
        safe_click(save_btn)
        time.sleep(1)

        # Verify City validation message
        city_validation = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.VALIDATION_CITY)))
        assert city_validation.is_displayed(), "City validation message not displayed"
        print("✓ City validation passed")

        # Enter City
        city_field = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CITY_FIELD)))
        safe_click(city_field)
        safe_type(city_field, "mumbai")

        # Try to save - should show validation for State
        safe_click(save_btn)
        time.sleep(1)

        # Verify State validation message
        state_validation = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.VALIDATION_STATE)))
        assert state_validation.is_displayed(), "State validation message not displayed"
        print("✓ State validation passed")

        # Enter State
        state_field = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.STATE_FIELD)))
        safe_click(state_field)
        safe_type(state_field, "maha")

        # Try to save - should show validation for Country
        safe_click(save_btn)
        time.sleep(1)

        # Verify Country validation message
        country_validation = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.VALIDATION_COUNTRY)))
        assert country_validation.is_displayed(), "Country validation message not displayed"
        print("✓ Country validation passed")

        # Select Country
        country_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.COUNTRY_DROPDOWN)))
        safe_click(country_dropdown)
        time.sleep(1)

        search_country = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SEARCH_COUNTRY_FIELD)))
        safe_type(search_country, "indi")
        time.sleep(1)

        india_option = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.INDIA_OPTION)))
        safe_click(india_option)
        time.sleep(1)

        # Try to save - should show validation for Pin Code
        safe_click(save_btn)
        time.sleep(1)

        # Verify Pin Code validation message
        pincode_validation = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.VALIDATION_PINCODE)))
        assert pincode_validation.is_displayed(), "Pin Code validation message not displayed"
        print("✓ Pin Code validation passed")

        # Enter Pin Code
        pincode_field = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.PIN_CODE_FIELD)))
        safe_click(pincode_field)
        safe_type(pincode_field, "122221")

        # Try to save - should show validation for Latitude
        safe_click(save_btn)
        time.sleep(1)

        # Verify Latitude validation message
        latitude_validation = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.VALIDATION_LATITUDE)))
        assert latitude_validation.is_displayed(), "Latitude validation message not displayed"
        print("✓ Latitude validation passed")

        # Enter Latitude
        latitude_field = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.LATITUDE_FIELD)))
        safe_click(latitude_field)
        safe_type(latitude_field, "12")

        # Try to save - should show validation for Longitude
        safe_click(save_btn)
        time.sleep(1)

        # Verify Longitude validation message
        longitude_validation = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.VALIDATION_LONGITUDE)))
        assert longitude_validation.is_displayed(), "Longitude validation message not displayed"
        print("✓ Longitude validation passed")

        # Enter Longitude
        longitude_field = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.LONGITUDE_FIELD)))
        safe_click(longitude_field)
        safe_type(longitude_field, "113")

        # Save Location
        safe_click(save_btn)
        time.sleep(2)

        # Verify Success Message
        success_msg = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.SUCCESS_MESSAGE)))
        assert success_msg.is_displayed(), "Success message not displayed"
        print("✅ Location saved successfully!")

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
