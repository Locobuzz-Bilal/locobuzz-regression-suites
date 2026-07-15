"""
1. Retag Category - Twitter
2. Direct Close - Twitter
3. Put on Hold - Facebook
4. Reopen - Twitter
5. Escalate - Instagram
6. Reply & Close - Facebook
7 . Assign - Twitter

Uses juw_agent account for all actions.
twitter: bilaltest1cx, pragyaantest
facebook: abdul.a, praveen.singa
instagram: kc.sumo, asishlocouser
"""
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from elements.login_page import LoginPageElements
from elements.bulk_actions_page import BulkActionsPageElements
import allure
from elements.reply_panel_page import ReplyPanelPageElements
from utils.credentials import get_twitter_creds

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/bulk_actions"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_bulk_actions():
    """Test bulk actions: retag, assign, hold, escalate, reply & close, reopen, direct close"""
    test_name = "test_bulk_actions"
    driver = None

    try:
        print("🔹 Logging in using Selenium (PreProd)...")
        username, password = get_twitter_creds()
        driver = locobuzzLoginPreProd(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(element):
            """Scroll element into view and click using JavaScript"""
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", element)

        def wait_and_click(xpath, timeout=20):
            """Wait for element and click safely"""
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            safe_click(element)
            return element

        # ✅ Step 1: Select All Brands & Submit
        print("📝 Step 1: Selecting all brands...")
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
        safe_click(select_all)
        time.sleep(1)

        submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
        safe_click(submit_btn)
        time.sleep(3)
        print("✅ Brands selected and submitted")

        time.sleep(5)

        with allure.step("Add Step - Retag Category"):
            
            # Scroll 
            try:
                ticket_1 = driver.find_element(By.XPATH, BulkActionsPageElements.BILALTEST1CX)
                driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", ticket_1)
                time.sleep(0.3)
               
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(0.5)
            except:
                pass

        # ✅ Step 2: Retag Category (Bulk Action)
        print("\n📝 Step 2: Retag Category - Selecting 2 tickets...")
        checkbox1 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.BILALTEST1CX)))
        if not checkbox1.is_selected():
            safe_click(checkbox1)
        
        checkbox2 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.PRAGYAANTEST)))
        if not checkbox2.is_selected():
            safe_click(checkbox2)
        time.sleep(1)

        # Click Retag Category button
        retag_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.RETAG_CATEGORY_BUTTON)))
        safe_click(retag_btn)
        time.sleep(1)

        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_JUW_TESTING_1))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_TESTING_2))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_TESTING_3))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_NEUTRAL))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_SUBMIT))))
        print("✅ Mention categories selected and submitted")

        #Step 3: Direct Close (Bulk Action)
       
        # Click Direct Close
        direct_close_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.DIRECT_CLOSE_BUTTON)))
        safe_click(direct_close_btn)
        time.sleep(1)

        # Confirm
        continue_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.CONTINUE_BUTTON)))
        safe_click(continue_btn)
        time.sleep(2)

        driver.refresh()
        time.sleep(10)

        print("✅ Direct Close completed")

        with allure.step("Add Step - ON HOLD"):
            
            # Scroll 
            try:
                ticket_3 = driver.find_element(By.XPATH, BulkActionsPageElements. ABDUL_A)
                driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", ticket_3)
                time.sleep(0.3)
                # Scroll down further to reveal Send Alert
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(0.5)
            except:
                pass

        # ✅ Step 4: Put on Hold (Bulk Action)
        print("\n📝 Step 4: Putting tickets on hold...")
        checkbox14 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.ABDUL_A)))
        if not checkbox14.is_selected():
            safe_click(checkbox14)
        
        with allure.step("Add Step - ON HOLD"):

            # Scroll 
            try:
                ticket_4 = driver.find_element(By.XPATH, BulkActionsPageElements.PRAVEEN_SINGA)
                driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", ticket_4)
                time.sleep(0.3)
                # Scroll down further to reveal Send Alert
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(0.5)
            except:
                pass

        checkbox15 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.PRAVEEN_SINGA)))
        if not checkbox15.is_selected():
            safe_click(checkbox15)
        time.sleep(1)

        # Click Put on hold
        hold_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.PUT_ON_HOLD_BUTTON)))
        safe_click(hold_btn)
        time.sleep(1)

        # Add note
        note_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, BulkActionsPageElements.NOTE_FIELD)
        ))
        note_field.clear()
        note_field.send_keys("on hold")
        time.sleep(0.5)

        # Save
        save_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.SAVE_BUTTON)))
        safe_click(save_btn)
        time.sleep(2)
        print("✅ Put on Hold completed")

        driver.refresh()
        time.sleep(10)

         # ✅ Step 5: Reopen Closed Tickets
        print("\n📝 Step 5: Reopening closed tickets...")
        with allure.step("Navigate to Closed Tickets"):
            # Check if CLOSED TICKETS TAB is available
            ct_alternate_elements = driver.find_elements(By.XPATH, BulkActionsPageElements.CLOSED_TICKETS_TAB)
            if ct_alternate_elements:
                # If CLOSED_TICKETS_TAB exists, click it directly
                safe_click(ct_alternate_elements[0])
                print("\u2705 Clicked Closed Tickets")
            else:
                # Otherwise, click More and then Closed Tickets
                moreTab = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.MORE_BUTTON)))
                safe_click(moreTab)
                closed_tickets = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.CLOSED_TICKETS_MENU)))
                safe_click(closed_tickets)
                print("\u2705 Clicked More → Closed Tickets")
            time.sleep(3)

        time.sleep(15)

        checkbox39 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.PRAGYAANTEST)))
        if not checkbox39.is_selected():
            safe_click(checkbox39)
        
        checkbox40 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.BILALTEST1CX)))
        if not checkbox40.is_selected():
            safe_click(checkbox40)
        time.sleep(1)

        # Click Reopen
        reopen_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.REOPEN_BUTTON)))
        safe_click(reopen_btn)
        time.sleep(1)

        # Enter note
        reopen_note = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.REOPEN_NOTE_FIELD)))
        reopen_note.clear()
        reopen_note.send_keys("reopen")
        time.sleep(0.5)

        # Save
        save_reopen = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.SAVE_REOPEN_BUTTON)))
        safe_click(save_reopen)
        time.sleep(2)
        print("✅ Reopen completed")

        driver.refresh()
        time.sleep(15)

        with allure.step("Add Step - ESCALATE"):
        #Scroll 
            try:
                ticket_5 = driver.find_element(By.XPATH, BulkActionsPageElements.KC_SUMO)
                driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", ticket_5)
                time.sleep(0.3)
            # Scroll down further to reveal Send Alert
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(0.5)
            except:
                pass

        # ✅ Step 6: Escalate (Bulk Action)
        print("\n📝 Step 6: Escalating tickets...")
       
        checkbox10 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.KC_SUMO)))
        if not checkbox10.is_selected():
            safe_click(checkbox10)
        
        checkbox11 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.ASISHLOCOUSER)))
        if not checkbox11.is_selected():
            safe_click(checkbox11)
        time.sleep(1)

        # Click Escalate
        escalate_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.ESCALATE_BUTTON)))
        safe_click(escalate_btn)
        time.sleep(1)

        # Select escalate to dropdown
        escalate_dropdown = wait.until(EC.presence_of_element_located(
            (By.XPATH, BulkActionsPageElements.ESCALATE_TO_DROPDOWN)
        ))
        safe_click(escalate_dropdown)
        time.sleep(1)

        # Select Juwairia CSD
        juwairia_option = wait.until(EC.presence_of_element_located(
            (By.XPATH, BulkActionsPageElements.JUWAIRIA_CSD_OPTION)
        ))
        safe_click(juwairia_option)
        time.sleep(1)

        # Add escalation note
        escalation_note = wait.until(EC.presence_of_element_located(
            (By.XPATH, BulkActionsPageElements.ESCALATION_NOTE_FIELD)
        ))
        escalation_note.clear()
        escalation_note.send_keys("escalate")
        time.sleep(0.5)

        # Send
        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.SEND_BUTTON)))
        safe_click(send_btn)
        time.sleep(2)
        print("✅ Escalate completed")

        driver.refresh()
        time.sleep(20)

        # ✅ Step 7: Reply & Close from On Hold
        print("\n📝 Step 7: Reply & Close from On Hold tickets...")
        # Click On Hold tab
        on_hold_tab = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.ON_HOLD_TAB)))
        safe_click(on_hold_tab)
        time.sleep(2)

        checkbox24 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.PRAVEEN_SINGA)))
        if not checkbox24.is_selected():
            safe_click(checkbox24)
        
        checkbox25 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.ABDUL_A)))
        if not checkbox25.is_selected():
            safe_click(checkbox25)
        time.sleep(1)

        # Click Reply
        reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.REPLY_BUTTON)))
        safe_click(reply_btn)
        time.sleep(1)

        # Select Reply Type dropdown
        reply_type_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.REPLY_TYPE_DROPDOWN)))
        safe_click(reply_type_dropdown)
        time.sleep(1)

        # Select Reply & Close
        reply_close_option = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.REPLY_CLOSE_OPTION)))
        safe_click(reply_close_option)
        time.sleep(1)

        # Write reply
        reply_field = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.REPLY_FIELD)))
        reply_field.clear()
        reply_field.send_keys("close")
        time.sleep(0.5)

        # Send
        send_reply = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.SEND_BUTTON)))
        safe_click(send_reply)
        time.sleep(2)
        print("✅ Reply & Close completed")

        driver.refresh()
        time.sleep(15)

        # ✅ Step 8: Assign (Bulk Action)
        print("\n📝 Step 8: Assigning tickets to Bilal Shaikh...")
        
        # Navigate to Open tab
        open_tab = wait.until(EC.presence_of_element_located(
            (By.XPATH, BulkActionsPageElements.OPEN_TAB)
        ))
        safe_click(open_tab)
        time.sleep(5)

        with allure.step("Add Step - Assign"):
            
            # Scroll 
            try:
                ticket_1 = driver.find_element(By.XPATH, BulkActionsPageElements.BILALTEST1CX)
                driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", ticket_1)
                time.sleep(0.3)
                # Scroll down further to reveal Send Alert
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(0.5)
            except:
                pass

        checkbox1 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.BILALTEST1CX)))
        if not checkbox1.is_selected():
            safe_click(checkbox1)
        
        checkbox2 = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.PRAGYAANTEST)))
        if not checkbox2.is_selected():
            safe_click(checkbox2)
        time.sleep(1)

        # Click Assign        
        assign_btn = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.ASSIGN_BUTTON)))
        safe_click(assign_btn)
        time.sleep(1)

        # Open assign dropdown
        assign_dropdown = wait.until(EC.presence_of_element_located(
            (By.XPATH, BulkActionsPageElements.ASSIGN_FORM_DROPDOWN)
        ))
        safe_click(assign_dropdown)
        time.sleep(1)

        # Select Bilal Shaikh
        bilal_option = wait.until(EC.presence_of_element_located(
            (By.XPATH, BulkActionsPageElements.BILAL_SHAIKH_OPTION)
        ))
        safe_click(bilal_option)
        time.sleep(1)

        # Click Assign button
        assign_confirm = wait.until(EC.presence_of_element_located((By.XPATH, BulkActionsPageElements.ASSIGN_CONFIRM_BUTTON)))
        safe_click(assign_confirm)
        time.sleep(2)
        print("✅ Assign completed")

        time.sleep(60)

        print("\n🎉 All bulk actions completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        if driver:
            capture_failure_screenshot(driver, test_name)
        raise

    finally:
        if driver:
            time.sleep(3)
            print("🔚 Closing browser...")
            driver.quit()


if __name__ == "__main__":
    test_bulk_actions()