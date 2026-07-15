"""
27th November 2025
Script according to the manual regression sheet.
used a facebook comment ticket. Make sure there are mentions in the ticket as we need it to attach a ticket
+ linkedin reply n close - ticket gen
FLOW:
1. PRIORITY
2. MARK INFLUENCER
3. CATEGORY SELECTION
4. OPEN LINK
5. SEND EMAIL
6. OPEN DETAILS & ADD NOTE
7. PERSONAL DETAILS UPDATE
8. DIRECT CLOSE WITH NOTE
9. REOPEN TICKET FROM CLOSED TICKETS
10. ATTACH TICKET
11. DATE RANGE FILTER
12. ADD TAB
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
from elements.manual_reg_page import ManualRegElements
from elements.reply_panel_page import ReplyPanelPageElements
import allure
from config.config import TICKET_IDS
from utils.credentials import get_facebook_creds 
TICKET_ID = TICKET_IDS["facebook"]

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/facebook_preprod"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_manual_reg_operations():
    """Test Facebook ticket operations: search, priority, filters, attach ticket, add tab"""
    test_name = "test_manual_reg_operations"
    driver = None

    try:
        print("🔹 Logging in using Selenium (PreProd) Facebook Credentials...")
        from utils.credentials import get_facebook_creds
        username, password = get_facebook_creds()
        driver = locobuzzLoginPreProd(username, password)
        wait = WebDriverWait(driver, 20)

        # CSS for the transient dialog-close animation backdrop that intercepts
        # clicks (class is exactly "cdk-overlay-backdrop controlled clone"). This
        # is NOT a legitimate open dialog — it's the fading clone left behind for
        # a fraction of a second after a Material dialog closes. We only ever wait
        # on THIS specific backdrop, never on plain/dark backdrops of open dialogs.
        TRANSIENT_BACKDROP_CSS = "div.cdk-overlay-backdrop.controlled.clone"

        def safe_click(element):
            """Click an element, riding out the transient dialog-close backdrop.

            Reactive only: we attempt a normal click first, and ONLY if it is
            intercepted do we wait for the fading `controlled clone` backdrop to
            detach and retry a *real* click. We deliberately avoid the old
            behaviour of silently JS-clicking through an interception — that fired
            the click behind the overlay (a no-op) and desynced later steps,
            which is why failures landed on a different step each run.
            """
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(0.3)

            last_exc = None
            for attempt in range(3):
                try:
                    element.click()
                    return
                except Exception as e:
                    last_exc = e
                    msg = str(e)
                    if "intercepted" in msg or "not clickable" in msg:
                        # A fading backdrop is in the way — wait for that specific
                        # clone to detach, then retry the real click.
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.invisibility_of_element_located(
                                    (By.CSS_SELECTOR, TRANSIENT_BACKDROP_CSS)
                                )
                            )
                        except Exception:
                            pass
                        time.sleep(0.3)
                        continue
                    # Not an interception (e.g. stale/other) — stop retrying real clicks.
                    break

            # Fallbacks only after real clicks are exhausted.
            print(f"⚠️ Regular click failed after retries: {last_exc}, trying JavaScript click...")
            try:
                driver.execute_script("arguments[0].click();", element)
            except Exception as e2:
                print(f"⚠️ JavaScript click failed: {e2}, trying ActionChains...")
                ActionChains(driver).move_to_element(element).click().perform()

        def wait_and_click(xpath, timeout=20):
            """Wait for element and click safely"""
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            safe_click(element)
            return element

        def get_ticket_count():
            """Extract ticket count from OPEN tab (e.g., 'Open (8)' returns 8)"""
            try:
                # Try to find the active tab with count
                count_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ManualRegElements.OPEN_TAB_COUNT))
                )
                # Extract text like "(8)" and get the number
                count_text = count_element.text.strip()
                print(f"🔍 Found count element text: '{count_text}'")
                count = int(count_text.replace('(', '').replace(')', '').strip())
                print(f"📊 Current ticket count in 'Open' tab: {count}")
                return count
            except Exception as e:
                print(f"⚠️ Could not extract ticket count: {str(e)[:100]}")
                # Try alternative approach - find any span with parentheses in active tab
                try:
                    alt_element = driver.find_element(By.XPATH, "//a[contains(@class,'active')]//span")
                    if alt_element and '(' in alt_element.text:
                        count_text = alt_element.text.strip()
                        count = int(count_text.replace('(', '').replace(')', '').strip())
                        print(f"📊 (Alternative) Current ticket count: {count}")
                        return count
                except:
                    pass
                return None

        # Select All Brands & Submit
        print("📝 Selecting all brands...")
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
        safe_click(select_all)
        time.sleep(1)

        submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
        safe_click(submit_btn)
        time.sleep(3)
        print("✅ Brands selected and submitted")

        # Search for Ticket
        search_btn=wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)
        search_icon = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
        safe_click(search_icon)
        time.sleep(1)

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

        # Click search again to execute search
        safe_click(search_icon)
        time.sleep(3)
        print("✅ Ticket search completed")

        # ✅ Step 1: Change Priority
        print("\n📝 Step 1: Changing ticket priority to Medium...")
        priority_low = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.PRIORITY_LOW)))
        safe_click(priority_low)
        time.sleep(1)

        priority_medium = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.PRIORITY_MEDIUM)))
        safe_click(priority_medium)
        time.sleep(2)
        print("✅ Priority changed to Medium")

        # ✅ Step 2: Mark Influencer

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

        # ✅ Step 3: Change category
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

        # Submitting the mention dialog closes it; wait for the dialog-close
        # backdrop to detach so the reply panel re-renders before we look for the
        # open-link button (otherwise OPEN_LINK_BUTTON isn't in the DOM yet).
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, TRANSIENT_BACKDROP_CSS))
            )
        except Exception:
            pass
        time.sleep(2)

        original_window = driver.current_window_handle

        # Step 4: Open link in new tab

        open_link = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OPEN_LINK_BUTTON)))
        driver.execute_script("arguments[0].click();", open_link)
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.window(driver.window_handles[-1])
        print("✅ Opened new link")
        # Switch back to the original tab
        driver.switch_to.window(original_window)
        print("🔙 Returned to the first tab")

        #  Step 5: Send Email
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

        # ✅ Step 6: Open Details & Add Note
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
        
        add_note = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ADD_NOTE_BUTTON)))
        safe_click(add_note)
        note_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ADD_NOTE_TEXTAREA)))
        note_box.send_keys("hello testing")

        save_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SAVE_BUTTON)))
        safe_click(save_btn)
        print("✅ Note added successfully")

        # Go Back
        back_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.BACK_TO_TICKET_LIST)))
        safe_click(back_btn)

        # ✅ Step 7: Personal Details Update

        account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
        safe_click(account_box)
        personal_details = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.PERSONAL_DETAILS_TAB)))
        safe_click(personal_details)

        # Wait for the name input to be visible and enabled
        name_box = wait.until(EC.visibility_of_element_located((By.XPATH, ReplyPanelPageElements.NAME_INPUT_FIELD)))
        wait.until(lambda d: name_box.is_enabled())
        try:
            name_box.clear()
        except Exception as e:
            print(f"⚠️ name_box.clear() failed: {e}, using JS to clear value...")
            driver.execute_script("arguments[0].value = ''", name_box)
        time.sleep(0.5)
        name_box.send_keys("juwairia")
        update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.UPDATE_BUTTON)))
        safe_click(update_btn)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        print("✅ Personal details updated")

        # ✅ Step 8: Close with Note

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

# Step 9: Reopen Ticket from Closed Tickets

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
            time.sleep(3)

        with allure.step("Open Account Box and Overview"):
            account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
            time.sleep(1)
            safe_click(account_box)
            time.sleep(2)
            overview_tab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OVERVIEW_TAB)))
            safe_click(overview_tab)
            time.sleep(2)

        with allure.step("Change Ticket Status to Open"):
            ticket_status = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.TICKET_STATUS_DROPDOWN)))
            safe_click(ticket_status)
            time.sleep(2)
            open_option = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.OPEN_STATUS_OPTION)))
            safe_click(open_option)
            time.sleep(2)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)

        with allure.step("Refresh to view reopened ticket"):
            driver.refresh()
            time.sleep(3)
        
        # ✅ Step 10: Attach Ticket
        print("\n📝 Step 10: Attaching ticket...")
        more_options = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.MORE_OPTIONS_ICON)))
        safe_click(more_options)
        time.sleep(1)

        attach_ticket_menu = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.ATTACH_TICKET_MENU)))
        safe_click(attach_ticket_menu)
        time.sleep(1)

        # Select attach to dropdown
        # Wait for overlays to disappear before clicking dropdown
        # WebDriverWait(driver, 10).until(
        #     EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop"))
        # )

        time.sleep(2)  # Additional wait to ensure dialog is ready
        attach_to_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.ATTACH_TO_DROPDOWN)))
        safe_click(attach_to_dropdown)
        time.sleep(1)

        first_option = wait.until(EC.presence_of_element_located((By.XPATH, "(//mat-option[@role='option'])[1]")))
        safe_click(first_option)
        time.sleep(1)

        # Add note
        attach_note = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.ATTACH_NOTE_FIELD)))
        attach_note.click()
        attach_note.clear()
        attach_note.send_keys("attach ticket")
        time.sleep(0.5)

        # Click Attach button (first occurrence)
        attach_btn = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.ATTACH_BUTTON)))
        safe_click(attach_btn)
        time.sleep(2)
        
        # Click Attach button again (confirmation)
        try:
            attach_btn2 = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.ATTACH_BUTTON)))
            safe_click(attach_btn2)
            time.sleep(2)
        except:
            pass

        print("✅ Ticket attached")

        # Wait for success message
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='The operation Attach Ticket was completed successfully']")))
            print(f"✅ Success message: {success_msg.text}")
            time.sleep(2)
        except:
            print("⚠️ No success message detected")

        # ✅ Step 11: Date Range Filter
        print("\n📝 Step 11: Setting date range filter...")
        duration_input = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.DURATION_INPUT)))
        safe_click(duration_input)
        time.sleep(1)

        # Click Last 30 Days
        last_30_days = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.LAST_30_DAYS)))
        safe_click(last_30_days)
        time.sleep(1)

        # Click custom
        custom_btn = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.CUSTOM_BUTTON)))
        safe_click(custom_btn)
        time.sleep(1)

        # Select date 16 (first occurrence)
        try:
            date_16_first = wait.until(EC.presence_of_element_located((By.XPATH, "(//span[text()='16'])[1]")))
            safe_click(date_16_first)
            time.sleep(0.5)
        except:
            print("⚠️ Could not select date 16 (first)")

        # Select date 20 (fourth occurrence)
        try:
            date_20_fourth = wait.until(EC.presence_of_element_located((By.XPATH, "(//span[text()='20'])[1]")))
            safe_click(date_20_fourth)
            time.sleep(0.5)
        except:
            print("⚠️ Could not select date 20 (fourth)")

        # Click Done
        done_btn = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.DONE_BUTTON)))
        safe_click(done_btn)
        time.sleep(2)
        print("✅ Custom date range set")

        # ✅ Step 5: Reset to Today
        print("\n📝 Step 5: Resetting to Today...")
        try:
            calendar_block = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'custom__block--calendar')]")))
            safe_click(calendar_block)
            time.sleep(1)

            today_btn = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.TODAY_BUTTON)))
            safe_click(today_btn)
            time.sleep(1)

            done_btn2 = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.DONE_BUTTON)))
            safe_click(done_btn2)
            time.sleep(2)
            print("✅ Date reset to Today")
        except:
            print("⚠️ Could not reset to today")

        driver.refresh()
        time.sleep(10)
        search_btn=wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_btn)
        search_icon = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
        safe_click(search_icon)
        time.sleep(1)

        # # Search Ticket
        # search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        # safe_click(search_btn)
        # search_field = wait.until(EC.presence_of_element_located(
        #     (By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)
        # ))
        # search_field.clear()
        # search_field.send_keys(TICKET_ID)
        # safe_click(search_btn)
        # time.sleep(3)

        # # Click search again to execute search
        # safe_click(search_icon)
        # time.sleep(3)
        # print("✅ Ticket search completed")

        # #Step 8: Create Ticket with count verification
        # print("\n📝 Step 8: create ticket...")
        
        # # Get initial ticket count
        # initial_count = get_ticket_count()
        
        # # Click on the ticket to select it first
        # try:
        #     ticket_item = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'post__content')]")))
        #     safe_click(ticket_item)
        #     time.sleep(2)
        # except:
        #     print("⚠️ Could not click ticket item, trying to proceed...")
        
        # safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OPEN_DETAILS_BUTTON))))
        # time.sleep(2)
        # safe_click(wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='mat-mdc-menu-trigger post__foot--item post__foot--itemaction hover-itemaction ng-star-inserted']//mat-icon[normalize-space()='more_vert']"))))
        # time.sleep(2)
        # safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.CREATE_TICKET_BUTTON))))
        # time.sleep(2)

        # #Enter note
        # enter_note = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.ENTER_NOTE_HERE)))
        # safe_click(enter_note)
        # enter_note.send_keys("Creating ticket via automation")
        # safe_click(wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SAVE_BUTTON))))
        # time.sleep(2)
        # print("✅ Ticket created")

        # # Wait for success message
        # try:
        #     ticket_success = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Ticket created successfully']")))
        #     print(f"✅ {ticket_success.text}")
        # except:
        #     print("⚠️ Ticket success message not found")
        
        # # Wait a moment for UI to update
        # time.sleep(2)
        
        # # Verify ticket count increment
        # final_count = get_ticket_count()
        
        # if initial_count is not None and final_count is not None:
        #     if final_count == initial_count + 1:
        #         print(f"✅ Ticket count verified! Increased from {initial_count} to {final_count}")
        #     elif final_count > initial_count:
        #         print(f"✅ Ticket count increased from {initial_count} to {final_count} (+{final_count - initial_count})")
        #     else:
        #         print(f"⚠️ Warning: Ticket count did not increase (Before: {initial_count}, After: {final_count})")
        # else:
        #     print("⚠️ Could not verify ticket count change")

        # ✅ Step 12: Add Tab
        print("\n📝 Step 12: Adding new tab...")
        
        # Dismiss any overlays that might be blocking
        try:
            overlay = driver.find_element(By.XPATH, "//div[contains(@class,'cdk-overlay-backdrop')]")
            if overlay:
                print("⚠️ Overlay detected, clicking to dismiss...")
                driver.execute_script("arguments[0].click();", overlay)
                time.sleep(1)
        except:
            pass  # No overlay found, continue
        
        add_tab_icon = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.ADD_TAB_ICON)))
        # Wait for icon to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ManualRegElements.ADD_TAB_ICON)))
        safe_click(add_tab_icon)
        time.sleep(3)

        # Wait for menu to appear and be clickable
        print("⏳ Waiting for Add Tab button to be clickable...")
        add_tab_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, ManualRegElements.ADD_TAB_BUTTON))
        )
        print("🖱️ Clicking Add Tab button...")
        safe_click(add_tab_btn)
        time.sleep(1)

        # Enter tab name
        tab_name_input = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.TAB_NAME_INPUT)))
        tab_name_input.click()
        tab_name_input.clear()
        tab_name_input.send_keys("testing")
        time.sleep(0.5)

        # Submit
        submit_tab = wait.until(EC.presence_of_element_located((By.XPATH, ManualRegElements.SUBMIT_TAB_BUTTON)))
        safe_click(submit_tab)
        time.sleep(2)

        print("\n🎉 All ticket operations completed successfully!")

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
    test_manual_reg_operations()