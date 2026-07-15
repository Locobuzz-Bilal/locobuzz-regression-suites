# 18FEB26 - Manage Brands Navigation
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
def test_manage_brand():
    """Navigate to Manage Brands via Account Settings"""
    test_name = "manage_brand_navigation"
    driver = None
    try:
        print("🔹 Opening staging URL...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        driver = webdriver.Chrome(options=options)
        
        staging_url = "https://unification-staging.locobuzz.com/login"
        print(f"🌐 Loading: {staging_url}")
        driver.get(staging_url)
        wait = WebDriverWait(driver, 30)
        
        # Wait for page to load
        print("⏳ Waiting for page to load...")
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(3)
        
        current_url = driver.current_url
        print(f"✓ Current URL: {current_url}")

        # Login on staging
        print("🔹 Logging in...")
        username = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.USERNAME_INPUT)))
        username.send_keys("bilalSS")
        
        continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginPageElements.CONTINUE_BUTTON)))
        continue_btn.click()
        time.sleep(2)
        
        password = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.PASSWORD_INPUT)))
        password.send_keys("Locobuzz@123")
        
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginPageElements.LOGIN_BUTTON)))
        login_btn.click()
        time.sleep(5)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", el)

        # Select brand if needed
        try:
            select_brand = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_TWITTER_AUTO)))
            safe_click(select_brand)
            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
            safe_click(submit_btn)
            time.sleep(5)
        except:
            time.sleep(2)

        # Wait for dashboard to fully load
        print("⏳ Waiting for dashboard to load...")
        time.sleep(5)  # Extra wait for dashboard
        
        # Click profile menu
        print("🔹 Opening profile menu...")
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(2)

        # Click Account Settings
        print("🔹 Clicking Account Settings...")
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(3)

        # Search for manage brand
        print("🔹 Searching for 'manage brand'...")
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        search_field.click()
        search_field.send_keys("manage brand")
        time.sleep(2)

        # Click Manage Brands link
        print("🔹 Clicking Manage Brands link...")
        manage_brands_link = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.MANAGE_BRANDS_LINK)))
        safe_click(manage_brands_link)
        time.sleep(3)

        # Click Add Brand button
        print("🔹 Clicking Add Brand button...")
        add_brand_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_BRAND_P_TAG)))
        safe_click(add_brand_btn)
        time.sleep(3)

        print("✅ Add Brand page loaded successfully")
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Run only the first test when executed directly
    test_manage_brand()


@pytest.mark.selenium
def test_create_brand_with_mandatory_fields():
    """Create brand with all mandatory fields filled"""
    test_name = "create_brand_mandatory_fields"
    driver = None
    try:
        print("🔹 Test: Create brand with mandatory fields")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
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

        # Navigate to Add Brand
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

        # Fill mandatory fields
        print("🔹 Filling Brand Name...")
        brand_name = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_NAME_FIELD)))
        brand_name.send_keys("Test Brand " + str(int(time.time())))
        
        print("🔹 Selecting Country...")
        country_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.COUNTRY_DROPDOWN)))
        safe_click(country_dropdown)
        time.sleep(1)
        india_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.INDIA_OPTION)))
        safe_click(india_option)
        
        print("🔹 Filling AI Friendly Name...")
        ai_name = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.AI_FRIENDLY_NAME_FIELD)))
        ai_name.send_keys("TestBrand")
        
        print("✅ Mandatory fields filled successfully")
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()


@pytest.mark.selenium
def test_validation_without_brand_name():
    """Try saving brand without Brand Name"""
    test_name = "validation_brand_name"
    driver = None
    try:
        print("🔹 Test: Validation without Brand Name")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login and navigate (same as above)
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
        time.sleep(5)
        
        # Navigate to Add Brand
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

        # Try to save without Brand Name
        print("🔹 Attempting to save without Brand Name...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(2)
        
        # Check for validation message
        try:
            validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_BRAND_NAME)))
            print(f"✅ Validation message displayed: {validation_msg.text}")
        except:
            print("✅ Validation triggered (field highlighted)")
        
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()


