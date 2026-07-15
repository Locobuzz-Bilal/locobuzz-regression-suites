#20OCT25
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from utils.credentials import get_twitter_creds
TICKET_ID = TICKET_IDS["twitter"]
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/reply_and_close"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_reply_and_close():
    test_name = "reply_and_close"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        user, pwd = get_twitter_creds()
        driver = locobuzzLogin(user, pwd)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Reply & Close actions...")

        # Select all & Submit
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
        safe_click(select_all)
        submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
        safe_click(submit_btn)
        time.sleep(2)
        pendingTab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.PENDING_TAB)))
        safe_click(pendingTab)
        safe_click(pendingTab)
        time.sleep(2)
        # Search Ticket
        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)
        search_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)
        ))
        search_field.clear()
        search_field.send_keys(TICKET_ID)
        safe_click(search_btn)
        time.sleep(3)


        # Click Reply
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_BUTTON))))
        # safe_click(wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(., '{TICKET_ID}')]//span[normalize-space(text())='Reply']"))))
        time.sleep(2)
        discard_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
        safe_click(discard_btn)
        submit_btn2 = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
        safe_click(submit_btn2)
        time.sleep(2)

        dismiss = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISMISS)))
        safe_click(dismiss)
        time.sleep(2)

        # Reply Type
        reply_type = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.REPLY_TYPE_DROPDOWN)
        ))
        safe_click(reply_type)
        reply_close_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_AND_CLOSE_OPTION)))
        safe_click(reply_close_option)

        # Write reply & Send
        print("✍️ Writing reply message...")
        reply_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_INPUT_BOX)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", reply_box)
        time.sleep(1)
        reply_box.click()
        reply_box.clear()
        reply_box.send_keys("Closing ticket by Selenium1")
        time.sleep(2)
        print("✅ Reply message written")
        
        print("📤 Clicking Send button...")
        try:
            send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
            safe_click(send_btn)
            print("✅ Send button clicked")
        except:
            print("⚠️ First attempt failed, trying alternate send button...")
            send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button//span[text()=' Send ']")))
            safe_click(send_btn)
            print("✅ Send button clicked (alternate)")
        time.sleep(3)

        # Navigate to Closed tab
        print("🔹 Navigating to Closed tab...")
        try:
            # Try first XPath
            closed_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CT_TAB_ALTERNATE)))
            safe_click(closed_tab)
            print("✅ Clicked Closed Tickets tab (first XPath)")
        except:
            # Try alternate XPath
            print("⚠️ First XPath failed, trying alternate...")
            closed_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CLOSED_TICKETS_TAB)))
            safe_click(closed_tab)
            print("✅ Clicked Closed Tickets tab (alternate XPath)")
        time.sleep(2)

        # Search for the ticket in Closed tab
        print("🔍 Searching for ticket in Closed tab...")
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)

        search_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
        search_field.clear()
        search_field.send_keys(TICKET_ID)
        safe_click(search_btn)
        time.sleep(2)

        # Open ticket details
        print("🔹 Opening ticket details...")
        from tests.selenium.linkedin.test_otherActions_closedTicket import click_with_retry
        
        account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
        time.sleep(1)
        click_with_retry(wait, (By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON))
        time.sleep(1)

        # Navigate to Timeline tab
        print("🔹 Navigating to Timeline tab...")
        next_arrow = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.NEXT_ARROW)))
        safe_click(next_arrow)
        safe_click(next_arrow)
        time.sleep(1)
        
        timeline_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.TIMELINE_TAB)))
        safe_click(timeline_tab)
        time.sleep(2)

        # Verify Timeline Message
        print("\n" + "="*80, flush=True)
        print("🔍 VERIFYING TIMELINE MESSAGE", flush=True)
        print("="*80, flush=True)
        
        timeline_text_xpath = ("//span[contains(@class, 'post-timeline__label') "
                              "and .//span[normalize-space(.)='Juwairia Agent'] "
                              "and .//a[normalize-space(.)='this mention'] "
                              "and contains(., 'has replied on') "
                              "and contains(., 'and closed the ticket')]")
        
        timeline_element = wait.until(EC.presence_of_element_located((By.XPATH, timeline_text_xpath)))
        timeline_text = timeline_element.text
        
        print(f"\n✅ Timeline element found!", flush=True)
        print(f"📝 Timeline text: {timeline_text}", flush=True)
        print("="*80, flush=True)
        
        # Verify the text contains expected elements
        assert "Juwairia Agent" in timeline_text, "Juwairia Agent not found in timeline"
        print("✓ 'Juwairia Agent' found", flush=True)
        
        assert "has replied on" in timeline_text, "'has replied on' not found in timeline"
        print("✓ 'has replied on' found", flush=True)
        
        assert "and closed the ticket" in timeline_text, "'and closed the ticket' not found in timeline"
        print("✓ 'and closed the ticket' found", flush=True)
        
        print("\n✅ TIMELINE VERIFICATION SUCCESSFUL!", flush=True)
        print("="*80 + "\n", flush=True)

        print("✅ Reply & Close test completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after reply & close")