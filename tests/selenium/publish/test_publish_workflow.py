#13NOV25 - Publish Workflow - Send for Approval, Edit, Save Draft, Delete
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from elements.publish_page import PublishPageElements
from elements.login_page import LoginPageElements
from utils.credentials import get_sa_creds
from selenium.common.exceptions import NoSuchElementException

def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/publish"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")

def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    driver.execute_script("arguments[0].click();", element)

@pytest.mark.selenium
def test_publish_workflow():
    test_name = "publish_workflow"
    driver = None
    try:
        print("🔹 Starting Publish Workflow Test...")
        from utils.credentials import get_sa_creds
        username, password = get_sa_creds()
        driver = locobuzzLoginPreProd(username, password)
        wait = WebDriverWait(driver, 20)

        print("🟢 Navigating to Publish...")
        
        # Click Publish link
        publish_link = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.PUBLISH_LINK)))
        safe_click(driver, publish_link)
        time.sleep(2)

        # Click Brand dropdown (SVG)
        brand_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.BRAND_DROPDOWN)))
        safe_click(driver, brand_dropdown)
        time.sleep(1)

        # Select Juws brand
        juws_option = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.JUWS_BRAND_OPTION)))
        safe_click(driver, juws_option)
        time.sleep(1)

        print("🟢 Creating new post...")

        # Click Compose Post
        compose_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.COMPOSE_POST_BUTTON)))
        safe_click(driver, compose_btn)
        time.sleep(2)

        # Click Location Mode
        location_mode_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.LOCATION_MODE_BUTTON)))
        safe_click(driver, location_mode_btn)
        time.sleep(1)

        # Click first image
        first_image = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.FIRST_IMAGE)))
        safe_click(driver, first_image)
        time.sleep(1)

        # Check checkbox (Instagram account)
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.ACCOUNT_CHECKBOX)))
        if not checkbox.is_selected():
            safe_click(driver, checkbox)
        time.sleep(1)

        # ========== FILTER BY CITY ==========
        print("🟢 Opening Cities dropdown...")
        cities_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.CITIES_DROPDOWN)))
        safe_click(driver, cities_dropdown)
        time.sleep(1)

        print("🟢 Selecting New Delhi...")
        new_delhi_option = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.NEW_DELHI_OPTION)))
        safe_click(driver, new_delhi_option)
        time.sleep(1)
        
        # Close dropdown by clicking backdrop
        try:
            backdrop = driver.find_element(By.CSS_SELECTOR, PublishPageElements.OVERLAY_BACKDROP)
            backdrop.click()
            time.sleep(0.5)
        except:
            pass

        # ========== FILTER BY TAGS ==========
        print("🟢 Opening Tags dropdown...")
        tags_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.TAGS_DROPDOWN)))
        safe_click(driver, tags_dropdown)
        time.sleep(1)

        print("🟢 Selecting tag...")
        # Select the checkbox in the tags dropdown
        tag_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.TAG_CHECKBOX)))
        safe_click(driver, tag_checkbox)
        time.sleep(1)
        
        # Close dropdown
        try:
            backdrop = driver.find_element(By.CSS_SELECTOR, PublishPageElements.OVERLAY_BACKDROP)
            backdrop.click()
            time.sleep(0.5)
        except:
            pass

        # ========== FILTER BY CHANNELS ==========
        print("🟢 Opening Channels dropdown...")
        channels_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.CHANNELS_DROPDOWN)))
        safe_click(driver, channels_dropdown)
        time.sleep(1)

        print("🟢 Selecting Facebook channel...")
        facebook_option = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.FACEBOOK_CHANNEL)))
        safe_click(driver, facebook_option)
        time.sleep(1)
        
        # Close dropdown
        try:
            backdrop = driver.find_element(By.CSS_SELECTOR, PublishPageElements.OVERLAY_BACKDROP)
            backdrop.click()
            time.sleep(0.5)
        except:
            pass

        # ========== APPLY FILTERS ==========
        print("🟢 Applying filters...")
        apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.APPLY_FILTERS_BUTTON)))
        safe_click(driver, apply_btn)
        time.sleep(3)

        # ========== CHECK FOR NO DATA & SEARCH ==========
        print("🟢 Checking if data is available...")
        try:
            no_data = driver.find_element(By.XPATH, PublishPageElements.NO_DATA_FOUND)
            if no_data.is_displayed():
                print("⚠️ No data found with current filters, clearing and searching Mumbai...")
                
                # Clear filters
                clear_btn = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.CLEAR_ALL_FILTERS_BUTTON)))
                safe_click(driver, clear_btn)
                time.sleep(1)
                
                # Search for Mumbai
                search_box = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.SEARCH_LOCATION_INPUT)))
                search_box.click()
                search_box.clear()
                search_box.send_keys("mumbai")
                time.sleep(1)
                
                # Apply search
                apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.APPLY_FILTERS_BUTTON)))
                safe_click(driver, apply_btn)
                time.sleep(2)
        except NoSuchElementException:
            print("✅ Data found, proceeding...")

        # ========== SELECT SOCIAL PROFILE ==========
        # print("🟢 Selecting social profile...")
        # # Select the first available checkbox
        # profile_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.PROFILE_CHECKBOX)))
        # if not profile_checkbox.is_selected():
        #     safe_click(driver, profile_checkbox)
        # time.sleep(1)

        # Click Next
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.NEXT_BUTTON)))
        safe_click(driver, next_btn)
        time.sleep(2)

        print("🟢 Adding media and caption...")

        #Enter Caption
        caption = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.CAPTION)))
        safe_click(driver, caption)
        caption.clear()
        caption.send_keys("test again")
        time.sleep(2)

         # ========== PERSONALIZE (OPTIONAL) ==========
        print("🟢 Attempting personalization...")
        try:
            personalize_btn = driver.find_element(By.XPATH, PublishPageElements.PERSONALIZE_BUTTON)
            if personalize_btn.is_displayed():
                safe_click(driver, personalize_btn)
                time.sleep(1)
                
                # Click on PhoneNumber option
                phone_option = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.PHONE_NUMBER_OPTION)))
                safe_click(driver, phone_option)
                time.sleep(1)
                
                # Dismiss
                dismiss_btn = wait.until(EC.element_to_be_clickable((By.XPATH, PublishPageElements.DISMISS_LINK)))
                safe_click(driver, dismiss_btn)
                time.sleep(1)
                print("✅ Personalization added")
        except:
            print("⚠️ Personalize option not available, skipping...")

        # Click Attach Image
        attach_image_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.ATTACH_IMAGE_BUTTON)))
        safe_click(driver, attach_image_btn)
        time.sleep(2)

        # Select first image from gallery
        gallery_image = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.GALLERY_FIRST_IMAGE)))
        safe_click(driver, gallery_image)
        time.sleep(1)

        # Click Attach button
        attach_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.ATTACH_BUTTON)))
        safe_click(driver, attach_btn)
        time.sleep(2)

        # Click Next
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.NEXT_BUTTON)))
        safe_click(driver, next_btn)
        time.sleep(2)

        # Fill caption
        caption_field = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.CAPTION_FIELD)))
        caption_field.click()
        caption_field.send_keys("test again")
        time.sleep(1)

        # Click Next
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.NEXT_BUTTON)))
        safe_click(driver, next_btn)
        time.sleep(2)

        print("🟢 Sending for approval...")

        # # Select Publish Now radio
        # publish_now_radio = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.PUBLISH_NOW_RADIO)))
        # safe_click(driver, publish_now_radio)
        # time.sleep(1)

        # Click Send for Approval
        send_approval_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.SEND_APPROVAL_BUTTON)))
        safe_click(driver, send_approval_btn)
        time.sleep(3)

        print("🟢 Editing post...")

        # Click edit icon
        edit_icon = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.EDIT_ICON)))
        safe_click(driver, edit_icon)
        time.sleep(2)

        # Click Next
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.NEXT_BUTTON)))
        safe_click(driver, next_btn)
        time.sleep(2)

        # # Clear caption
        # caption_field = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.CAPTION_FIELD)))
        # caption_field.click()
        # caption_field.clear()
        # time.sleep(1)

        # Click Next twice
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.NEXT_BUTTON)))
        safe_click(driver, next_btn)
        time.sleep(1)
        
        next_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.NEXT_BUTTON)))
        safe_click(driver, next_btn)
        time.sleep(2)

        print("🟢 Saving as draft with schedule...")

        # Select Publish Later radio
        publish_later_radio = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.PUBLISH_LATER_RADIO)))
        safe_click(driver, publish_later_radio)
        time.sleep(1)

        # Click date picker
        date_picker = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.DATE_PICKER)))
        safe_click(driver, date_picker)
        time.sleep(1)

        # Select date (29th)
        date_29 = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.DATE_29)))
        safe_click(driver, date_29)
        time.sleep(1)

        # Click Apply button
        apply_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.APPLY_BUTTON)))
        safe_click(driver, apply_btn)
        time.sleep(1)

        # Click Save Draft
        save_draft_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.SAVE_DRAFT_BUTTON)))
        safe_click(driver, save_draft_btn)
        time.sleep(3)

        print("🟢 Deleting draft...")

        # Click delete icon
        delete_icon = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.DELETE_ICON)))
        safe_click(driver, delete_icon)
        time.sleep(2)

        # Confirm delete
        delete_confirm_btn = wait.until(EC.presence_of_element_located((By.XPATH, PublishPageElements.DELETE_CONFIRM_BUTTON)))
        safe_click(driver, delete_confirm_btn)
        time.sleep(3)

        print("✅ Publish workflow completed successfully")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        if driver:
            capture_failure_screenshot(driver, test_name)
        raise

    finally:
        if driver:
            print("🧹 Browser closed safely after publish workflow test")
            driver.quit()