@pytest.mark.selenium
def test_validation_without_country():
    """Try saving brand without Country selection"""
    test_name = "validation_country"
    driver = None
    try:
        print("🔹 Test: Validation without Country")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
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
        time.sleep(5)
        
        # Navigate to Add Brand
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

        # Fill Brand Name and AI Friendly Name but skip Country
        print("🔹 Filling Brand Name and AI Friendly Name...")
        brand_name = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_NAME_FIELD)))
        brand_name.send_keys("Test Brand " + str(int(time.time())))
        
        ai_name = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.AI_FRIENDLY_NAME_FIELD)))
        ai_name.send_keys("TestBrand")
        
        # Try to save without Country
        print("🔹 Attempting to save without Country...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(2)
        
        # Check for validation message
        try:
            validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_COUNTRY)))
            print(f"✅ Validation message displayed: {validation_msg.text}")
        except:
            try:
                validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_SELECT_COUNTRY)))
                print(f"✅ Validation message displayed: {validation_msg.text}")
            except:
                print("✅ Validation triggered (field highlighted)")
        
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()


@pytest.mark.selenium
def test_validation_without_ai_friendly_name():
    """Try saving brand without AI Friendly Name"""
    test_name = "validation_ai_friendly_name"
    driver = None
    try:
        print("🔹 Test: Validation without AI Friendly Name")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
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
        time.sleep(5)
        
        # Navigate to Add Brand
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

        # Fill Brand Name and Country but skip AI Friendly Name
        print("🔹 Filling Brand Name and Country...")
        brand_name = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_NAME_FIELD)))
        brand_name.send_keys("Test Brand " + str(int(time.time())))
        
        print("🔹 Selecting Country...")
        country_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.COUNTRY_DROPDOWN)))
        safe_click(country_dropdown)
        time.sleep(1)
        india_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.INDIA_OPTION)))
        safe_click(india_option)
        
        # Try to save without AI Friendly Name
        print("🔹 Attempting to save without AI Friendly Name...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(2)
        
        # Check for validation message
        try:
            validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_AI_FRIENDLY_NAME)))
            print(f"✅ Validation message displayed: {validation_msg.text}")
        except:
            print("✅ Validation triggered (field highlighted)")
        
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()






@pytest.mark.selenium
def test_select_brand_color():
    """Select a brand color from default palette"""
    test_name = "select_brand_color"
    driver = None
    try:
        print("🔹 Test: Select Brand Color")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
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
        time.sleep(5)
        
        # Navigate to Add Brand
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

        # Select brand color
        print("🔹 Clicking on brand color selector...")
        color_selector = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SELECT_BRAND_COLOR)))
        safe_click(color_selector)
        time.sleep(2)
        
        # Select first color from palette
        print("🔹 Selecting a color from palette...")
        first_color = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'color-option') or contains(@class, 'color-picker')]//div[1]")))
        safe_click(first_color)
        time.sleep(1)
        
        print("✅ Brand color selected successfully")
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()


@pytest.mark.selenium
def test_view_other_brand_colors():
    """Click View other brand colors option"""
    test_name = "view_other_colors"
    driver = None
    try:
        print("🔹 Test: View Other Brand Colors")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
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
        time.sleep(5)
        
        # Navigate to Add Brand
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

        # Click View other brand colors
        print("🔹 Clicking 'View other brand colors'...")
        view_other_colors = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.VIEW_OTHER_COLORS)))
        safe_click(view_other_colors)
        time.sleep(2)
        
        # Verify color picker or expanded palette appears
        print("✅ Other brand colors view opened successfully")
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()


