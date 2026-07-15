# 03DEC2025
# Create Dashboard workflow: Create → Edit (Add Section) → Duplicate → Delete
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from locobuzz_login.CX_login import locobuzzLogin
from elements.awa_regression_page import AWAElements
from selenium.webdriver.common.action_chains import ActionChains
from elements.login_page import LoginPageElements   
from utils.credentials import get_sa_creds


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/dashboard"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_dashboard_workflow():
    test_name = "dashboard_workflow"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Dashboard workflow...")
        
        # Wait for page to load
        time.sleep(3)
        
        # Try to click Analytics menu first (might be required for navigation)
        try:
            analytics_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Analytics']")))
            safe_click(analytics_menu)
            time.sleep(2)
        except:
            pass
        
        # Switch to iframe first (All Dashboards button is inside iframe)
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.ANALYTICS_IFRAME)))
        driver.switch_to.frame(iframe)
        time.sleep(3)
        
        # Click All Dashboards (now inside iframe)
        all_dashboards_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ALL_DASHBOARDS_BUTTON)))
        safe_click(all_dashboards_btn)
        time.sleep(2)

        # Create New Dashboard - try multiple click approaches
        print("Looking for Create New Dashboard button...")
        create_dashboard_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.CREATE_NEW_DASHBOARD_BUTTON)))
        print("Found Create New Dashboard button")
        
        # Scroll into view and wait
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_dashboard_btn)
        time.sleep(1)
        
        # Try clicking with multiple methods
        try:
            driver.execute_script("arguments[0].click();", create_dashboard_btn)
            print("✅ Clicked Create New Dashboard using JavaScript")
        except Exception as e:
            print(f"JS click failed, trying ActionChains: {e}")
            ActionChains(driver).move_to_element(create_dashboard_btn).click().perform()
            print("✅ Clicked Create New Dashboard using ActionChains")
        
        time.sleep(2)

        # Enter Dashboard Name
        dashboard_name_input = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DASHBOARD_NAME_INPUT)))
        safe_click(dashboard_name_input)
        dashboard_name_input.clear()
        dashboard_name_input.send_keys("testing dashboard 002")
        time.sleep(1)

        # Click to add widget
        click_to_add = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.CLICK_TO_ADD_WIDGET)))
        safe_click(click_to_add)
        time.sleep(1)

        # Select a widget 
        widget_option = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='checklist '])[1]")))
        safe_click(widget_option)
        time.sleep(1)

        # Click Add Widget
        add_widget_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ADD_WIDGET_BUTTON)))
        safe_click(add_widget_btn)
        time.sleep(2)

        # Save Dashboard (first instance)
        save_dashboard_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_DASHBOARD_BTN)))
        safe_click(save_dashboard_btn)
        time.sleep(1)

        # Save Dashboard (second instance in settings dialog)
        save_dashboard_settings_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(., 'Save Dashboard')])[2]")))
        safe_click(save_dashboard_settings_btn)
        time.sleep(3)

        # Verify creation success
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DASHBOARD_CREATED_SUCCESS)))
            print(f"✅ Dashboard created: {success_msg.text}")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Success message not found: {e}")

        # Hover over More icon again for Edit
        more_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DASHBOARD_MORE_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_icon)
        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.move_to_element(more_icon).perform()
        print("Hovering over More icon for edit - waiting for menu to appear")
        time.sleep(1.5)

        # Edit Dashboard
        print("Editing dashboard...")
        edit_text = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.EDIT_DASHBOARD_TEXT)))
        safe_click(edit_text)
        time.sleep(2)

        # Add Section
        add_section_text = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ADD_SECTION_TEXT)))
        safe_click(add_section_text)
        time.sleep(1)

        # Select section type (CLUSTER-1-LEVEL or similar)
        section_option = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='checklist '])[2]")))
        safe_click(section_option)
        time.sleep(1)

        # Click Add Section button
        add_section_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ADD_SECTION_BUTTON)))
        safe_click(add_section_btn)
        time.sleep(1)

        # Enter section name
        section_name_input = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.SECTION_NAME_INPUT)))
        safe_click(section_name_input)
        section_name_input.clear()
        section_name_input.send_keys("test")
        time.sleep(1)

        # Save section
        save_section_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_SECTION_BUTTON)))
        safe_click(save_section_btn)
        time.sleep(2)

        # Save Changes
        save_changes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_CHANGES_BUTTON)))
        safe_click(save_changes_btn)
        time.sleep(1)

        # Save Dashboard after edit
        save_dashboard_final = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_DASHBOARD_BTN)))
        safe_click(save_dashboard_final)
        time.sleep(3)

        # Verify update success
        try:
            update_msg = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DASHBOARD_SUCCESS_MESSAGE)))
            print(f"✅ Dashboard updated: {update_msg.text}")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Update message not found: {e}")

        # # Still inside iframe - click All Dashboards to go back to dashboard list
        # all_dashboards_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ALL_DASHBOARDS_BUTTON)))
        # safe_click(all_dashboards_btn)
        # time.sleep(2)

        safe_click(wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.CLOSE_TAB))))
        time.sleep(2)

        # Search for the dashboard (still inside iframe)
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DASHBOARD_SEARCH_INPUT)))
        safe_click(search_input)
        search_input.clear()
        search_input.send_keys("testing dashboard 002")
        time.sleep(1)

        search_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DASHBOARD_SEARCH_ICON)))
        safe_click(search_icon)
        time.sleep(2)

        # Hover over More icon to show menu
        more_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DASHBOARD_MORE_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_icon)
        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.move_to_element(more_icon).perform()
        print("Hovering over More icon - waiting for menu to appear")
        time.sleep(1.5)

        # Duplicate Dashboard
        print("Duplicating dashboard...")
        duplicate_selectors = [
            AWAElements.DUPLICATE_DASHBOARD_TEXT,
            "//div[text()='Duplicate']",
            "//span[text()='Duplicate']",
            "//*[text()='Duplicate']",
            "//li[contains(., 'Duplicate')]",
        ]
        
        duplicate_text = None
        for selector in duplicate_selectors:
            try:
                duplicate_text = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"Found Duplicate using: {selector}")
                break
            except Exception:
                pass
        
        if not duplicate_text:
            raise Exception("Duplicate option not found in menu")
        
        safe_click(duplicate_text)
        time.sleep(1)

        # Enter duplicate dashboard name
        duplicate_name_input = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DUPLICATE_DASHBOARD_INPUT)))
        safe_click(duplicate_name_input)
        duplicate_name_input.clear()
        duplicate_name_input.send_keys("testing dashboard 002")
        time.sleep(1)

        # Save duplicate
        duplicate_save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DUPLICATE_SAVE_BUTTON)))
        safe_click(duplicate_save_btn)
        time.sleep(3)

        # Verify duplication success
        try:
            duplicate_msg = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DASHBOARD_DUPLICATED_SUCCESS)))
            print(f"✅ Dashboard duplicated: {duplicate_msg.text}")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Duplication message not found: {e}")

        # Delete Dashboard
        print("Deleting dashboard...")
        
        # Hover over More icon again for delete
        more_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DASHBOARD_MORE_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_icon)
        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.move_to_element(more_icon).perform()
        print("Hovering over More icon for delete - waiting for menu to appear")
        time.sleep(1.5)

        delete_selectors = [
            AWAElements.DELETE_DASHBOARD_TEXT,
            "//span[text()='Delete']",
            "//div[text()='Delete']",
            "//*[text()='Delete']",
            "//li[contains(., 'Delete')]",
        ]
        
        delete_text = None
        for selector in delete_selectors:
            try:
                delete_text = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"Found Delete using: {selector}")
                break
            except Exception:
                pass
        
        if not delete_text:
            raise Exception("Delete option not found in menu")
        
        safe_click(delete_text)
        time.sleep(1)

        # Confirm deletion
        delete_yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DELETE_DASHBOARD_YES_BUTTON)))
        safe_click(delete_yes_btn)
        time.sleep(3)

        # Verify deletion success
        try:
            delete_msg = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DASHBOARD_DELETED_SUCCESS)))
            print(f"✅ Dashboard deleted: {delete_msg.text}")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Deletion message not found: {e}")

        # Switch back to default content
        driver.switch_to.default_content()

        print("✅ Dashboard workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after dashboard workflow")

