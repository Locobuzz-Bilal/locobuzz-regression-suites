import pytest
import time
import os
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements
from utils.credentials import get_email_creds

EMAIL_TICKET_ID = TICKET_IDS.get("email")


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/email"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"\U0001F4F8 Screenshot saved: {path}")
    allure.attach.file(path, name=test_name, attachment_type=allure.attachment_type.PNG)


def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    driver.execute_script("arguments[0].click();", element)


@pytest.mark.selenium
def test_email_other_actions_open_ticket():
    test_name = "email_other_actions_open_ticket"
    driver = None

    try:
        with allure.step("Login"):
            print("\u25AA Logging in for Email Other Actions...")
            try:
                username, password = get_email_creds()
            except RuntimeError as cred_err:
                pytest.skip(f"Skipping: {cred_err}")
            driver = locobuzzLogin(username, password)
            wait = WebDriverWait(driver, 25)

        with allure.step("Select All & Submit"):
            select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
            safe_click(driver, select_all)
            apply_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
            safe_click(driver, apply_btn)
            time.sleep(2)

        with allure.step("Search Ticket"):
            search_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
            safe_click(driver, search_btn)
            search_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_INPUT_BOX)))
            search_field.clear()
            search_field.send_keys(EMAIL_TICKET_ID)
            safe_click(driver, search_btn)
            safe_click(driver, search_btn)
            print(f"\U0001F50D Searched ticket: {EMAIL_TICKET_ID}")
            time.sleep(3)
 
        with allure.step("Navigate to Closed Tickets"):
            # Check if CT_TAB_ALTERNATE is available
            ct_alternate_elements = driver.find_elements(By.XPATH, ReplyPanelPageElements.CT_TAB_ALTERNATE)
            if ct_alternate_elements:
                # If CT_TAB_ALTERNATE exists, click it directly
                safe_click(driver, ct_alternate_elements[0])
                print("\u2705 Clicked CT_TAB_ALTERNATE")
            else:
                # Otherwise, click More and then Closed Tickets
                moreTab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MORE_OPTIONS_ICON)))
                safe_click(driver, moreTab)
                closed_tickets = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CLOSED_TICKETS_TAB)))
                safe_click(driver, closed_tickets)
                print("\u2705 Clicked More → Closed Tickets")
            time.sleep(3)

        with allure.step("Open Account Box and Overview"):
            account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", account_box)
            time.sleep(1)
            safe_click(driver, account_box)
            time.sleep(2)
            overview_tab = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OVERVIEW_TAB)))
            safe_click(driver, overview_tab)
            time.sleep(2)

        with allure.step("Change Ticket Status to Open"):
            ticket_status = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.TICKET_STATUS_DROPDOWN)))
            safe_click(driver, ticket_status)
            time.sleep(2)
            open_option = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.OPEN_STATUS_OPTION)))
            safe_click(driver, open_option)
            time.sleep(2)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)

        with allure.step("Refresh to view reopened ticket"):
            driver.refresh()
            time.sleep(3)

        with allure.step("Mark as Influencer"):
            more_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MORE_BUTTON)))
            safe_click(driver, more_btn)
            mark_influencer = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MARK_INFLUENCER_BUTTON)))
            safe_click(driver, mark_influencer)
            influencer_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.INFLUENCER_CATEGORY_DROPDOWN)))
            safe_click(driver, influencer_dropdown)
            anchor_option = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ANCHOR_OPTION)))
            safe_click(driver, anchor_option)
            mark_influencer_confirm = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MARK_INFLUENCER_CONFIRM)))
            safe_click(driver, mark_influencer_confirm)
            print("\u2705 Mark Influencer Done")

        with allure.step("Select Mention Categories"):
            others_section = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OTHERS_SECTION)))
            safe_click(driver, others_section)
            safe_click(driver, wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_JUW_TESTING_1))))
            safe_click(driver, wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_TESTING_2))))
            safe_click(driver, wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_TESTING_3))))
            safe_click(driver, wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_NEUTRAL))))
            safe_click(driver, wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.MENTION_SUBMIT))))
            print("\u2705 Mention categories selected and submitted")

        with allure.step("Send Email"):
            send_email = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEND_EMAIL_BUTTON)))
            safe_click(driver, send_email)
            time.sleep(2)
            email_field = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_INPUT_FIELD)))
            email_field.send_keys("juw@email.com")
            time.sleep(2)
            email_field.send_keys(u'\ue007')  # press Enter
            time.sleep(2)
            send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.EMAIL_SEND_BTN)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", send_btn)
            time.sleep(0.5)
            safe_click(driver, send_btn)
            print("\u2705 Email sent successfully")
            time.sleep(2)

        with allure.step("Add Note"):
            open_details = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.OPEN_DETAILS_BUTTON)))
            safe_click(driver, open_details)
            time.sleep(2)

            # Discard if present
            discard_elements = driver.find_elements(By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)
            if discard_elements:
                safe_click(driver, discard_elements[0])
                time.sleep(1)
                submit_elements = driver.find_elements(By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)
                if submit_elements:
                    safe_click(driver, submit_elements[0])
            else:
                print("Discard button not found, skipping...")

            add_note = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ADD_NOTE_BUTTON)))
            safe_click(driver, add_note)
            note_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ADD_NOTE_TEXTAREA)))
            note_box.send_keys("hello testing")
            save_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SAVE_BUTTON)))
            safe_click(driver, save_btn)
            print("\u2705 Note added successfully")

        with allure.step("Go Back to Ticket List"):
            back_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.BACK_TO_TICKET_LIST)))
            safe_click(driver, back_btn)

        with allure.step("Update Personal Details"):
            account_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ACCOUNT_BOX_ICON)))
            safe_click(driver, account_box)
            personal_details = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.PERSONAL_DETAILS_TAB)))
            safe_click(driver, personal_details)
            name_box = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.NAME_INPUT_FIELD)))
            name_box.clear()
            name_box.send_keys("juwairia")
            update_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.UPDATE_BUTTON)))
            safe_click(driver, update_btn)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
            print("\u2705 Personal details updated")

        with allure.step("Close Ticket with Note"):
            dropdown_close = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DIRECT_CLOSE_DROPDOWN)))
            safe_click(driver, dropdown_close)
            close_with_note = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CLOSE_WITH_NOTE_OPTION)))
            safe_click(driver, close_with_note)
            note_area = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CLOSE_NOTE_TEXTAREA)))
            note_area.send_keys("direct closing with note")
            attach_media = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_MEDIA_CLOSE)))
            safe_click(driver, attach_media)
            safe_click(driver, wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SPECIFIC_IMAGE))))
            time.sleep(2)
            safe_click(driver, wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.ATTACH_BUTTON_CLOSE))))
            direct_close = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DIRECT_CLOSE_BUTTON)))
            safe_click(driver, direct_close)
            time.sleep(3)
            print("\u2705 Ticket closed successfully!")

        print("\u2705 Email Other Actions test completed")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"\u274C Test failed: {e}")

    finally:
        if driver:
            driver.quit()
        print("\U0001F9F9 Browser closed and resources cleaned up.")
