# 05DEC2025
# Twitter channel widget workflow
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locobuzz_login.CX_login import locobuzzLogin
from elements.awa_regression_page import AWAElements
from utils.credentials import get_sa_creds


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/widgets"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_twitter_widgets():
    test_name = "twitter_widgets"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Twitter widgets workflow...")

        # Switch to iframe
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.ANALYTICS_IFRAME)))
        driver.switch_to.frame(iframe)
        time.sleep(3)

        # Scroll down to load all channel elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Wait for page to stabilize
        time.sleep(3)
        
        # Click on Twitter channel
        print("Clicking Twitter channel...")
        
        # First check if element exists
        try:
            all_twitter_spans = driver.find_elements(By.XPATH, "//span[text()='Twitter']")
            print(f"Found {len(all_twitter_spans)} Twitter spans")
        except:
            print("Could not find any Twitter spans")
        
        # Wait for the element with increased timeout
        twitter_wait = WebDriverWait(driver, 30)
        twitter_channel = twitter_wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.TWITTER_CHANNEL)))
        
        # Scroll to element
        driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'smooth'});", twitter_channel)
        time.sleep(2)
        
        # Wait for it to be clickable
        twitter_channel = twitter_wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.TWITTER_CHANNEL)))
        
        # Try multiple clicks to ensure element is clicked
        safe_click(twitter_channel)
        time.sleep(1)
        safe_click(twitter_channel)
        time.sleep(3)

        # Click on "Channel (Twitter)" widget
        print("Clicking Channel (Twitter) widget...")
        channel_twitter = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.CHANNEL_TWITTER_WIDGET)))
        safe_click(channel_twitter)
        time.sleep(2)

        # Click Mentions button
        print("Clicking Mentions button...")
        mentions_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.MENTIONS_BUTTON)))
        safe_click(mentions_btn)
        time.sleep(2)

        # Click Word Cloud button
        print("Clicking Word Cloud button...")
        word_cloud_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.WORD_CLOUD_BUTTON)))
        safe_click(word_cloud_btn)
        time.sleep(2)

        # Click Category button
        print("Clicking Category button...")
        category_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.CATEGORY_BUTTON)))
        safe_click(category_btn)
        time.sleep(2)

        # Click Influencers button
        print("Clicking Influencers button...")
        influencers_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.INFLUENCERS_BUTTON)))
        safe_click(influencers_btn)
        time.sleep(2)

        # Click Source of Post button
        print("Clicking Source of Post button...")
        source_post_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SOURCE_POST_BUTTON)))
        safe_click(source_post_btn)
        time.sleep(2)

        # Click Location Profiles button
        print("Clicking Location Profiles button...")
        location_profiles_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.LOCATION_PROFILES_BUTTON)))
        safe_click(location_profiles_btn)
        time.sleep(2)

        # Click Mentions button again
        print("Clicking Mentions button again...")
        mentions_btn_final = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.MENTIONS_BUTTON)))
        safe_click(mentions_btn_final)
        time.sleep(2)

        print("✅ Twitter widgets workflow completed successfully")

        # Switch back to default content
        driver.switch_to.default_content()

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after Twitter widgets workflow")