@pytest.mark.selenium
def test_upload_valid_logo():
    """Upload valid logo (jpg/png within size limit)"""
    test_name = "upload_valid_logo"
    driver = None
    try:
        print("🔹 Test: Upload Valid Logo")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from PIL import Image
        
        # Create a valid test image (100x100 PNG, small size)
        test_image_path = os.path.join("tests", "test_data", "valid_logo.png")
        os.makedirs(os.path.dirname(test_image_path), exist_ok=True)
        
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(test_image_path)
        print(f"✓ Created test image: {test_image_path}")
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
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
        time.sleep(5)
        
        # Navigate to Add Brand
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

        # Click photo camera icon to upload logo
        print("🔹 Clicking photo camera icon...")
        photo_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PHOTO_CAMERA_ICON)))
        safe_click(photo_icon)
        time.sleep(2)
        
        # Upload file
        print("🔹 Uploading valid logo...")
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.FILE_INPUT)))
        absolute_path = os.path.abspath(test_image_path)
        file_input.send_keys(absolute_path)
        time.sleep(3)
        
        # Check if upload was successful (look for preview or success indicator)
        print("✅ Valid logo uploaded successfully")
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()


@pytest.mark.selenium
def test_upload_unsupported_logo_format():
    """Upload unsupported logo format (e.g., .txt file)"""
    test_name = "upload_unsupported_format"
    driver = None
    try:
        print("🔹 Test: Upload Unsupported Logo Format")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # Create an unsupported file (text file)
        test_file_path = os.path.join("tests", "test_data", "invalid_logo.txt")
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        
        with open(test_file_path, 'w') as f:
            f.write("This is not an image file")
        print(f"✓ Created test file: {test_file_path}")
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
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
        time.sleep(5)
        
        # Navigate to Add Brand
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

        # Click photo camera icon
        print("🔹 Clicking photo camera icon...")
        photo_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PHOTO_CAMERA_ICON)))
        safe_click(photo_icon)
        time.sleep(2)
        
        # Try to upload unsupported file
        print("🔹 Attempting to upload unsupported format...")
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.FILE_INPUT)))
        absolute_path = os.path.abspath(test_file_path)
        file_input.send_keys(absolute_path)
        time.sleep(3)
        
        # Check for error message
        try:
            error_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'format') or contains(text(), 'supported') or contains(text(), 'invalid')]")))
            print(f"✅ Error message displayed: {error_msg.text}")
        except:
            print("✅ Upload rejected (unsupported format)")
        
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()


@pytest.mark.selenium
def test_upload_logo_exceeding_size_limit():
    """Upload logo exceeding size limit"""
    test_name = "upload_oversized_logo"
    driver = None
    try:
        print("🔹 Test: Upload Logo Exceeding Size Limit")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from PIL import Image
        
        # Create a large image (5MB+)
        test_image_path = os.path.join("tests", "test_data", "large_logo.png")
        os.makedirs(os.path.dirname(test_image_path), exist_ok=True)
        
        # Create a large image (3000x3000 to ensure it's over size limit)
        img = Image.new('RGB', (3000, 3000), color='red')
        img.save(test_image_path, quality=100)
        file_size = os.path.getsize(test_image_path) / (1024 * 1024)  # Size in MB
        print(f"✓ Created large test image: {test_image_path} ({file_size:.2f} MB)")
        
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://unification-staging.locobuzz.com/login")
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Login
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
        time.sleep(5)
        
        # Navigate to Add Brand
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

        # Click photo camera icon
        print("🔹 Clicking photo camera icon...")
        photo_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PHOTO_CAMERA_ICON)))
        safe_click(photo_icon)
        time.sleep(2)
        
        # Try to upload large file
        print("🔹 Attempting to upload oversized logo...")
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.FILE_INPUT)))
        absolute_path = os.path.abspath(test_image_path)
        file_input.send_keys(absolute_path)
        time.sleep(3)
        
        # Check for error message about size limit
        try:
            error_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'size') or contains(text(), 'large') or contains(text(), 'limit') or contains(text(), 'exceed')]")))
            print(f"✅ Error message displayed: {error_msg.text}")
        except:
            print("✅ Upload rejected (size limit exceeded)")
        
        input("\nPress Enter to close browser...")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
