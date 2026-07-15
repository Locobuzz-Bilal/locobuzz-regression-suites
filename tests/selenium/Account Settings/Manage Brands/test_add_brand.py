# Add Brand Test - Converted from Playwright
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
def test_add_brand():
    """Test negative flow with validation messages for Add Brand workflow"""
    test_name = "add_brand_negative"
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

        print("🟢 Starting Add Brand Negative Validation workflow...")

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
        search_field.send_keys("manage")
        time.sleep(1)

        # Click Manage Brands link
        manage_brands_link = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.MANAGE_BRANDS_LINK)))
        safe_click(manage_brands_link)
        time.sleep(2)

        # Click Add Brand button
        add_brand_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_BRAND_BUTTON)))
        safe_click(add_brand_btn)
        time.sleep(2)

        # TEST 1: Try to save without brand name
        print("🧪 Test 1: Attempting to save without brand name...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)
        
        # Verify validation message
        validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_PLEASE_FILL)))
        print(f"✅ Validation shown: {validation_msg.text}")

        # Fill Brand Name
        brand_name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_NAME_FIELD)))
        safe_click(brand_name_field)
        brand_name_field.clear()
        brand_name_field.send_keys("Samsung")
        time.sleep(1)
        print("✅ Entered brand name: Samsung")

        # TEST 2: Try to save with only brand name
        print("🧪 Test 2: Attempting to save with only brand name...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)
        
        # Verify validation message
        validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_PLEASE_FILL)))
        print(f"✅ Validation shown: {validation_msg.text}")

        # Fill AI Friendly Name
        ai_name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.AI_FRIENDLY_NAME_FIELD)))
        safe_click(ai_name_field)
        ai_name_field.clear()
        ai_name_field.send_keys("Apple")
        time.sleep(1)
        print("✅ Entered AI Friendly Name: Apple")

        # Click Generate Description button
        generate_desc_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.GENERATE_DESCRIPTION_BUTTON)))
        safe_click(generate_desc_btn)
        time.sleep(4)
        print("✅ Clicked Generate Description")

        # TEST 3: Try to save without brand logo
        print("🧪 Test 3: Attempting to save without brand logo...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)
        
        # Verify validation message
        validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_SELECT_LOGO)))
        print(f"✅ Validation shown: {validation_msg.text}")

        # Upload Brand Logo
        try:
            photo_camera = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PHOTO_CAMERA_ICON)))
            safe_click(photo_camera)
            time.sleep(1)
            print("🔍 Clicked photo_camera icon")

            # Find the file input element
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.FILE_INPUT)))
            image_path = os.path.abspath("elements/test_data/images/brand_logo.png.jpg")
            file_input.send_keys(image_path)
            time.sleep(2)
            print(f"✅ Uploaded brand logo: {image_path}")

            # Click Save button in the upload dialog
            save_upload_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_UPLOAD_BUTTON)))
            safe_click(save_upload_btn)
            time.sleep(2)
            print("✅ Saved uploaded logo")
        except Exception as e:
            print(f"⚠️ Could not upload brand logo: {e}")

        # TEST 4: Try to save without country
        print("🧪 Test 4: Attempting to save without country...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)
        
        # Verify validation message
        validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_SELECT_COUNTRY)))
        print(f"✅ Validation shown: {validation_msg.text}")

        # Select Country dropdown
        country_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.COUNTRY_DROPDOWN)))
        safe_click(country_dropdown)
        time.sleep(1)

        # Search for India
        country_search = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.COUNTRY_SEARCH_FIELD)))
        country_search.send_keys("india")
        time.sleep(1)

        # Select India option
        india_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.INDIA_OPTION)))
        safe_click(india_option)
        time.sleep(1)
        print("✅ Selected country: India")

        # TEST 5: Try to save without catch-all category
        print("🧪 Test 5: Attempting to save without catch-all category...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)
        
        # Verify validation message
        validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_SELECT_CATCHALL)))
        print(f"✅ Validation shown: {validation_msg.text}")

        # Select Category Group
        category_group_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.CATEGORY_GROUP_DROPDOWN)))
        safe_click(category_group_dropdown)
        time.sleep(1)

        default_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.DEFAULT_OPTION)))
        safe_click(default_option)
        time.sleep(1)
        print("✅ Selected Category Group: Default")

        # Select Catch-all Category
        catchall_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.CATCHALL_CATEGORY_DROPDOWN)))
        safe_click(catchall_dropdown)
        time.sleep(1)

        manager_approval_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.MANAGER_APPROVAL_PENDING_OPTION)))
        safe_click(manager_approval_option)
        time.sleep(1)
        print("✅ Selected Catch-all Category: ManagerApprovalPending")

        # TEST 6: Try to save without assigning users
        print("🧪 Test 6: Attempting to save without assigning users...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)
        
        # Verify validation message
        validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_ASSIGN_USER)))
        print(f"✅ Validation shown: {validation_msg.text}")

        # Search and select user
        search_users = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_USERS_FIELD)))
        safe_click(search_users)
        search_users.clear()
        search_users.send_keys("juwsa")
        time.sleep(1)

        # Check juwsa checkbox
        user_checkbox_xpath = AccountSettingsPageElements.JUWSA
        juwsa_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, user_checkbox_xpath)))
        driver.execute_script("arguments[0].click();", juwsa_checkbox)
        time.sleep(1)
        print("✅ Selected user: juwsa")

        #enable ticket creation toggle
        safe_click(wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.TICKET_CREATION_TOGGLE))))
        time.sleep(1)

        # Fill in the editor (CKEditor iframe)
        try:
            iframe = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.EDITOR_IFRAME)))
            driver.switch_to.frame(iframe)
            
            editor_body = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.EDITOR_BODY)))
            safe_click(editor_body)
            editor_body.clear()
            editor_body.send_keys("testing manage brands")
            time.sleep(1)
            print("✅ Entered editor content: testing manage brands")
            
            driver.switch_to.default_content()
        except Exception as e:
            print(f"⚠️ Could not fill editor: {e}")
            driver.switch_to.default_content()

        # TEST 7: Product validation - try to save without product name
        print("🧪 Test 7: Testing product name validation...")
        add_product_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_PRODUCT_BUTTON)))
        safe_click(add_product_btn)
        time.sleep(1)

        # Try to save product without name
        save_product_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_PRODUCT_BUTTON)))
        safe_click(save_product_btn)
        time.sleep(1)

        # Verify validation message
        validation_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.VALIDATION_PRODUCT_NAME)))
        print(f"✅ Validation shown: {validation_msg.text}")

        # Fill Product Name
        product_name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.PRODUCT_NAME_FIELD)))
        safe_click(product_name_field)
        product_name_field.clear()
        product_name_field.send_keys("iphone")
        time.sleep(1)

        # Fill Synonyms
        synonyms_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SYNONYMS_FIELD)))
        safe_click(synonyms_field)
        synonyms_field.clear()
        synonyms_field.send_keys("mobiles")
        time.sleep(1)
        print("✅ Added product: iphone with synonym: mobiles")

        # Save product
        save_product_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_PRODUCT_BUTTON)))
        safe_click(save_product_btn)
        time.sleep(2)
        print("✅ Saved product")

        # TEST 8: Delete product
        print("🧪 Test 8: Testing product deletion...")
        delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.DELETE_BUTTON)))
        safe_click(delete_btn)
        time.sleep(1)

        # Confirm deletion
        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.YES_CONFIRM_BUTTON)))
        safe_click(yes_btn)
        time.sleep(2)
        print("✅ Deleted product")

        # TEST 9: Add and delete competitor
        print("🧪 Test 9: Testing competitor add and delete...")
        try:
            add_competitor_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_COMPETITOR_BUTTON)))
            safe_click(add_competitor_btn)
            time.sleep(1)

            # Fill competitor name
            competitor_name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.COMPETITOR_NAME_FIELD)))
            safe_click(competitor_name_field)
            competitor_name_field.clear()
            competitor_name_field.send_keys("heelo")
            time.sleep(1)
            print("✅ Entered competitor name: heelo")

            # Click check button to save
            check_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.CHECK_BUTTON)))
            safe_click(check_btn)
            time.sleep(2)
            print("✅ Saved competitor")

            # Delete competitor
            delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.DELETE_BUTTON)))
            safe_click(delete_btn)
            time.sleep(1)

            # Confirm deletion
            yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.YES_CONFIRM_BUTTON)))
            safe_click(yes_btn)
            time.sleep(2)
            print("✅ Deleted competitor")
        except Exception as e:
            print(f"⚠️ Competitor flow issue: {e}")

 # Click final Save Brand button
        final_save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BRAND_BUTTON)))
        safe_click(final_save_btn)
        time.sleep(3)
        print("✅ Clicked Save Brand button")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after add brand negative workflow")


if __name__ == "__main__":
    test_add_brand()
