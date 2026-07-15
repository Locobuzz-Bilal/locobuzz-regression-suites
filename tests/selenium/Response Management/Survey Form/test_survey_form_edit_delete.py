# 09DEC2025
# Survey Form Edit and Delete with Conditional Logic
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from locobuzz_login.CX_login import locobuzzLogin
from elements.survey_form_page import SurveyFormElements
from elements.accountSettings_page import AccountSettingsPageElements
from utils.credentials import get_sa_creds


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/survey"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_survey_form_edit_delete():
    test_name = "survey_form_edit_delete"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Survey Form Edit and Delete workflow...")
    
        # Navigate to Account Settings
        print("Clicking profile menu...")
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        
        print("Clicking Account Settings...")
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)
        
        # Search for Survey Form
        print("Searching for Survey Form...")
        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        search_input.click()
        search_input.send_keys("survey form")
        time.sleep(1)
        
        # Click Survey Form link
        print("Clicking Survey Form link...")
        survey_form_link = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.SURVEY_FORM_LINK)))
        safe_click(survey_form_link)
        time.sleep(3)
        
        # Click more_vert menu (three dots)
        print("Clicking more menu...")
        more_menu = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.MORE_MENU_BUTTON)))
        safe_click(more_menu)
        time.sleep(1)
        
        # Click Edit menu item
        print("Clicking Edit...")
        edit_menu = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.EDIT_MENU_ITEM)))
        safe_click(edit_menu)
        time.sleep(2)
        
        # Click on "testing 1" field
        print("Clicking testing 1 field...")
        testing1_field = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.TESTING_1_FIELD)))
        safe_click(testing1_field)
        time.sleep(1)
        
        # Click "Set conditional logic"
        print("Clicking Set conditional logic...")
        conditional_logic = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.SET_CONDITIONAL_LOGIC)))
        safe_click(conditional_logic)
        time.sleep(2)
        
        # Click AND toggle button
        print("Clicking AND toggle...")
        and_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.OR_TOGGLE_BUTTON)))
        safe_click(and_toggle)
        time.sleep(1)
        
        # Select Attribute - testing 3
        print("Selecting Attribute: testing 3...")
        attribute_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.ATTRIBUTE_DROPDOWN)))
        safe_click(attribute_dropdown)
        time.sleep(1)
        
        testing3_option = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.TESTING_3_OPTION)))
        safe_click(testing3_option)
        time.sleep(1)
        
        # Select Operator - greater than
        print("Selecting Operator: greater than...")
        operator_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.OPERATOR_DROPDOWN)))
        safe_click(operator_dropdown)
        time.sleep(1)
        
        greater_than_option = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.GREATER_THAN_OPTION)))
        safe_click(greater_than_option)
        time.sleep(1)
        
        # Enter Value = 2
        print("Entering value: 2...")
        value_input = wait.until(EC.visibility_of_element_located((By.XPATH, SurveyFormElements.VALUE_INPUT)))
        value_input.click()
        value_input.clear()
        value_input.send_keys("2")
        time.sleep(1)
        
        # Click "+ Add Attribute"
        print("Clicking + Add Attribute...")
        add_attribute = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.ADD_ATTRIBUTE_BUTTON)))
        safe_click(add_attribute)
        time.sleep(1)
        
        # Select second Attribute - testing 3
        print("Selecting second Attribute: testing 3...")
        attribute_dropdown2 = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.ATTRIBUTE_DROPDOWN_5)))
        safe_click(attribute_dropdown2)
        time.sleep(1)
        
        testing3_option2 = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.TESTING_3_OPTION)))
        safe_click(testing3_option2)
        time.sleep(1)
        
        # Select second Operator - is empty
        print("Selecting second Operator: is empty...")
        operator_dropdown2 = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.OPERATOR_DROPDOWN_6)))
        safe_click(operator_dropdown2)
        time.sleep(1)
        
        is_empty_option = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.IS_EMPTY_OPTION)))
        safe_click(is_empty_option)
        time.sleep(1)
        
        # Click "+ Add Group"
        print("Clicking + Add Group...")
        add_group = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.ADD_GROUP_BUTTON)))
        safe_click(add_group)
        time.sleep(1)
        
        # Click OR toggle in new group
        print("Clicking OR toggle in new group...")
        or_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.OR_TOGGLE_BUTTON)))
        safe_click(or_toggle)
        time.sleep(1)
        
        # Select Attribute in new group - testing 2
        print("Selecting Attribute in new group: testing 2...")
        attribute_dropdown3 = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.ATTRIBUTE_DROPDOWN_7)))
        safe_click(attribute_dropdown3)
        time.sleep(1)
        
        testing2_option = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.TESTING_2_OPTION)))
        safe_click(testing2_option)
        time.sleep(1)
        
        # Select Operator - does not equal
        print("Selecting Operator: does not equal...")
        operator_dropdown3 = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.OPERATOR_DROPDOWN_8)))
        safe_click(operator_dropdown3)
        time.sleep(1)
        
        not_equal_option = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.NOT_EQUAL_OPTION)))
        safe_click(not_equal_option)
        time.sleep(1)
        
        # Enter Value = 3
        print("Entering value: 3...")
        value_input2 = wait.until(EC.visibility_of_element_located((By.XPATH, SurveyFormElements.VALUE_INPUT_7)))
        value_input2.click()
        value_input2.clear()
        value_input2.send_keys("3")
        time.sleep(1)
        
        # Delete the second condition using delete_outline (3rd occurrence)
        print("Deleting second condition...")
        time.sleep(1)  # Wait for elements to be ready
        delete_icons_list = driver.find_elements(By.XPATH, SurveyFormElements.DELETE_OUTLINE_ICON)
        print(f"Found {len(delete_icons_list)} delete_outline icons")
        if len(delete_icons_list) > 2:
            delete_icon = delete_icons_list[2]
            safe_click(delete_icon)
        else:
            print(f"⚠️ Expected at least 3 delete_outline icons, found {len(delete_icons_list)}")
        time.sleep(1)
        
        # Click Save button
        print("Clicking Save button...")
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.SAVE_BUTTON)))
        safe_click(save_button)
        time.sleep(2)
        
        # Verify "Condition logic saved" message
        print("Verifying condition logic saved message...")
        saved_message = wait.until(EC.visibility_of_element_located((By.XPATH, SurveyFormElements.CONDITION_LOGIC_SAVED_MESSAGE)))
        assert saved_message.is_displayed(), "Condition logic saved message not displayed"
        print("✓ Condition logic saved message verified")
        time.sleep(1)
        
        # Click on "testing 2" field
        print("Clicking testing 2 field...")
        testing2_field = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.TESTING_2_FIELD)))
        safe_click(testing2_field)
        time.sleep(1)
        
        # Delete the field using delete icon (4th occurrence of 'delete')
        print("Deleting testing 2 field...")
        time.sleep(1)  # Wait for elements to be ready
        delete_icons = driver.find_elements(By.XPATH, SurveyFormElements.DELETE_ICON)
        print(f"Found {len(delete_icons)} delete icons")
        if len(delete_icons) > 3:
            safe_click(delete_icons[3])
        else:
            print(f"⚠️ Expected at least 4 delete icons, found {len(delete_icons)}")
        time.sleep(1)
        
        # Click Update Form button
        print("Clicking Update Form button...")
        update_form_button = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.UPDATE_FORM_BUTTON)))
        safe_click(update_form_button)
        time.sleep(2)
        
        # Verify "Form updated successfully." message
        print("Verifying form updated message...")
        updated_message = wait.until(EC.visibility_of_element_located((By.XPATH, SurveyFormElements.FORM_UPDATED_MESSAGE)))
        assert updated_message.is_displayed(), "Form updated successfully message not displayed"
        print("✓ Form updated successfully message verified")
        time.sleep(1)
        
        # Click more_vert menu again
        print("Clicking more menu for deletion...")
        more_menu2 = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.MORE_MENU_BUTTON)))
        safe_click(more_menu2)
        time.sleep(1)
        
        # Click Delete menu item
        print("Clicking Delete...")
        delete_menu = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.DELETE_MENU_ITEM)))
        safe_click(delete_menu)
        time.sleep(1)
        
        # Click Yes button in confirmation dialog
        print("Confirming deletion...")
        yes_button = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.DELETE_CONFIRMATION_YES)))
        safe_click(yes_button)
        time.sleep(2)
        
        # Verify "Form deleted successfully." message
        print("Verifying form deleted message...")
        deleted_message = wait.until(EC.visibility_of_element_located((By.XPATH, SurveyFormElements.FORM_DELETED_MESSAGE)))
        assert deleted_message.is_displayed(), "Form deleted successfully message not displayed"
        print("✓ Form deleted successfully message verified")
        
        print("✅ Survey Form edit and delete workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after Survey Form edit/delete workflow")
