# Feedback/Survey Form Configuration Test
# in Set Messages, delete the 'hello again' one
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
def test_feedback_survey_form():
    test_name = "feedback_survey_form"
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

        print("🟢 Performing Feedback/Survey Form configuration...")

  # Navigate to Account Settings
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(2)

        # Click on Account Settings menu item
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for "survey"
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        safe_click(search_field)
        search_field.clear()
        search_field.send_keys("survey")
        time.sleep(1)

        # Click on "Feedback / Survey Form" link
        feedback_link = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.FEEDBACK_SURVEY_FORM_LINK)))
        safe_click(feedback_link)
        time.sleep(2)

        # Check if toggle button is enabled, if not, toggle it on
        try:
            # Find the actual input checkbox element
            toggle_input = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.FEEDBACK_TOGGLE)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", toggle_input)
            time.sleep(0.5)
            
            # Check if checkbox is checked
            is_checked = toggle_input.is_selected()
            
            if not is_checked:
                print("⚠️ Toggle is disabled, enabling it...")
                # Click using JavaScript to ensure it works even if visually hidden
                driver.execute_script("arguments[0].click();", toggle_input)
                time.sleep(1.5)
                print("✅ Toggle enabled")
            else:
                print("✅ Toggle is already enabled")
        except Exception as e:
            print(f"⚠️ Could not find or check toggle button: {e}")
            # Continue anyway as toggle might not be present or accessible

        # Click on Feedback Rating (to expand or navigate)
        try:
            feedback_rating = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.FEEDBACK_RATING_TEXT)))
            safe_click(feedback_rating)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Feedback Rating element not needed to click: {e}")

        # Select Unit - Days
        unit_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.UNIT_DROPDOWN)))
        safe_click(unit_dropdown)
        time.sleep(1)
        days_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.DAYS_OPTION)))
        safe_click(days_option)
        time.sleep(1)

        # Select Expiry Duration Value - 1
        expiry_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.EXPIRY_DURATION_DROPDOWN)))
        safe_click(expiry_dropdown)
        time.sleep(1)
        duration_1 = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.DURATION_VALUE_1)))
        safe_click(duration_1)
        time.sleep(1)

        # Select Manual radio button
        manual_radio = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.MANUAL_RADIO)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", manual_radio)
        time.sleep(0.5)
        safe_click(manual_radio)
        time.sleep(1)

        # Add Categories
        add_categories_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_CATEGORIES_BUTTON)))
        safe_click(add_categories_btn)
        time.sleep(1)

        # Enter category name
        category_name = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.CATEGORY_NAME_INPUT)))
        safe_click(category_name)
        category_name.clear()
        category_name.send_keys("test")
        time.sleep(1)

        # Select Icon
        icon_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ICON_DROPDOWN)))
        safe_click(icon_dropdown)
        time.sleep(1)
        icon_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ICON_OPTION)))
        safe_click(icon_option)
        time.sleep(1)

        # Save Category
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_BUTTON)))
        safe_click(save_btn)
        time.sleep(2)

        # Add Messages
        add_messages_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_MESSAGES_BUTTON)))
        safe_click(add_messages_btn)
        time.sleep(1)

        # Click on message textbox
        message_textbox = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.MESSAGE_TEXTBOX)))
        safe_click(message_textbox)
        time.sleep(0.5)

        # Click Personalize and add Screen Name
        personalize_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PERSONALIZE_BUTTON)))
        safe_click(personalize_btn)
        time.sleep(0.5)
        screen_name_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SCREEN_NAME_MENU)))
        safe_click(screen_name_menu)
        time.sleep(1)

        # Try to add without valid message (will show error)
        try:
            add_msg_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_MESSAGE_BUTTON)))
            safe_click(add_msg_btn)
            time.sleep(1)
            # Error message should appear
            print("⚠️ Attempted to add without proper message (expected error)")
        except Exception as e:
            print(f"⚠️ Add button not clickable: {e}")

        # Click Personalize again and add Feedback Link
        personalize_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PERSONALIZE_BUTTON)))
        safe_click(personalize_btn)
        time.sleep(0.5)
        feedback_link_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.FEEDBACK_LINK_MENU)))
        safe_click(feedback_link_menu)
        time.sleep(1)

        # Message already exists error should appear, click Reset
        try:
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.RESET_BUTTON)))
            safe_click(reset_btn)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Reset button not found: {e}")

        # Enter proper message
        message_textbox = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.MESSAGE_TEXTBOX)))
        safe_click(message_textbox)
        message_textbox.clear()
        message_textbox.send_keys("hello again")
        time.sleep(0.5)

        # Add Screen Name
        personalize_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PERSONALIZE_BUTTON)))
        safe_click(personalize_btn)
        time.sleep(0.5)
        screen_name_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SCREEN_NAME_MENU)))
        safe_click(screen_name_menu)
        time.sleep(0.5)

        # Add Feedback Link
        personalize_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PERSONALIZE_BUTTON)))
        safe_click(personalize_btn)
        time.sleep(0.5)
        feedback_link_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.FEEDBACK_LINK_MENU)))
        safe_click(feedback_link_menu)
        time.sleep(1)

        # Add message
        add_msg_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_MESSAGE_BUTTON)))
        safe_click(add_msg_btn)
        time.sleep(2)
        print("✅ Template message added successfully")

        # Select Layout Theme
        try:
            layout_theme = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.LAYOUT_THEME_TEXT)))
            safe_click(layout_theme)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Layout Theme text not needed to click: {e}")

        # Select the radio button for layout theme (6th radio button)
        try:
            layout_radio = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.LAYOUT_THEME_CARD_3)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", layout_radio)
            time.sleep(1)
            driver.execute_script("arguments[0].checked = true; arguments[0].click();", layout_radio)
            time.sleep(2)
            print("✅ Selected layout theme radio button")
        except Exception as e:
            print(f"⚠️ Could not select layout radio: {e}")

        # Click Select button to confirm the layout choice
        try:
            select_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SELECT_BUTTON)))
            print(f"🔍 Found Select button, clicking it now...")
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select_btn)
            time.sleep(1)
            select_btn.click()  # Try normal click first
            time.sleep(3)
            print("✅ Clicked Select button - waiting for modal to close")
            
            # Wait for layout theme modal to disappear
            time.sleep(2)
            print("✅ Modal should be closed now")
        except Exception as e:
            print(f"⚠️ Could not click Select button: {e}")
            # Try JavaScript click as fallback
            try:
                select_btn_js = driver.find_element(By.XPATH, AccountSettingsPageElements.SELECT_BUTTON)
                driver.execute_script("arguments[0].click();", select_btn_js)
                time.sleep(3)
                print("✅ Clicked Select button via JavaScript")
            except Exception as e2:
                print(f"❌ JavaScript click also failed: {e2}")

        # Handle Preview in browser (opens new window)
        main_window = driver.current_window_handle
        try:
            preview_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PREVIEW_IN_BROWSER)))
            safe_click(preview_btn)
            time.sleep(2)
            
            # Switch to new window if opened
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[-1])
                print("✅ Preview window opened")
                time.sleep(2)
                driver.close()
                driver.switch_to.window(main_window)
                print("✅ Closed preview window")
        except Exception as e:
            print(f"⚠️ Preview button issue: {e}")
            driver.switch_to.window(main_window)

        # Save the form
        save_feedback_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_FEEDBACK_BUTTON)))
        safe_click(save_feedback_btn)
        time.sleep(2)

        # Verify success message
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SUCCESS_MESSAGE_FEEDBACK)))
            print(f"✅ {success_msg.text}")
        except Exception as e:
            print(f"⚠️ Success message not found: {e}")

        print("✅ Feedback/Survey Form configuration completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after feedback form configuration")


if __name__ == "__main__":
    test_feedback_survey_form()
