# 08DEC2025
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
def test_category_filter_workflow():
    """
    Test Description: Test Category & Location filter workflow
    
    Steps:
    1. Login to LocoBuzz
    2. Switch to analytics iframe
    3. Click Category & Location button
    4. Expand zepto QA+ brand
    5. Select All checkbox
    6. Click Done button
    7. Click Header Filter button
    """
    test_name = "category_filter_workflow"
    driver = None
    
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 30)

        def safe_click(el):
            """Safe click using JavaScript to avoid interception issues"""
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Filter workflow...")

        # Switch to iframe
        print("🔄 Switching to iframe...")
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@name='analyticsFrame']")))
        driver.switch_to.frame(iframe)
        time.sleep(5)
        print("✅ Switched to iframe successfully")

        # Click Category & Location button
        print("Clicking Category & Location button...")
        category_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Category & Location')]")))
        safe_click(category_btn)
        time.sleep(2)
        print("✅ Clicked Category & Location button")

        # Expand zepto QA+ brand
        print("Expanding zepto QA+ brand...")
        zepto_expand = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='zepto QA+']/following-sibling::div")))
        safe_click(zepto_expand)
        time.sleep(2)
        print("✅ Expanded zepto QA+ brand")

        # Click All checkbox
        print("Clicking All checkbox...")
        all_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='tooltip']//span[text()='All']")))
        safe_click(all_checkbox)
        time.sleep(1)
        print("✅ Clicked All checkbox")

        # Click Done button
        print("Clicking Done button...")
        done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Done')]")))
        safe_click(done_btn)
        time.sleep(2)
        print("✅ Clicked Done button")

        # Click Header Filter button
        print("Clicking Header Filter button...")
        header_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Header Filter') or .//img[@alt='Header Filter']]")))
        safe_click(header_filter)
        time.sleep(2)
        print("✅ Clicked Header Filter button")

        print("✅ Category filter workflow completed successfully")

        # Switch back to default content
        driver.switch_to.default_content()

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
        
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely")


if __name__ == "__main__":
    # For manual testing
    test_category_filter_workflow()
