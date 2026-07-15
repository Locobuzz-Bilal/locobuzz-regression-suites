# Generated on 16DEC25
# Description: create a test that logs in

import pytest
import time
import os
import allure
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locobuzz_login.CX_login import locobuzzLogin
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from config.config import TICKET_IDS
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements
from elements.manual_reg_page import ManualRegElements

TICKET_ID = TICKET_IDS["twitter-OT"]

def capture_failure_screenshot(driver, test_name):
    """Capture screenshot on test failure"""
    screenshots_dir = "tests/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
@allure.feature('Twitter Tests')
@allure.story('Generated Test - General Workflow')
def test_twitter_create_a_test():
    """
    Test Description: create a test that logs in
    
    Steps:
    1. Login to the system
    2. Select twitter brand
    3. Search for ticket
        - Perform test actions\n    - Verify results\n
    4. Verify success
    """
    test_name_var = "test_twitter_create_a_test"
    driver = None

    try:
        print("🔹 Logging in using Selenium...")
        driver = locobuzzLogin("xagent", "Locobuzz@123")
        wait = WebDriverWait(driver, 20)

        def safe_click(element):
            """Safe click with scroll into view"""
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            driver.execute_script("arguments[0].click();", element)

        # Select brand
        print(f"🔹 Selecting {category} brand...")
        select_brand = wait.until(EC.presence_of_element_located(
            (By.XPATH, LoginPageElements.SELECT_TWITTER_AUTO)
        ))
        safe_click(select_brand)

        apply_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, LoginPageElements.SUBMIT_BUTTON)
        ))
        safe_click(apply_btn)
        time.sleep(2)

        # Search for ticket
        print(f"🔹 Searching for ticket: {TICKET_ID}...")
        search_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.SEARCH_ICON)
        ))
        safe_click(search_btn)

        search_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT)
        ))
        search_input.clear()
        search_input.send_keys(TICKET_ID)
        search_input.send_keys(Keys.ENTER)
        time.sleep(3)

        # Main test logic
        print("🔹 Executing test actions...")
        # TODO: Implement specific test logic based on requirements
        # Add your test steps here
        
        time.sleep(2)
        print("✓ Test actions completed")

        print("✅ Test completed successfully")
        
    except Exception as e:
        capture_failure_screenshot(driver, test_name_var)
        print(f"❌ Test failed: {str(e)}")
        raise

    finally:
        if driver:
            driver.quit()
            print("🔹 Browser closed")
