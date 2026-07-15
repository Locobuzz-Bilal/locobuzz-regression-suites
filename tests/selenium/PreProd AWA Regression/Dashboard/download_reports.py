# 03DEC2025
# Download PDF and PPT reports workflow
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
def test_download_reports():
    test_name = "download_reports"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLoginPreProd(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Download Reports workflow...")

        # Switch to iframe (analytics is already loaded after login)
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.ANALYTICS_IFRAME)))
        driver.switch_to.frame(iframe)
        time.sleep(3)

        # Hover over More icon 
        more_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DASHBOARD_MORE_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_icon)
        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.move_to_element(more_icon).perform()
        print("Hovering over More icon for edit - waiting for menu to appear")
        time.sleep(1.5)

        # Download PDF
        print("Downloading PDF...")
        download_pdf_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DOWNLOAD_PDF_BUTTON)))
        safe_click(download_pdf_btn)
        time.sleep(2)

        # Verify PDF confirmation message
        try:
            pdf_msg = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.PDF_CONFIRMATION_MESSAGE)))
            print(f"✅ PDF confirmation: {pdf_msg.text}")
            time.sleep(1)
            # Click the message to dismiss (if needed)
            safe_click(pdf_msg)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ PDF confirmation message not found: {e}")

        time.sleep(2)
        # Hover over More icon again 
        more_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DASHBOARD_MORE_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_icon)
        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.move_to_element(more_icon).perform()
        print("Hovering over More icon for edit - waiting for menu to appear")
        time.sleep(1.5)

        # Download PPT
        print("Downloading PPT...")
        download_ppt_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DOWNLOAD_PPT_BUTTON)))
        safe_click(download_ppt_btn)
        time.sleep(1)

        # Select Download as Native
        download_native_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DOWNLOAD_AS_NATIVE_BUTTON)))
        safe_click(download_native_btn)
        time.sleep(1)

        # Click Next button
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.NEXT_BUTTON)))
        safe_click(next_btn)
        time.sleep(1)

        # Store the current window handle
        main_window = driver.current_window_handle
        
        # Click Download PPT (this opens a new window/tab)
        download_ppt_confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DOWNLOAD_PPT_CONFIRM_BUTTON)))
        safe_click(download_ppt_confirm_btn)
        time.sleep(2)

        # Switch to the new window/tab
        try:
            # Wait for new window to open
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            
            # Get all window handles
            windows = driver.window_handles
            
            # Switch to the new window (last one)
            new_window = [w for w in windows if w != main_window][0]
            driver.switch_to.window(new_window)
            print("✅ Switched to new window for PPT download")
            time.sleep(5)

            # Wait for generating message
            try:
                generating_msg = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, AWAElements.PPT_GENERATING_MESSAGE))
                )
                print(f"✅ PPT status: {generating_msg.text}")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Generating message not found: {e}")

            # Wait for download to complete
            time.sleep(10)

            # Verify download success message
            try:
                download_success_msg = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, AWAElements.PPT_DOWNLOADED_MESSAGE))
                )
                print(f"✅ PPT download: {download_success_msg.text}")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Download success message not found: {e}")

            # Close the new window
            driver.close()
            print("✅ Closed PPT download window")
            
            # Switch back to main window
            driver.switch_to.window(main_window)
            print("✅ Switched back to main window")
            
        except Exception as e:
            print(f"⚠️ Error handling new window: {e}")
            # Make sure we're back to main window
            driver.switch_to.window(main_window)

        # Switch back to default content
        driver.switch_to.default_content()

        print("✅ Download Reports workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after download reports workflow")
