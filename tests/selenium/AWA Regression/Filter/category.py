# 04DEC2025
# Filter workflow: Category & Location, Header Filter
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
    screenshots_dir = "tests/screenshots/filter"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_filter_workflow():
    test_name = "filter_workflow"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Filter workflow...")

        # Switch to iframe
        print("🔄 Switching to iframe...")
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.ANALYTICS_IFRAME)))
        driver.switch_to.frame(iframe)
        time.sleep(5)  # Increased wait time for iframe to fully load
        print("✅ Switched to iframe successfully")

        # Click Category & Location button
        print("Clicking Category & Location button...")
        try:
            # Wait for the button to be present first
            category_location_btn = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.CATEGORY_LOCATION_BUTTON)))
            print(f"✅ Found Category & Location button")
            time.sleep(1)
            # Then wait for it to be clickable
            category_location_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.CATEGORY_LOCATION_BUTTON)))
            print(f"✅ Button is clickable, attempting to click...")
            safe_click(category_location_btn)
            time.sleep(3)
            print("✅ Successfully clicked Category & Location button")
        except Exception as e:
            print(f"❌ Failed to click Category & Location button: {e}")
            raise

        # Click on zepto QA+ to expand
        print("Expanding zepto QA+ brand...")
        zepto_expand = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.BRAND_EXPAND)))
        safe_click(zepto_expand)
        time.sleep(3)  # Wait longer for expansion animation

        # Check "All" checkbox
        print("Checking All checkbox...")
        try:
            # Try the original XPath first
            all_checkbox_label = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ALL_CHECKBOX)))
            safe_click(all_checkbox_label)
        except:
            print("⚠️ Original All checkbox XPath failed, trying alternatives...")
            try:
                # Try finding by just the span text "All"
                all_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='All']")))
                safe_click(all_checkbox)
            except:
                # Last resort: find any label containing "All"
                all_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'All')]")))
                safe_click(all_checkbox)
        time.sleep(2)
        print("✅ All checkbox clicked")

        # Click Done button to close the dialog
        print("Clicking Done button...")
        try:
            # Try multiple XPath strategies for Done button
            done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Done']")))
            safe_click(done_btn)
        except:
            print("⚠️ First Done button XPath failed, trying alternative...")
            done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Done')]")))
            safe_click(done_btn)
        time.sleep(2)

        # Click Header Filter button
        print("Clicking Header Filter button...")
        header_filter_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.HEADER_FILTER_BUTTON)))
        safe_click(header_filter_btn)
        time.sleep(1)

        # Search for "category"
        print("Searching for category...")
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.FILTER_SEARCH_INPUT)))
        safe_click(search_input)
        search_input.clear()
        search_input.send_keys("category")
        time.sleep(1)

        # Click Category with arrow button
        print("Clicking Category arrow button...")
        category_arrow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.CATEGORY_ARROW_BUTTON)))
        safe_click(category_arrow_btn)
        time.sleep(1)

        # Search for "brand" in Category search
        print("Searching for brand in Category...")
        category_search_input = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.CATEGORY_SEARCH_INPUT)))
        safe_click(category_search_input)
        category_search_input.clear()
        category_search_input.send_keys("brand")
        time.sleep(1)

        # Check Include checkbox
        print("Checking Include checkbox...")
        include_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.INCLUDE_CHECKBOX)))
        if not include_checkbox.is_selected():
            safe_click(include_checkbox)
        time.sleep(1)

        # Click Apply button
        print("Clicking Apply button...")
        apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.APPLY_BUTTON)))
        safe_click(apply_btn)
        time.sleep(2)

        # Click on "Brand Mentions" text in Listening Overview
        print("Clicking Brand Mentions...")
        brand_mentions = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.BRAND_MENTIONS_TEXT)))
        safe_click(brand_mentions)
        time.sleep(2)

        print("✅ Filter workflow completed successfully")

        # Switch back to default content
        driver.switch_to.default_content()

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after filter workflow")
