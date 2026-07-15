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
    screenshots_dir = "tests/screenshots/category_mapping"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_category_mapping():
    """Test Category Mapping creation and validation"""
    test_name = "category_mapping"
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

        print("🟢 Testing Category Mapping creation...")

        # Navigate to Account Settings
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for category mapping
        search_field = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        safe_click(search_field)
        safe_type(search_field, "category")
        time.sleep(1)

        # Click on Category Mapping
        category_mapping_link = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CATEGORY_MAPPING_LINK)))
        safe_click(category_mapping_link)
        time.sleep(2)

        # Click Create New Category
        create_category_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CREATE_NEW_CATEGORY_BUTTON)))
        safe_click(create_category_btn)
        time.sleep(1)

        # Enter Category Name
        category_name = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CATEGORY_NAME_FIELD)))
        safe_click(category_name)
        safe_type(category_name, "category testing")

        # Save Category
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SAVE_BUTTON)))
        safe_click(save_btn)
        time.sleep(1)

        # Enter Keywords
        keywords_field = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ENTER_KEYWORDS_FIELD)))
        safe_click(keywords_field)
        safe_type(keywords_field, "loco987buzz")
        time.sleep(1)

        # Open Advance Query Builder
        adv_query_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ADVANCE_QUERY_BUILDER)))
        safe_click(adv_query_btn)
        time.sleep(1)

        # Fill Query Builder fields
        all_words_and = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ALL_WORDS_AND_FIELD)))
        safe_click(all_words_and)
        safe_type(all_words_and, "qwertyuio")
        any_words_or = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ANY_WORDS_OR_FIELD)))
        safe_click(any_words_or)
        safe_type(any_words_or, "sdfcghjblkm,;")
        none_words_not = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.NONE_WORDS_NOT_FIELD)))
        safe_click(none_words_not)
        safe_type(none_words_not, "drftghjkl;")

        # Select OR radio
        or_radio = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.OR_RADIO)))
        safe_click(or_radio)
        time.sleep(1)


        # Add Group
        add_group_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ADD_GROUP_BUTTON)))
        safe_click(add_group_btn)
        time.sleep(1)

        # Fill new group fields
        all_words_and_2 = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ALL_WORDS_AND_FIELD + "[2]")))
        safe_click(all_words_and_2)
        safe_type(all_words_and_2, "awerstyuiopk")
        chip_input_1 = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CHIP_LIST_INPUT_1)))
        safe_click(chip_input_1)
        safe_type(chip_input_1, "swedrftgyuhijo")
        chip_input_2 = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CHIP_LIST_INPUT_2)))
        safe_click(chip_input_2)
        safe_type(chip_input_2, "w3ertyuij")
        chip_input_2.send_keys(Keys.ENTER)
        time.sleep(1)

        # Delete group (if needed)
        try:
            delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.DELETE_BUTTON)))
            safe_click(delete_btn)
            time.sleep(1)
        except Exception:
            pass

        # Save Keywords
        save_keywords_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SAVE_BUTTON)))
        safe_click(save_keywords_btn)
        time.sleep(1)

        # Confirm Yes
        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.YES_BUTTON)))
        safe_click(yes_btn)
        time.sleep(1)

        # Sort actions
        sort_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SORT_BUTTON)))
        safe_click(sort_btn)
        ascending_radio = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.ASCENDING_RADIO)))
        safe_click(ascending_radio)
        sort_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SORT_BUTTON)))
        safe_click(sort_btn)
        category_name_radio = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CATEGORY_NAME_RADIO)))
        safe_click(category_name_radio)
        time.sleep(1)

        # Select Brand Mentions
        brand_mentions_combo = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.BRAND_MENTIONS_COMBOBOX)))
        safe_click(brand_mentions_combo)
        testing_option = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.TESTING_OPTION)))
        safe_click(testing_option)
        time.sleep(1)

        # Select Based on subject and body radio
        based_on_radio = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.BASED_ON_SUBJECT_BODY_RADIO)))
        safe_click(based_on_radio)
        time.sleep(1)

        # Ticket Category Tagging
        ticket_category_label = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.TICKET_CATEGORY_TAGGING_LABEL)))
        safe_click(ticket_category_label)
        check_circle_category = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CHECK_CIRCLE_CATEGORY)))
        safe_click(check_circle_category)
        time.sleep(1)

        # Add chip inputs
        chip_input_0 = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CHIP_LIST_INPUT_1)))
        safe_click(chip_input_0)
        safe_type(chip_input_0, "vgjhbkm/,l")
        chip_input_1 = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.CHIP_LIST_INPUT_2)))
        safe_click(chip_input_1)
        safe_type(chip_input_1, "awsedrftgyhujikol")
        time.sleep(1)

        # Save final
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ListeningSettingsPageElements.SAVE_BUTTON)))
        safe_click(save_btn)
        time.sleep(2)

        # Verify Success Message
        success_msg = wait.until(EC.presence_of_element_located((By.XPATH, ListeningSettingsPageElements.SUCCESS_MESSAGE_GENERIC)))
        assert success_msg.is_displayed(), "Success message not displayed"
        print("✅ Category Mapping saved successfully!")

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
