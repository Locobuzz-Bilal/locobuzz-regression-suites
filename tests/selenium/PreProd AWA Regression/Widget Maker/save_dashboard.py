import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import elements and utilities
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from elements.awa_regression_page import AWAElements
from elements.login_page import LoginPageElements
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from utils.credentials import get_sa_creds

def safe_click(element):
    """Safely click an element using JavaScript if normal click fails"""
    try:
        element.click()
    except Exception:
        driver = element.parent
        driver.execute_script("arguments[0].click();", element)


def test_save_dashboard_workflow():
    """
    Test: Edit Widget → Save Widget → Save Dashboard → Verify success → Dismiss
    Flow: Login → Switch to iframe → Edit Widget → Save → Save Dashboard → Verify message
    """
    driver = None
    test_name = "save_dashboard_workflow"
    
    try:
        with allure.step("Login"):
            print("\u25AA Logging in for Email Other Actions...")
            try:
                username, password = get_sa_creds()
            except RuntimeError as cred_err:
                pytest.skip(f"Skipping: {cred_err}")
            driver = locobuzzLoginPreProd(username, password)
            wait = WebDriverWait(driver, 25)
        
        print("🟢 Performing Save Dashboard actions...")
        
        # Switch to analytics iframe
        iframe = wait.until(
            EC.presence_of_element_located((By.XPATH, AWAElements.ANALYTICS_IFRAME))
        )
        driver.switch_to.frame(iframe)
        print("✅ Switched to analyticsFrame")
        time.sleep(2)
        
        # Click "Edit Widget" text
        #hover over MORE
        time.sleep(1)  # Wait for page to stabilize
        more_icon = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.MORE)))
        # Re-find element to avoid stale reference
        time.sleep(0.5)
        more_icon = driver.find_element(By.XPATH, AWAElements.MORE)
        webdriver.ActionChains(driver).move_to_element(more_icon).perform()
        print("✅ Hovered over MORE icon")
        time.sleep(1)

        edit_widget = wait.until(
            EC.element_to_be_clickable((By.XPATH, AWAElements.EDIT_WIDGET_TEXT))
        )
        safe_click(edit_widget)
        print("✅ Clicked Edit Widget")
        time.sleep(2)
        
        # Click "Save Widget" button
        save_widget_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_WIDGET_BTN))
        )
        safe_click(save_widget_btn)
        print("✅ Clicked Save Widget button")
        time.sleep(1)
        
        # Click "Save" button
        save_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_BTN))
        )
        safe_click(save_btn)
        print("✅ Clicked Save button")
        time.sleep(2)
        
        # Click "Save" button again (if it appears - sometimes there's a confirmation)
        try:
            save_btn_2 = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_BTN))
            )
            safe_click(save_btn_2)
            print("✅ Clicked Save button (confirmation)")
            time.sleep(1)
        except:
            print("ℹ️ No second Save button needed")
        
        # Click "Save Dashboard" button
        save_dashboard_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_DASHBOARD_BTN))
        )
        safe_click(save_dashboard_btn)
        print("✅ Clicked Save Dashboard button")
        time.sleep(2)
        
        # Verify "Dashboard updated successfully" message appears
        success_message = wait.until(
            EC.presence_of_element_located((By.XPATH, AWAElements.DASHBOARD_SUCCESS_MESSAGE))
        )
        print(f"✅ Success message displayed: {success_message.text}")
        
        # Click on the success message (if clickable - as per Playwright script)
        try:
            safe_click(success_message)
            print("✅ Clicked success message")
            time.sleep(0.5)
        except:
            print("ℹ️ Success message not clickable")
        
        # Click "Dismiss" button
        dismiss_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, AWAElements.DISMISS_BTN))
        )
        safe_click(dismiss_btn)
        print("✅ Clicked Dismiss button")
        time.sleep(1)
        
        # Switch back to default content
        driver.switch_to.default_content()
        
        print("✅ Save Dashboard workflow completed successfully")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        if driver:
            # Take screenshot on failure
            screenshot_dir = "tests/screenshots/widget_maker"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = f"{screenshot_dir}/{test_name}_error_{int(time.time())}.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
        pytest.fail(f"Test failed: {e}")
        
    finally:
        if driver:
            driver.quit()
            print("🧹 Browser closed")


if __name__ == "__main__":
    test_save_dashboard_workflow()
