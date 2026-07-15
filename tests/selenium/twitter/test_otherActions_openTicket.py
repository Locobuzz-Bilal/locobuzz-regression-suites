# running 20OCT25
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
from utils.credentials import get_twitter_ot_creds
TICKET_ID = TICKET_IDS["twitter-OT"]
from selenium.common.exceptions import TimeoutException

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_otherActions_openTicket():
    test_name = "test_otherActions_openTicket"
    driver = None

    try:
        print("🔹 Logging in using Selenium...")
        user, pwd = get_twitter_ot_creds()
        driver = locobuzzLogin(user, pwd)
        wait = WebDriverWait(driver, 20)

        def safe_click(element):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            driver.execute_script("arguments[0].click();", element)

        # ✅ Select All & Submit
        select_Twitter_Auto = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_TWITTER_AUTO)))
        safe_click(select_Twitter_Auto)

        apply_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
        safe_click(apply_btn)

        # ✅ Search Ticket
        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)

        search_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)
        ))
        search_field.clear()
        search_field.send_keys(TICKET_ID)
        safe_click(search_btn)
        safe_click(search_btn)
        print(f"🔍 Searched ticket: {TICKET_ID}")

        time.sleep(3)

        with allure.step("Navigate to Closed Tickets"):
            # Check if CT_TAB_ALTERNATE is available
            ct_alternate_elements = driver.find_elements(By.XPATH, ReplyPanelPageElements.CT_TAB_ALTERNATE)
            if ct_alternate_elements:
                # If CT_TAB_ALTERNATE exists, click it directly
                safe_click(ct_alternate_elements[0])
                print("\u2705 Clicked CT_TAB_ALTERNATE")
            else:
                # Otherwise, click More and then Closed Tickets
                moreTab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MORE_OPTIONS_ICON)))
                safe_click(moreTab)
                closed_tickets = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CLOSED_TICKETS_TAB)))
                safe_click(closed_tickets)
                print("\u2705 Clicked More → Closed Tickets")
            
            # Wait for the ticket card to load in Closed Tickets tab
            time.sleep(3)

        # Re-find account_box to avoid stale element
        account_box = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
        time.sleep(1)
        # Re-find after scroll to avoid stale element
        account_box = driver.find_element(By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)
        driver.execute_script("arguments[0].click();", account_box)
        time.sleep(2)

        overview_tab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OVERVIEW_TAB)))
        safe_click(overview_tab)
        time.sleep(2)

        ticket_status = wait.until(EC.presence_of_element_located
                                   ((By.XPATH, ReplyPanelPageElements.TICKET_STATUS_DROPDOWN)))
        safe_click(ticket_status)
        time.sleep(2)

        open_option = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.OPEN_STATUS_OPTION)))
        safe_click(open_option)
        time.sleep(2)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        
        # Hard refresh to go back to Open tab (default view)
        driver.refresh()
        time.sleep(3)

        # ✅ Search Ticket again after refresh
        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)

        search_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)
        ))
        search_field.clear()
        search_field.send_keys(TICKET_ID)
        safe_click(search_btn)
        safe_click(search_btn)
        print(f"🔍 Searched ticket: {TICKET_ID}")

        time.sleep(3)
        
        # Now continue with actions on the reopened ticket

        print("\n📝 Step 3: Changing ticket priority to Medium...")
        priority_low = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.PRIORITY_LOW)))
        safe_click(priority_low)
        time.sleep(1)

        priority_medium = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.PRIORITY_MEDIUM)))
        safe_click(priority_medium)
        time.sleep(2)
        print("✅ Priority changed to Medium")
        
        # Verify Priority Change in Timeline
        account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        safe_click(account_box)
        time.sleep(1)
        
        next_arrow = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.NEXT_ARROW)))
        safe_click(next_arrow)
        safe_click(next_arrow)
        time.sleep(1)
        
        timeline_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.TIMELINE_TAB)))
        safe_click(timeline_tab)
        time.sleep(2)
        
        print("\n" + "="*80, flush=True)
        print("🔍 VERIFYING PRIORITY CHANGE IN TIMELINE", flush=True)
        print("="*80, flush=True)
        
        priority_timeline_xpath = ("//span[contains(@class, 'post-timeline__label') "
                                  "and contains(., 'Moved to priority by')]")
        
        priority_timeline = wait.until(EC.presence_of_element_located((By.XPATH, priority_timeline_xpath)))
        priority_text = priority_timeline.text
        
        print(f"\n✅ Priority timeline element found!", flush=True)
        print(f"📝 Timeline text: {priority_text}", flush=True)
        print("="*80, flush=True)
        
        assert "Moved to priority by" in priority_text, "'Moved to priority by' not found in timeline"
        print("✓ 'Moved to priority by' found", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Close account box
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        
        more_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MORE_BUTTON)))
        safe_click(more_btn)

        mark_influencer = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MARK_INFLUENCER_BUTTON)))
        safe_click(mark_influencer)

        influencer_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.INFLUENCER_CATEGORY_DROPDOWN)))
        safe_click(influencer_dropdown)

        anchor_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ANCHOR_OPTION)))
        safe_click(anchor_option)

        mark_influencer_confirm = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MARK_INFLUENCER_CONFIRM)))
        safe_click(mark_influencer_confirm)

        print("✅ Mark Influencer Done")

        # 🟢 Continue Additional Actions
        others_section = wait.until(EC.presence_of_element_located(
            (By.XPATH, ReplyPanelPageElements.OTHERS_SECTION)))
        safe_click(others_section)

        # Example selecting mention options
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_JUW_TESTING_1))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_TESTING_2))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_TESTING_3))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_NEUTRAL))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_SUBMIT))))
        print("✅ Mention categories selected and submitted")
        time.sleep(2)
        
        # Verify Mention Category Change in Timeline
        account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        safe_click(account_box)
        time.sleep(1)
        
        next_arrow = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.NEXT_ARROW)))
        safe_click(next_arrow)
        safe_click(next_arrow)
        time.sleep(1)
        
        timeline_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.TIMELINE_TAB)))
        safe_click(timeline_tab)
        time.sleep(2)
        
        print("\n" + "="*80, flush=True)
        print("🔍 VERIFYING MENTION CATEGORY CHANGE IN TIMELINE", flush=True)
        print("="*80, flush=True)
        
        category_timeline_xpath = ("//span[contains(@class, 'post-timeline__label') "
                                  "and contains(., 'has modified mention category')]")
        
        category_timeline = wait.until(EC.presence_of_element_located((By.XPATH, category_timeline_xpath)))
        category_text = category_timeline.text
        
        print(f"\n✅ Category timeline element found!", flush=True)
        print(f"📝 Timeline text: {category_text}", flush=True)
        print("="*80, flush=True)
        
        assert "has modified mention category" in category_text, "'has modified mention category' not found in timeline"
        print("✓ 'has modified mention category' found", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Close account box
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

        original_window = driver.current_window_handle
        
        # Open link in new tab
        open_link = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OPEN_LINK_BUTTON)))
        driver.execute_script("arguments[0].click();", open_link)
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.window(driver.window_handles[-1])
        print("✅ Opened new link")
        # Switch back to the original tab
        driver.switch_to.window(original_window)
        print("🔙 Returned to the first tab")

        # Send Email
        send_email = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEND_EMAIL_BUTTON)))
        safe_click(send_email)
        time.sleep(2)
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_INPUT_FIELD)))
        email_field.send_keys("juw@email.com")
        time.sleep(2)
        email_field.send_keys(u'\ue007')  # press Enter
        time.sleep(2)
        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_SEND_BUTTON)))
        safe_click(send_btn)
        print("✅ Email sent successfully")
        time.sleep(2)

        # Add Note
        open_details = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OPEN_DETAILS_BUTTON)))
        safe_click(open_details)
        time.sleep(2)

        
        discard_elements = driver.find_elements(By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)
        if discard_elements:
         safe_click(discard_elements[0])
        time.sleep(1)
    
        submit_elements = driver.find_elements(By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)
        if submit_elements:
             safe_click(submit_elements[0])
        else:
         print("Discard button not found, skipping...")
        

        # discard = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
        # safe_click(discard)
        # time.sleep(1)
        # submitBtn2 = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
        # safe_click(submitBtn2)
        # time.sleep(1)
        
        add_note = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ADD_NOTE_BUTTON)))
        safe_click(add_note)
        note_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ADD_NOTE_TEXTAREA)))
        note_box.send_keys("hello testing")

        # attach_media = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_MEDIA_BUTTON)))
        # safe_click(attach_media)
        # first_image = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.FIRST_IMAGE)))
        # safe_click(first_image)
        # attach_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_BUTTON_MEDIA)))
        # safe_click(attach_btn)

        save_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SAVE_BUTTON)))
        safe_click(save_btn)
        print("✅ Note added successfully")

        # Go Back
        back_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.BACK_TO_TICKET_LIST)))
        safe_click(back_btn)

        # Personal Details Update
        account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        safe_click(account_box)
        personal_details = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.PERSONAL_DETAILS_TAB)))
        safe_click(personal_details)

        name_box = wait.until(EC.presence_of_element_located
                              ((By.XPATH, ReplyPanelPageElements.NAME_INPUT_FIELD)))
        name_box.clear()
        name_box.send_keys("juwairia")
        update_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.UPDATE_BUTTON)))
        safe_click(update_btn)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()   
        time.sleep(1)
        print("✅ Personal details updated")

        # Close with Note
        dropdown_close = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DIRECT_CLOSE_DROPDOWN)))
        safe_click(dropdown_close)
        close_with_note = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CLOSE_WITH_NOTE_OPTION)))
        safe_click(close_with_note)
        note_area = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CLOSE_NOTE_TEXTAREA)))
        note_area.send_keys("direct closing with note")

        attach_media = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_MEDIA_CLOSE)))
        safe_click(attach_media)
        safe_click(wait.until(EC.presence_of_element_located
            ((By.XPATH, ReplyPanelPageElements.X_IMAGE))))
        time.sleep(2)
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_BUTTON_CLOSE))))
        direct_close = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DIRECT_CLOSE_BUTTON)))
        safe_click(direct_close)
        time.sleep(3)

        print("✅ Ticket closed successfully!")
        
        # Verify Direct Close with Attachment in Timeline
        # Navigate to Closed Tickets tab
        with allure.step("Navigate to Closed Tickets for Timeline Verification"):
            ct_alternate_elements = driver.find_elements(By.XPATH, ReplyPanelPageElements.CT_TAB_ALTERNATE)
            if ct_alternate_elements:
                safe_click(ct_alternate_elements[0])
                print("✅ Clicked CT_TAB_ALTERNATE")
            else:
                moreTab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MORE_OPTIONS_ICON)))
                safe_click(moreTab)
                closed_tickets = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CLOSED_TICKETS_TAB)))
                safe_click(closed_tickets)
                print("✅ Clicked More → Closed Tickets")
            time.sleep(3)
        
        # Search for the ticket
        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
        search_field.clear()
        search_field.send_keys(TICKET_ID)
        safe_click(search_btn)
        safe_click(search_btn)
        print(f"🔍 Searched ticket in Closed: {TICKET_ID}")
        time.sleep(3)
        
        # Open account box and navigate to timeline
        account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        safe_click(account_box)
        time.sleep(1)
        
        next_arrow = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.NEXT_ARROW)))
        safe_click(next_arrow)
        safe_click(next_arrow)
        time.sleep(1)
        
        timeline_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.TIMELINE_TAB)))
        safe_click(timeline_tab)
        time.sleep(2)
        
        print("\n" + "="*80, flush=True)
        print("🔍 VERIFYING DIRECT CLOSE WITH ATTACHMENT IN TIMELINE", flush=True)
        print("="*80, flush=True)
        
        close_timeline_xpath = ("//span[contains(@class, 'post-timeline__label') "
                               "and .//a[normalize-space(.)='this mention'] "
                               "and .//a[normalize-space(.)='this note with attachment'] "
                               "and contains(., 'has directly closed')]")
        
        close_timeline = wait.until(EC.presence_of_element_located((By.XPATH, close_timeline_xpath)))
        close_text = close_timeline.text
        
        print(f"\n✅ Direct close timeline element found!", flush=True)
        print(f"📝 Timeline text: {close_text}", flush=True)
        print("="*80, flush=True)
        
        assert "this mention" in close_text, "'this mention' not found in timeline"
        print("✓ 'this mention' found", flush=True)
        
        assert "this note with attachment" in close_text, "'this note with attachment' not found in timeline"
        print("✓ 'this note with attachment' found", flush=True)
        
        assert "has directly closed" in close_text, "'has directly closed' not found in timeline"
        print("✓ 'has directly closed' found", flush=True)
        print("="*80 + "\n", flush=True)

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")

    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed and resources cleaned up.")