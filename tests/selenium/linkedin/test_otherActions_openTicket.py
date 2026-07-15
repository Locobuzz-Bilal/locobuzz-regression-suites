# running 20OCT25
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locobuzz_login.CX_login import locobuzzLogin
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from config.config import TICKET_IDS
TICKET_ID = TICKET_IDS["linkedin"]
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
        driver = locobuzzLogin("juw_agent", "Buzz@1234")
        wait = WebDriverWait(driver, 20)

        def safe_click(element):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            driver.execute_script("arguments[0].click();", element)

        # ✅ Select All & Submit
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Select all']")))
        safe_click(select_all)

        apply_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Submit ']")))
        safe_click(apply_btn)

        # ✅ Search Ticket


        # try:
        #     searchIcon = WebDriverWait(wait._driver, 5).until(
        #         EC.presence_of_element_located((By.XPATH, "//a[.//mat-icon[text()=' search']]"))
        #     )
        #     safe_click(searchIcon)
        # except TimeoutException:
        #     fallbackBtn = wait.until(EC.element_to_be_clickable(
        #             (By.XPATH, "//mat-icon[text()='inbox']"))
        #             )
        #     safe_click(fallbackBtn)
        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//a[.//mat-icon[text()=' search']]")))
        safe_click(search_btn)

        search_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]')
        ))
        search_field.clear()
        search_field.send_keys(TICKET_ID)
        safe_click(search_btn)
        safe_click(search_btn)
        print(f"🔍 Searched ticket: {TICKET_ID}")

        time.sleep(3)

        # ✅ Ticket Actions
        closed_tickets = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Closed Tickets')]")))
        safe_click(closed_tickets)

        account_box = wait.until(EC.presence_of_element_located((By.XPATH, "//mat-icon[text()='account_box']")))
        safe_click(account_box)
        time.sleep(2)

        overview_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='tab' and .='Overview']")))
        safe_click(overview_tab)
        time.sleep(2)

        ticket_status = wait.until(EC.presence_of_element_located
                                   ((By.XPATH, "//mat-label[normalize-space()='Ticket Status']/ancestor::mat-form-field//div[contains(@class,'mat-mdc-select-trigger')]")))
        safe_click(ticket_status)
        time.sleep(2)

        open_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-option//span[normalize-space()='Open']")))
        safe_click(open_option)
        time.sleep(2)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(3)

        # closeIcon = wait.until(EC.presence_of_element_located((By.XPATH, "//mat-icon[text()='close']")))
        # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", closeIcon)
        # time.sleep(1)
        # driver.execute_script("arguments[0].click();", closeIcon)
        # print("✅ Closed tab clicked safely via JS")


        # close_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//mat-icon[text()='close']")))
        # safe_click(close_tab)

        open_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//li[.//span[@class='post-option__name' and normalize-space(text())='Open']]")))
        safe_click(open_tab)
        
        safe_click(open_tab)
        time.sleep(2)
        more_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='More']")))
        safe_click(more_btn)

        mark_influencer = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Mark Influencer']")))
        safe_click(mark_influencer)

        influencer_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//mat-label[text()='Select Influencer Category']")))
        safe_click(influencer_dropdown)

        anchor_option = wait.until(EC.presence_of_element_located((By.XPATH, "//mat-option//span[normalize-space()='Anchor']")))
        safe_click(anchor_option)

        mark_influencer_confirm = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()=' Mark Influencer ']")))
        safe_click(mark_influencer_confirm)

        print("✅ Mark Influencer Done")

        # 🟢 Continue Additional Actions
        others_section = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//mat-icon[@role='img' and normalize-space(text())='alternate_email']")))
        safe_click(others_section)

        # Example selecting mention options
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()=' juw testing 1']"))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()=' testing 2']"))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()=' testing 3 ']"))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Neutral']"))))
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Submit']"))))
        print("✅ Mention categories selected and submitted")


        original_window = driver.current_window_handle
        # Open link in new tab

        open_link = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Open Link']")))
        driver.execute_script("arguments[0].click();", open_link)
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.window(driver.window_handles[-1])
        print("✅ Opened new link")
        # Switch back to the original tab
        driver.switch_to.window(original_window)
        print("🔙 Returned to the first tab")

        # Send Email
        send_email = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Send Email')]")))
        safe_click(send_email)
        time.sleep(2)
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='New To Email...']")))
        email_field.send_keys("juw@email.com")
        time.sleep(2)
        email_field.send_keys(u'\ue007')  # press Enter
        time.sleep(2)
        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Send ']")))
        safe_click(send_btn)
        print("✅ Email sent successfully")
        time.sleep(2)

        # Add Note
        open_details = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Open Details ']")))
        safe_click(open_details)
        time.sleep(2)

        
        discard_elements = driver.find_elements(By.XPATH, "//span[text()=' Discard ']")
        if discard_elements:
         safe_click(discard_elements[0])
        time.sleep(1)
    
        submit_elements = driver.find_elements(By.XPATH, "//span[text()=' Submit ']")
        if submit_elements:
             safe_click(submit_elements[0])
        else:
         print("Discard button not found, skipping...")
        

        # discard = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Discard ']")))
        # safe_click(discard)
        # time.sleep(1)
        # submitBtn2 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Submit ']")))
        # safe_click(submitBtn2)
        # time.sleep(1)
        
        add_note = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Add Note ']")))
        safe_click(add_note)
        note_box = wait.until(EC.presence_of_element_located((By.XPATH, "//mat-form-field[.//mat-label[text()='Add note']]//textarea")))
        note_box.send_keys("hello testing")

        # attach_media = wait.until(EC.presence_of_element_located((By.XPATH, "//a//span[text()='Attach Media']")))
        # safe_click(attach_media)
        # first_image = wait.until(EC.presence_of_element_located((By.XPATH, "(//img)[1]")))
        # safe_click(first_image)
        # attach_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Attach']")))
        # safe_click(attach_btn)

        save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Save ']")))
        safe_click(save_btn)
        print("✅ Note added successfully")

        # Go Back
        back_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Back To Ticket List']")))
        safe_click(back_btn)

        # Personal Details Update
        account_box = wait.until(EC.presence_of_element_located((By.XPATH, "//mat-icon[text()='account_box']")))
        safe_click(account_box)
        personal_details = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Personal Details']")))
        safe_click(personal_details)

        name_box = wait.until(EC.presence_of_element_located
                              ((By.XPATH, "//mat-form-field[.//mat-label[text()='Name']]//input")))
        name_box.clear()
        name_box.send_keys("juwairia")
        update_btn = wait.until(EC.presence_of_element_located((By.XPATH, " //span[text()=' Update ']")))
        safe_click(update_btn)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()   
        time.sleep(1)
        print("✅ Personal details updated")

        # Close with Note
        dropdown_close = wait.until(EC.presence_of_element_located((By.XPATH, "//span[.//span[text()='Direct Close']]//mat-icon[text()='keyboard_arrow_down']")))
        safe_click(dropdown_close)
        close_with_note = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Close With Note']")))
        safe_click(close_with_note)
        note_area = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='textArea']")))
        note_area.send_keys("direct closing with note")

        attach_media = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Attach Media']")))
        safe_click(attach_media)
        safe_click(wait.until(EC.presence_of_element_located
            ((By.XPATH, '//img[@src="https://images.locobuzz.com/LocoBuzzImages/SocialPostTriggerScheduling/reliancejiodb/002c68f8-4ff7-4678-b064-e6322f903bb8.png"]'))))
        time.sleep(2)
        safe_click(wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Attach ']"))))
        direct_close = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()=' Direct Close ']")))
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