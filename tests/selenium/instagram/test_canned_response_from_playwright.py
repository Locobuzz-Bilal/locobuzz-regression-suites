import pytest
import time
import os
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from locobuzz_login.CX_login import locobuzzLogin
from config.config import TICKET_IDS
from elements.reply_panel_page import ReplyPanelPageElements
from elements.login_page import LoginPageElements
from elements.accountSettings_page import AccountSettingsPageElements

TICKET_ID = TICKET_IDS.get("instagram")


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/canned_response"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_canned_response_from_playwright():
    test_name = "instagram_canned_response_from_playwright"
    driver = None
    try:
        # credentials helpers used in repo
        from utils.credentials import get_sa_creds, get_instagram_creds
        sa_username, sa_password = get_sa_creds()
        agent_username, agent_password = get_instagram_creds()

        print("🔹 Login as supervisor")
        driver = locobuzzLogin(sa_username, sa_password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
                from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        # Scroll into view then try a normal click first
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                        time.sleep(0.3)
                        el.click()
                        return
                    except StaleElementReferenceException:
                        # If element is stale, find again by xpath if possible
                        time.sleep(0.5)
                        if attempt == max_retries - 1:
                            raise
                        continue
                    except ElementClickInterceptedException as intercepted:
                        # If something overlays the element, try to hide overlays or use JS click
                        try:
                            # attempt to remove common overlay/footer elements before clicking
                            driver.execute_script("var el=document.querySelector('.foot'); if(el) el.style.display='none';")
                        except Exception:
                            pass
                        try:
                            driver.execute_script("arguments[0].click();", el)
                            return
                        except Exception:
                            # fallback to ActionChains click
                            try:
                                ActionChains(driver).move_to_element(el).click(el).perform()
                                return
                            except Exception:
                                time.sleep(0.6)
                                if attempt == max_retries - 1:
                                    raise intercepted
                                continue
                    except Exception as e:
                        # unknown exception, retry a couple times
                        time.sleep(0.5)
                        if attempt == max_retries - 1:
                            raise e
                        continue

        # Open profile menu -> Account Settings
        time.sleep(2)
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(1)
        account_settings = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(1)

        # Search "canned"
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        search_field.click()
        search_field.send_keys("canned")
        time.sleep(1)

        # Click Canned Responses
        canned_link = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.CANNED_RESPONSES_LINK)))
        safe_click(canned_link)
        time.sleep(2)

        # Select Brand -> Juws
        brand_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.BRAND_DROPDOWN)))
        safe_click(brand_dropdown)
        time.sleep(1)
        juws_option = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.JUWS_BRAND_OPTION)))
        safe_click(juws_option)
        time.sleep(1)

        # Add Response with text + personalization + attachments
        add_btn = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ADD_RESPONSES_BUTTON)))
        safe_click(add_btn)
        time.sleep(1)

        # Fill name and text
        name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.RESPONSE_NAME_FIELD)))
        name_field.click()
        name_field.clear()
        name_field.send_keys("testing0005")
        time.sleep(0.5)

        text_area = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.RESPONSE_PREVIEW)))
        text_area.click()
        text_area.send_keys("test")
        time.sleep(0.5)

        # Personalize -> Full Name (attempt to open menu and pick)
        try:
            attach_personalize = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PERSONALIZE_BUTTON)))
            safe_click(attach_personalize)
            full_name_item = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.PERSONALIZE_FULLNAME)))
            safe_click(full_name_item)
        except Exception:
            # If element not present, continue
            pass

        time.sleep(1)

        # Attachment flow: open attachment dialog, select first few items and attach
        attach_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ATTACHMENT_BUTTON)))
        safe_click(attach_btn)
        time.sleep(1)

        # Select some media items if available
        try:
            first_img = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SECOND_IMAGE)))
            safe_click(first_img)
            time.sleep(0.5)
            attach_confirm = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ATTACH_BUTTON)))
            safe_click(attach_confirm)
            time.sleep(1)
        except Exception:
            pass

        # Save response
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_RESPONSE_BUTTON)))
        safe_click(save_btn)
        time.sleep(3)  # Allow save operation to complete

        # Add another response with only text - re-locate add button
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_RESPONSES_BUTTON)))
        safe_click(add_btn)
        time.sleep(2)
        name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.RESPONSE_NAME_FIELD)))
        name_field.click(); name_field.clear(); name_field.send_keys("onlytext05")
        text_area = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.RESPONSE_PREVIEW)))
        text_area.click(); text_area.clear(); text_area.send_keys("asdrftgyhuoipk")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_RESPONSE_BUTTON)))
        safe_click(save_btn)
        time.sleep(2)

        # Add response with only attachment - re-locate add button
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ADD_RESPONSES_BUTTON)))
        safe_click(add_btn)
        time.sleep(2)
        name_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.RESPONSE_NAME_FIELD)))
        name_field.click(); name_field.clear(); name_field.send_keys("onlyattachment05")
        attach_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ATTACHMENT_BUTTON)))
        safe_click(attach_btn)
        time.sleep(2)
        try:
            first_img = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.FIRST_IMAGE)))
            safe_click(first_img)
            safe_click(wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SECOND_IMAGE))))
            time.sleep(0.5)
            attach_confirm = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.ATTACH_BUTTON)))
            safe_click(attach_confirm)
        except Exception:
            pass
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.SAVE_RESPONSE_BUTTON)))
        safe_click(save_btn)
        safe_click(wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.DISMISS))))
        time.sleep(2)
        safe_click(wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CANCEL))))
        time.sleep(2)

        # Edit the first response
        try:
            # locate by text containing testing0001
            edit_target = wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()=' juws']")))
            safe_click(edit_target)
            safe_click(wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.EDIT))))
            time.sleep(2)
            edit_textarea = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.RESPONSE_PREVIEW)))
            edit_textarea.clear(); edit_textarea.send_keys("hi juws 30th sep november 3")
            update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.UPDATE)))
            safe_click(update_btn)
            time.sleep(2)
        except Exception:
            pass

        # Delete one of the test responses if present
        confirm_yes = None
        try:
            delete_target = wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()=' testing0005']")))
            safe_click(delete_target)
            delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Delete']")))
            safe_click(delete_btn)
            time.sleep(1)
            confirm_yes = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Yes']")))
            safe_click(confirm_yes)
            time.sleep(2)
        except Exception:
            pass

        # Logout supervisor
        profile_menu = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        time.sleep(1)
        logout_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.LOGOUT_BUTTON)))
        safe_click(logout_btn)
        time.sleep(1)
        confirm_logout = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.CONFIRM_LOGOUT_BUTTON)))
        safe_click(confirm_logout)
        time.sleep(2)

        # Login as agent
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.USERNAME_FIELD)))
        username_field.click(); username_field.clear(); username_field.send_keys(agent_username)
        cont_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.CONTINUE_BUTTON)))
        safe_click(cont_btn)
        time.sleep(1)
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.PASSWORD_FIELD)))
        password_field.click(); password_field.clear(); password_field.send_keys(agent_password)
        login_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.LOGIN_BUTTON)))
        safe_click(login_btn)
        time.sleep(2)

        # Select all brands and submit if prompt appears
        try:
            select_all = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SELECT_ALL_BRANDS)))
            safe_click(select_all)
            submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.SUBMIT_BUTTON)))
            safe_click(submit_btn)
            time.sleep(1)
        except Exception:
            pass

        # Search ticket
        search_icon = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_ICON)))
        safe_click(search_icon)
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEARCH_FIELD)))
        search_input.click(); search_input.clear(); search_input.send_keys(TICKET_ID); search_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # Open reply and discard then reopen reply
        reply_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.REPLY_BUTTON)))
        safe_click(reply_btn); time.sleep(1)
        discard_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_BUTTON)))
        safe_click(discard_btn); time.sleep(0.5)
        discard_submit = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
        safe_click(discard_submit); time.sleep(1)

        # Click canned response icon, choose response and send
        canned_icon = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CANNED_RESPONSE_ICON)))
        safe_click(canned_icon); time.sleep(1)
        canned_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CANNED_RESPONSE_DROPDOWN)))
        safe_click(canned_dropdown); time.sleep(1)
        # Select response by visible text
        option = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(),'testing0005') or contains(text(),'onlytext') or contains(text(),'onlyattachment') ]")))
        safe_click(option); time.sleep(1)
        select_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SELECT_CANNED_BUTTON)))
        safe_click(select_btn); time.sleep(1)
        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SEND_BUTTON)))
        safe_click(send_btn); time.sleep(2)

        print("✅ Converted canned response flow completed")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        if driver:
            capture_failure_screenshot(driver, test_name)
        raise

    finally:
        if driver:
            print("🧹 Closing browser")
            driver.quit()
