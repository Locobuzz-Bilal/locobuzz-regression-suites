# 10DEC2025
# Schedule Report workflow: Create Monthly Scheduled Report with Preview
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
from utils.credentials import get_sa_creds


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/schedule_report"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_schedule_report():
    test_name = "schedule_report"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Starting Schedule Report workflow...")

        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.OVERVIEW_TAB))))

        # Switch to iframe
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.ANALYTICS_IFRAME)))
        driver.switch_to.frame(iframe)
        time.sleep(3)

        # Wait for iframe content to fully load and re-locate More icon
        print("Hovering over More icon for edit - waiting for menu to appear")
        more_icon = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DASHBOARD_MORE_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_icon)
        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.move_to_element(more_icon).perform()
        time.sleep(1.5)

        # Click Schedule Report
        print("Clicking Schedule Report...")
        schedule_report_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SCHEDULE_REPORT_BUTTON)))
        safe_click(schedule_report_btn)
        time.sleep(2)

        # Click Next button
        print("Clicking Next...")
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SCHEDULE_REPORT_NEXT_BUTTON)))
        safe_click(next_btn)
        time.sleep(1)

        # Select Schedule Report radio button
        print("Selecting Schedule Report option...")
        schedule_radio = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SCHEDULE_REPORT_RADIO)))
        safe_click(schedule_radio)
        time.sleep(1)

        # Select Monthly from frequency dropdown
        print("Selecting Monthly frequency...")
        # Click on frequency text to focus, then use ActionChains to send keys
        frequency_div = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.FREQUENCY_DIV)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", frequency_div)
        time.sleep(0.5)
        frequency_div.click()  # Click the text to focus
        time.sleep(0.5)
        
        # Use ActionChains to send DOWN arrow key to open dropdown
        actions = ActionChains(driver)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(2)
        
        # Click Monthly option
        monthly_option = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.FREQUENCY_MONTHLY_OPTION)))
        safe_click(monthly_option)
        time.sleep(1)

        # Select "Last month" from period dropdown
        print("Selecting Last month period...")
        period_selector = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.PERIOD_SELECTOR)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", period_selector)
        time.sleep(0.5)
        period_selector.click()
        time.sleep(0.5)
        
        # Use ActionChains to send DOWN arrow key to open dropdown
        actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(2)
        
        last_month_option = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.LAST_MONTH_OPTION)))
        safe_click(last_month_option)
        time.sleep(1)

        # Select "2nd of every month" from day dropdown
        print("Selecting 2nd of every month...")
        day_selector = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.DAY_SELECTOR)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", day_selector)
        time.sleep(0.5)
        day_selector.click()
        time.sleep(0.5)
        
        # Use ActionChains to send DOWN arrow key to open dropdown
        actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(2)
        
        second_day_option = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SECOND_DAY_OPTION)))
        safe_click(second_day_option)
        time.sleep(1)

        # Select time (12:30 AM)
        print("Selecting time 12:30 AM...")
        time_selector = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.TIME_SELECTOR)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", time_selector)
        time.sleep(0.5)
        time_selector.click()
        time.sleep(0.5)
        
        # Type the time in the search field
        actions.send_keys("12:30").perform()
        time.sleep(1)
        
        # Press ENTER to select the first matching option
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(1)

        # Click Next
        print("Clicking Next...")
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SCHEDULE_REPORT_NEXT_BUTTON)))
        safe_click(next_btn)
        time.sleep(2)

        # Click Preview button
        print("Clicking Preview...")
        preview_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.PREVIEW_BUTTON)))
        safe_click(preview_btn)
        time.sleep(3)

        # Click on "Listening Overview" text in the preview
        print("Verifying preview content - Listening Overview...")
        listening_overview = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.LISTENING_OVERVIEW_TEXT)))
        safe_click(listening_overview)
        time.sleep(1)

        # Click Schedule Report button
        print("Clicking Schedule Report button...")
        schedule_report_final = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SCHEDULE_REPORT_FINAL_BUTTON)))
        safe_click(schedule_report_final)
        time.sleep(3)

        # Verify success message
        print("Verifying success message...")
        success_msg = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.REPORT_SCHEDULED_SUCCESS)))
        if success_msg.is_displayed():
            print(f"✅ {success_msg.text}")
        time.sleep(2)

        # Switch back to default content
        driver.switch_to.default_content()

        print("✅ Schedule Report workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after schedule report workflow")
