#27NOV2025
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from elements.reply_panel_page import ReplyPanelPageElements
from utils.credentials import get_instagram_creds

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/chatbot"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

@pytest.mark.selenium
def test_chatbot_workflow():
    test_name = "chatbot_workflow"
    driver = None
    try:
        print("🔹 Logging in to PreProd using Selenium...")
        from utils.credentials import get_instagram_creds
        username, password = get_instagram_creds()
        driver = locobuzzLoginPreProd(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Chatbot Workflow actions...")

        # Select all & Submit
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.SELECT_ALL_BUTTON)))
        safe_click(select_all)
        submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.DISCARD_SUBMIT_BUTTON)))
        safe_click(submit_btn)
        time.sleep(2)

        # Click chat bubble icon to open chatbot
        chat_icon = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHAT_BUBBLE_ICON)))
        safe_click(chat_icon)
        time.sleep(2)

        insta_icon = wait.until(EC.element_to_be_clickable((By.XPATH,'(//img[@src="/assets/images/channel-logos/insta_dm.svg"])[2]')))
        safe_click(insta_icon)
        time.sleep(2)

        # Send text message "hello"
        reply_input = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CHATBOT_REPLY_INPUT)))
        reply_input.click()
        reply_input.clear()
        reply_input.send_keys("hello")
        
        # Click send button
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_SEND_BUTTON)))
        safe_click(send_btn)
        time.sleep(2)

        # Attach file - click attach_file icon
        attach_icon = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_ATTACH_FILE_ICON)))
        safe_click(attach_icon)
        time.sleep(1)

        # Select appleLogo.png from the file list
        apple_logo = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_APPLE_LOGO)))
        safe_click(apple_logo)
        time.sleep(1)

        # Send the attachment
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_ATTACH_BTN)))
        safe_click(send_btn)
        time.sleep(2)

        # Click emoji/satisfied icon (third icon in the row)
        emoji_icon = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_EMOJI_ICON)))
        safe_click(emoji_icon)
        time.sleep(1)

        #Select emoji
        select_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_EMOJI)))
        safe_click(select_btn)
        time.sleep(1)

        # Send the emoji
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_SEND_BUTTON)))
        safe_click(send_btn)
        time.sleep(2)

        # Click canned response icon
        canned_response_icon = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_CANNED_RESPONSE_ICON)))
        safe_click(canned_response_icon)
        time.sleep(2)

        safe_click(wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_SELECT_BUTTON))))
        time.sleep(2)
        
        # Send the canned response
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_SEND_BUTTON)))
        safe_click(send_btn)
        time.sleep(2)

        # Click escalation warning icon
        escalate_icon = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_ESCALATE_ICON)))
        safe_click(escalate_icon)
        time.sleep(2)

        # Click Escalate To dropdown
        escalate_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_ESCALATE_DROPDOWN)))
        safe_click(escalate_dropdown)
        time.sleep(1)

        # Select "Juwairia CSD (1)"
        escalate_user = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_JUWAIRIA_CSD)))
        safe_click(escalate_user)
        time.sleep(1)

        # Write escalation note
        escalation_note = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CHATBOT_ESCALATION_NOTE)))
        escalation_note.click()
        escalation_note.clear()
        escalation_note.send_keys("escalating")
        time.sleep(1)

        # Click Send button for escalation
        send_escalation_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_SEND_ESCALATION)))
        safe_click(send_escalation_btn)
        time.sleep(3)

        # Close the chatbot (click cancel)
        cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_CLOSE_BUTTON)))
        safe_click(cancel_btn)
        time.sleep(1)

        # Confirm Yes to close ticket
        yes_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_YES_BUTTON)))
        safe_click(yes_btn)
        time.sleep(2)

        # Verify success message
        success_msg = wait.until(EC.presence_of_element_located((By.XPATH, ReplyPanelPageElements.CHATBOT_SUCCESS_MESSAGE)))
        print(f"✅ Success message: {success_msg.text}")
        
        # Close the notification
        close_notification = wait.until(EC.element_to_be_clickable((By.XPATH, ReplyPanelPageElements.CHATBOT_CLOSE_NOTIFICATION)))
        safe_click(close_notification)
        time.sleep(1)

        print("✅ Chatbot workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after chatbot workflow")
