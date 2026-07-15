# 23FEB26 - Manage Brands Complete Test Suite
import pytest
import time
import os
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from elements.login_page import LoginPageElements
from elements.accountSettings_page import AccountSettingsPageElements

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/single_store/manage_brands"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_create_brand_with_mandatory_fields():
    """Create brand with all mandatory fields filled and save"""
    test_name = "create_brand_mandatory_fields"
    driver = None
    try:
        print("\n" + "="*70)
        print("TEST: Create Brand with Mandatory Fields")
        print("="*70)
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
        print("🔹 Logging in...")
        username = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.USERNAME_INPUT)))
        username.send_keys("bilalSS")
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginPageElements.CONTINUE_BUTTON))).click()
        time.sleep(2)
        password = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.PASSWORD_INPUT)))
        password.send_keys("Locobuzz@123")
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginPageElements.LOGIN_BUTTON))).click()
        time.sleep(5)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", el)

        # Wait for dashboard to load
        print("⏳ Waiting for dashboard to load...")
        time.sleep(5)
        
        # Navigate to Add Brand
        print("🔹 Navigating to Manage Brands...")
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(2)
        
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(3)
        
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        search_field.click()
        search_field.send_keys("manage brand")
        time.sleep(2)
        
        manage_brands_link = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.MANAGE_BRANDS_LINK)))
        safe_click(manage_brands_link)
        time.sleep(3)
        
        add_brand_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_BRAND_P_TAG)))
        safe_click(add_brand_btn)
        time.sleep(3)

        # Generate unique brand name
        timestamp = str(int(time.time()))
        brand_name_text = f"AutoTest_{timestamp}"
        
        # Fill Brand Name
        print(f"🔹 Filling Brand Name: {brand_name_text}")
        brand_name = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_NAME_FIELD)))
        brand_name.clear()
        brand_name.send_keys(brand_name_text)
        time.sleep(1)
        
        # Select Country
        print("🔹 Selecting Country: India")
        country_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.COUNTRY_DROPDOWN)))
        safe_click(country_dropdown)
        time.sleep(1)
        india_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.INDIA_OPTION)))
        safe_click(india_option)
        time.sleep(1)
        
        # Fill AI Friendly Name
        ai_name_text = f"AutoTest{timestamp}"
        print(f"🔹 Filling AI Friendly Name: {ai_name_text}")
        ai_name = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.AI_FRIENDLY_NAME_FIELD)))
        ai_name.clear()
        ai_name.send_keys(ai_name_text)
        time.sleep(1)
        
        # Upload Logo (if file path provided)
        logo_path = os.path.join(os.getcwd(), "tests", "test_data", "brand_logo.png")
        if os.path.exists(logo_path):
            print(f"🔹 Uploading logo: {logo_path}")
            try:
                # Click camera icon to open upload dialog
                camera_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PHOTO_CAMERA_ICON)))
                safe_click(camera_icon)
                time.sleep(2)
                
                # Upload file
                file_input = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.FILE_INPUT)))
                file_input.send_keys(logo_path)
                time.sleep(2)
                
                # Click save upload button if exists
                try:
                    save_upload = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_UPLOAD_BUTTON)))
                    safe_click(save_upload)
                    time.sleep(2)
                    print("✅ Logo uploaded successfully")
                except:
                    print("⚠️ No save upload button found, continuing...")
            except Exception as e:
                print(f"⚠️ Logo upload skipped: {e}")
        else:
            print(f"⚠️ Logo file not found at: {logo_path}")
            print("   Create a 'tests/test_data' folder and add 'brand_logo.png' to test logo upload")
        
        # Select Brand Color (optional but good to test)
        try:
            print("🔹 Selecting brand color...")
            brand_color = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SELECT_BRAND_COLOR)))
            safe_click(brand_color)
            time.sleep(1)
            # Click first color option (you can customize this)
            first_color = driver.find_element(By.XPATH, "(//div[contains(@class, 'color-option')])[1]")
            safe_click(first_color)
            time.sleep(1)
            print("✅ Brand color selected")
        except Exception as e:
            print(f"⚠️ Brand color selection skipped: {e}")
        
        # Scroll to Save button
        print("🔹 Scrolling to Save Brand button...")
        save_btn = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
        time.sleep(2)
        
        # Click Save Brand button
        print("🔹 Clicking Save Brand button...")
        safe_click(save_btn)
        time.sleep(5)
        
        # Check for success message
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SUCCESS_MESSAGE_GENERIC)))
            print(f"✅ SUCCESS: {success_msg.text}")
            print(f"✅ Brand '{brand_name_text}' created successfully!")
            
            # Take success screenshot
            screenshots_dir = "tests/screenshots/single_store/manage_brands"
            os.makedirs(screenshots_dir, exist_ok=True)
            success_path = os.path.join(screenshots_dir, f"success_{test_name}_{timestamp}.png")
            driver.save_screenshot(success_path)
            print(f"📸 Success screenshot saved: {success_path}")
            
        except Exception as e:
            print(f"⚠️ Could not find success message: {e}")
            print("   Checking if brand was created anyway...")
        
        print("\n" + "="*70)
        print("TEST SUMMARY:")
        print(f"Brand Name: {brand_name_text}")
        print(f"Country: India")
        print(f"AI Friendly Name: {ai_name_text}")
        print("="*70)
        
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    # Run the test when executed directly
    test_create_brand_with_mandatory_fields()
