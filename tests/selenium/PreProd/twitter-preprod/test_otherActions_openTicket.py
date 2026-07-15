# running 20OCT25
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locobuzz_login.CX_login import locobuzzLogin
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from config.config import TICKET_IDS
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements
TICKET_ID = TICKET_IDS["twitter"]
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
        driver = locobuzzLoginPreProd("juw_agent", "Buzz@1234")
        wait = WebDriverWait(driver, 20)

        def safe_click(element):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            driver.execute_script("arguments[0].click();", element)

        # ✅ Select All & Submit
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
        safe_click(select_all)

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

        moreTab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MORE_OPTIONS_ICON)))
        safe_click(moreTab)

        # ✅ Ticket Actions
        closed_tickets = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CLOSED_TICKETS_TAB)))
        safe_click(closed_tickets)
        time.sleep(3)  # Wait for closed tickets to load

        account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
        time.sleep(1)
        safe_click(account_box)
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
        
        # Now continue with actions on the reopened ticket
        # account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        # driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
        # time.sleep(1)
        # safe_click(account_box)
        # time.sleep(2)
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
            ((By.XPATH, ReplyPanelPageElements.SPECIFIC_IMAGE))))
        time.sleep(2)
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_BUTTON_CLOSE))))
        direct_close = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DIRECT_CLOSE_BUTTON)))
        safe_click(direct_close)
        time.sleep(3)

        print("✅ Ticket closed successfully!")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")

    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed and resources cleaned up.")