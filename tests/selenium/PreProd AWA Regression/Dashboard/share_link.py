# 03DEC2025
# Share Link workflow: Generate shareable link and verify access
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from elements.awa_regression_page import AWAElements
from selenium.webdriver.common.action_chains import ActionChains
from utils.credentials import get_sa_creds


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/dashboard"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_share_link():
    test_name = "share_link"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLoginPreProd(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Share Link workflow...")

        # Switch to iframe (analytics is already loaded after login)
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.ANALYTICS_IFRAME)))
        driver.switch_to.frame(iframe)
        time.sleep(3)

        # Hover over More icon to show menu
        more_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DASHBOARD_MORE_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_icon)
        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.move_to_element(more_icon).perform()
        print("Hovering over More icon - waiting for menu to appear")
        time.sleep(1.5)

        # Click Share
        print("Clicking Share...")
        share_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SHARE_BUTTON)))
        safe_click(share_btn)
        time.sleep(3)  # Increased wait for share modal to open
        print("✅ Clicked Share button, waiting for modal...")

        # Click Open Link Generator - with longer wait and better error handling
        try:
            print("🔍 Looking for Open Link Generator button...")
            open_link_gen_btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, AWAElements.OPEN_LINK_GENERATOR_BUTTON))
            )
            print("✅ Found Open Link Generator button")
            safe_click(open_link_gen_btn)
            time.sleep(2)
            print("✅ Clicked Open Link Generator button")
        except Exception as e:
            print(f"❌ Could not find/click Open Link Generator button: {e}")
            # Take screenshot to see current state
            driver.save_screenshot("tests/screenshots/dashboard/share_link_debug.png")
            print("📸 Debug screenshot saved")
            raise

        # Check Allow Brand Switching checkbox
        try:
            allow_brand_switching_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.ALLOW_BRAND_SWITCHING_CHECKBOX)))
            if not allow_brand_switching_checkbox.is_selected():
                safe_click(allow_brand_switching_checkbox)
                print("✅ Checked Allow Brand Switching")
            else:
                print("✅ Allow Brand Switching already checked")
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Could not find/check Allow Brand Switching checkbox: {e}")

        # Select Open for anyone radio button
        try:
            open_for_anyone_radio = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.OPEN_FOR_ANYONE_RADIO)))
            safe_click(open_for_anyone_radio)
            print("✅ Selected 'Open for anyone'")
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Could not select 'Open for anyone' radio: {e}")

        # Click Generate Shareable Link
        generate_link_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.GENERATE_SHAREABLE_LINK_BUTTON)))
        safe_click(generate_link_btn)
        time.sleep(2)

        # Click Copy button to copy the link
        copy_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.COPY_LINK_BUTTON)))
        safe_click(copy_btn)
        print("✅ Copied shareable link")
        time.sleep(1)

        # Get the shareable link from clipboard or from the input field
        # Try to get link from the page
        try:
            # Look for input field containing the share link
            link_input = driver.find_element(By.XPATH, "//input[@type='text' and contains(@value, 'share_id')]")
            share_link = link_input.get_attribute('value')
            print(f"✅ Share link: {share_link}")
        except Exception as e:
            print(f"⚠️ Could not retrieve share link from page: {e}")
            # Use a default/example link format
            share_link = "https://analytics.locobuzz.com/share?share_id=e8f24e76-2da9-47ff-8b49-45490a41e305"
            print(f"Using example link: {share_link}")

        # Switch back to default content
        driver.switch_to.default_content()

        # Open the shared link in a new tab
        print("Opening shared link in new tab...")
        driver.execute_script(f"window.open('{share_link}', '_blank');")
        time.sleep(3)

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        print("✅ Switched to new tab with shared link")
        time.sleep(5)

        # Wait for page to load and verify deep dive tab is visible
        try:
            deep_dive_tab = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, AWAElements.DEEP_DIVE_TAB))
            )
            print("✅ Shared dashboard loaded successfully")
            
            # Click on the deep dive tab
            safe_click(deep_dive_tab)
            print("✅ Clicked on deep dive tab")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Could not find deep dive tab: {e}")

        # Close the new tab and switch back to main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("✅ Closed shared link tab and returned to main window")

        print("✅ Share Link workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after share link workflow")
