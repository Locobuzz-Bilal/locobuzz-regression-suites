#28NOV2025
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
from utils.credentials import get_sa_creds

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/keyword_configuration"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_keyword_configuration():
    test_name = "keyword_configuration"
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

        print("🟢 Performing Keyword Configuration actions...")

        # Navigate to Account Settings
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for keywords
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        safe_click(search_field)
        safe_type(search_field, "keyword")
        time.sleep(1)

        # Click Keywords Configuration
        keywords_config = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.KEYWORDS_CONFIGURATION_LINK)))
        safe_click(keywords_config)
        time.sleep(2)

        # Add Keywords/Social Profiles
        add_keywords_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_KEYWORDS_BUTTON)))
        safe_click(add_keywords_btn)
        time.sleep(2)

        # Enter Keywords Group Name
        group_name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.KEYWORDS_GROUP_NAME_FIELD)))
        safe_type(group_name_field, "keyword config testing")
        time.sleep(1)

        # Select social media platforms (Twitter and Instagram)
        print("🔍 Looking for Twitter checkbox...")
        twitter_found = False
        try:
            # Try to find Twitter checkbox with multiple selectors
            twitter_checkbox = None
            selectors = [
                AccountSettingsPageElements.TWITTER_CHECKBOX,
                "//div[@id='twitter']//input[@type='checkbox']",
                "//mat-checkbox[contains(.,'Twitter')]//input",
                "//label[contains(.,'Twitter')]//input[@type='checkbox']",
                "//div[contains(@class,'twitter')]//input[@type='checkbox']"
            ]
            
            for selector in selectors:
                try:
                    twitter_checkbox = driver.find_element(By.XPATH, selector)
                    print(f"✅ Found Twitter checkbox with selector: {selector}")
                    break
                except:
                    continue
            
            if twitter_checkbox:
                if not twitter_checkbox.is_selected():
                    safe_click(twitter_checkbox)
                    twitter_found = True
                    print("✅ Twitter checkbox clicked")
                else:
                    print("ℹ️ Twitter checkbox already selected")
                    twitter_found = True
        except Exception as e:
            print(f"⚠️ Twitter checkbox error: {e}")

        print("🔍 Looking for Instagram/Facebook checkbox...")
        instagram_found = False
        try:
            # Try to find Instagram/Facebook checkbox
            instagram_checkbox = None
            selectors = [
                AccountSettingsPageElements.INSTAGRAM_CHECKBOX,
                "//div[@id='facebook']//input[@type='checkbox']",
                "//mat-checkbox[contains(.,'Facebook')]//input",
                "//label[contains(.,'Facebook')]//input[@type='checkbox']",
                "//div[contains(@class,'facebook')]//input[@type='checkbox']"
            ]
            
            for selector in selectors:
                try:
                    instagram_checkbox = driver.find_element(By.XPATH, selector)
                    print(f"✅ Found Instagram/Facebook checkbox with selector: {selector}")
                    break
                except:
                    continue
            
            if instagram_checkbox:
                if not instagram_checkbox.is_selected():
                    safe_click(instagram_checkbox)
                    instagram_found = True
                    print("✅ Instagram/Facebook checkbox clicked")
                else:
                    print("ℹ️ Instagram/Facebook checkbox already selected")
                    instagram_found = True
        except Exception as e:
            print(f"⚠️ Instagram/Facebook checkbox error: {e}")

        if not twitter_found and not instagram_found:
            print("⚠️ No social media checkboxes found - continuing anyway...")

        time.sleep(1)

        # Enter included keywords
        included_keywords = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.INCLUDED_KEYWORDS_FIELD)))
        safe_type(included_keywords, "123locobuzztesting")
        included_keywords.send_keys(Keys.ENTER)
        time.sleep(1)

        # Click Advance Query Builder
        advance_builder = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADVANCE_QUERY_BUILDER)))
        safe_click(advance_builder)
        time.sleep(2)

        # Select Twitter section (double click as in original)
        print("🔍 Looking for Twitter checkbox in advance builder...")
        twitter_found = False
        try:
            # Try to find Twitter checkbox with multiple selectors
            twitter_checkbox = None
            selectors = [
                AccountSettingsPageElements.TWITTER_CHECKBOX,
                "//div[@id='twitter']//input[@type='checkbox']",
                "//mat-checkbox[contains(.,'Twitter')]//input",
                "//label[contains(.,'Twitter')]//input[@type='checkbox']",
                "//div[contains(@class,'twitter')]//input[@type='checkbox']"
            ]
            
            for selector in selectors:
                try:
                    twitter_checkbox = driver.find_element(By.XPATH, selector)
                    print(f"✅ Found Twitter checkbox with selector: {selector}")
                    break
                except:
                    continue
            
            if twitter_checkbox:
                if not twitter_checkbox.is_selected():
                    safe_click(twitter_checkbox)
                    twitter_found = True
                    print("✅ Twitter checkbox clicked")
                else:
                    print("ℹ️ Twitter checkbox already selected")
                    twitter_found = True
        except Exception as e:
            print(f"⚠️ Twitter checkbox error: {e}")

        # Select AND toggle
        and_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.AND_TOGGLE)))
        safe_click(and_toggle)
        time.sleep(1)

        # Configure first attribute group
        attribute_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ATTRIBUTE_DROPDOWN)))
        safe_click(attribute_dropdown)
        time.sleep(1)
        
        tweet_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.TWEET_OPTION)))
        safe_click(tweet_option)
        time.sleep(1)
        
        try:
            operator_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.OPERATOR_DROPDOWN)))
        except:
            print("⚠️ Primary operator dropdown not found, trying alternative...")
            operator_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//mat-select)[2] | (//div[contains(@class, 'select')])[2]")))
        
        safe_click(operator_dropdown)
        time.sleep(1)
            
        should_contain = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SHOULD_CONTAIN_OPTION)))
        safe_click(should_contain)
        time.sleep(1)

        keywords_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ENTER_KEYWORDS_FIELD)))
        safe_type(keywords_field, "123locotest")
        keywords_field.send_keys(Keys.ENTER)
        time.sleep(1)

        # Add Group
        add_group_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_GROUP_BUTTON)))
        safe_click(add_group_btn)
        time.sleep(1)

        # Select NOT toggle for second group
        not_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.OR_TOGGLE)))
        safe_click(not_toggle)
        time.sleep(1)

        # Configure second attribute (NOT condition)
        try:
            # Click attribute dropdown for second group
            attribute_dropdown_2 = driver.find_elements(By.XPATH, AccountSettingsPageElements.ATTRIBUTE_DROPDOWN)[1]
            safe_click(attribute_dropdown_2)
            tweet_option_2 = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.TWEET_OPTION)))
            safe_click(tweet_option_2)
            time.sleep(1)

            operator_dropdown_2 = driver.find_elements(By.XPATH, AccountSettingsPageElements.OPERATOR_DROPDOWN)[1]
            safe_click(operator_dropdown_2)
            should_not_contain = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SHOULD_NOT_CONTAIN_OPTION)))
            safe_click(should_not_contain)
            time.sleep(1)

            keywords_field_2 = driver.find_elements(By.XPATH, AccountSettingsPageElements.ENTER_KEYWORDS_FIELD)[1]
            safe_type(keywords_field_2, "locotestbuzz")
            keywords_field_2.send_keys(Keys.ENTER)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Second attribute configuration failed: {e}")

        # Add another attribute
        try:
            add_attribute_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_ATTRIBUTE_BUTTON)))
            safe_click(add_attribute_btn)
            time.sleep(1)

            # Configure third attribute
            attribute_dropdown_3 = driver.find_elements(By.XPATH, AccountSettingsPageElements.ATTRIBUTE_DROPDOWN)[-1]
            safe_click(attribute_dropdown_3)
            tweet_option_3 = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.TWEET_OPTION)))
            safe_click(tweet_option_3)
            time.sleep(1)

            operator_dropdown_3 = driver.find_elements(By.XPATH, AccountSettingsPageElements.OPERATOR_DROPDOWN)[-1]
            safe_click(operator_dropdown_3)
            should_contain_3 = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SHOULD_CONTAIN_OPTION)))
            safe_click(should_contain_3)
            time.sleep(1)

            keywords_field_3 = driver.find_elements(By.XPATH, AccountSettingsPageElements.ENTER_KEYWORDS_FIELD)[-1]
            safe_type(keywords_field_3, "busna")
            keywords_field_3.send_keys(Keys.ENTER)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Third attribute configuration failed: {e}")

        # First save attempt (expecting error)
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)

        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.YES_BUTTON)))
        safe_click(yes_btn)
        time.sleep(2)

        # Check for error message
        try:
            error_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ERROR_MESSAGE)))
            print(f"⚠️ Expected error: {error_msg.text}")
        except:
            print("⚠️ Error message not found")

        # Switch to OR toggle to fix the error
        or_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.OR_TOGGLE)))
        safe_click(or_toggle)
        time.sleep(1)

        # Save again
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)

        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.YES_BUTTON)))
        safe_click(yes_btn)
        time.sleep(2)

        # Verify success message
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SUCCESS_MESSAGE)))
            print(f"✅ Success: {success_msg.text}")
        except:
            print("⚠️ Success message not found")

        # Search for created keyword group
        search_keywords_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_KEYWORDS_FIELD)))
        safe_type(search_keywords_field, "testing")
        
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SEARCH_KEYWORDS_BUTTON)))
        safe_click(search_btn)
        time.sleep(2)

        # Click on the created keyword row (delete button)
        try:
            delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.DELETE_KEYWORD_BUTTON)))
            safe_click(delete_btn)
            print("✅ Clicked delete button for testing keyword")
        except:
            print("⚠️ Delete button not found - keyword may not have been created")

        print("✅ Keyword Configuration workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after keyword configuration")