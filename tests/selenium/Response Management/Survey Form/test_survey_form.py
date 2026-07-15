# 08DEC2025
# Survey Form Creation and Testing
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from locobuzz_login.CX_login import locobuzzLogin
from elements.survey_form_page import SurveyFormElements
from elements.accountSettings_page import AccountSettingsPageElements
from utils.credentials import get_sa_creds


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/survey"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


@pytest.mark.selenium
def test_survey_form_creation():
    test_name = "survey_form_creation"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLogin(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Survey Form workflow...")
    
        # Navigate to Account Settings
        profile_menu = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.PROFILE_MENU)))
        safe_click(profile_menu)
        
        account_settings = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.ACCOUNT_SETTINGS)))
        safe_click(account_settings)
        time.sleep(2)

        # Search for keywords
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, AccountSettingsPageElements.SEARCH_FIELD)))
        safe_click(search_field)
        search_field.send_keys("survey form")
        time.sleep(1)

        # Click Survey Form link
        print("Clicking Survey Form link...")
        survey_form_link = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.SURVEY_FORM_LINK)))
        safe_click(survey_form_link)
        time.sleep(2)

        # Select Brand - Click dropdown
        print("Selecting brand...")
        brand_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.BRAND_DROPDOWN)))
        safe_click(brand_dropdown)
        time.sleep(1)

        # Select "Juws" brand
        print("Selecting Juws brand...")
        juws_option = wait.until(EC.element_to_be_clickable((By.XPATH, AccountSettingsPageElements.JUWS_BRAND_OPTION)))
        safe_click(juws_option)
        time.sleep(1)

        # Click Create New Form button
        print("Clicking Create New Form...")
        create_form_btn = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.CREATE_NEW_FORM_BUTTON)))
        safe_click(create_form_btn)
        time.sleep(2)

        # Click first image
        print("Clicking first image...")
        first_image = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.FIRST_IMAGE)))
        safe_click(first_image)
        time.sleep(1)

        # Click and edit form title
        print("Editing form title...")
        form_title = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.UNTITLED_FORM_TEXT)))
        safe_click(form_title)
        time.sleep(0.5)
        
        title_input = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.UNTITLED_FORM_TEXT)))
        title_input.clear()
        title_input.send_keys("Survey Form Testing")
        time.sleep(1)

        # Locate the drop zone
        print("Locating drop zone...")
        drop_zone = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'form-container')]//div[@dnddropzone])[2]")))

        # Drag and drop Rating elements into the form
        print("Dragging and dropping Rating elements...")
        rating_elements = driver.find_elements(By.XPATH, SurveyFormElements.RATING_TEXT)
        
        actions = ActionChains(driver)
        for i, rating_element in enumerate(rating_elements, 1):
            print(f"Dragging Rating element {i}...")
            # Scroll the element into view
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", rating_element)
            time.sleep(0.5)
            
            # Perform drag and drop
            actions.drag_and_drop(rating_element, drop_zone).perform()
            time.sleep(1)

        # Click Rating element
        print("Clicking Rating element...")
        rating_element = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.RATING_TEXT)))
        safe_click(rating_element)
        time.sleep(1)

        # Edit first rating label
        print("Editing first rating label...")
        rating_input = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.RATING_LABEL_INPUT)))
        safe_click(rating_input)
        rating_input.send_keys(Keys.CONTROL + "a")
        rating_input.send_keys("testing 1")
        time.sleep(1)

        # Select dropdown option 3
        print("Selecting rating scale...")
        rating_dropdown_elem = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.RATING_DROPDOWN)))
        dropdown = Select(rating_dropdown_elem)
        dropdown.select_by_value("3")
        time.sleep(1)
        
        # Locate the drop zone
        print("Locating drop zone...")
        drop_zone = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'form-container')]//div[@dnddropzone])[2]")))

        # Drag and drop Rating elements into the form
        print("Dragging and dropping Rating elements...")
        rating_elements = driver.find_elements(By.XPATH, SurveyFormElements.RATING_TEXT)
        
        actions = ActionChains(driver)
        for i, rating_element in enumerate(rating_elements, 1):
            print(f"Dragging Rating element {i}...")
            # Scroll the element into view
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", rating_element)
            time.sleep(0.5)
            
            # Perform drag and drop
            actions.drag_and_drop(rating_element, drop_zone).perform()
            time.sleep(1)

        # # Click Rating again
        # print("Clicking Rating span...")
        # rating_span = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.RATING_TEXT)))
        # safe_click(rating_span)
        # time.sleep(1)

        # Edit rating question text
        print("Editing rating question...")
        question_text = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.RATING_QUESTION_TEXT)))
        safe_click(question_text)
        question_text.send_keys(Keys.CONTROL + "a")
        question_text.send_keys("testing 2")
        time.sleep(1)

        # Click Rating in Current Element
        print("Clicking Rating in Current Element...")
        rating_current = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()=' Rating ']")))
        safe_click(rating_current)
        time.sleep(1)

        # Locate the drop zone
        print("Locating drop zone...")
        drop_zone = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'form-container')]//div[@dnddropzone])[2]")))

        # Drag and drop Rating elements into the form
        print("Dragging and dropping Rating elements...")
        rating_elements = driver.find_elements(By.XPATH, SurveyFormElements.RATING_TEXT)
        
        actions = ActionChains(driver)
        for i, rating_element in enumerate(rating_elements, 1):
            print(f"Dragging Rating element {i}...")
            # Scroll the element into view
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", rating_element)
            time.sleep(0.5)
            
            # Perform drag and drop
            actions.drag_and_drop(rating_element, drop_zone).perform()
            time.sleep(1)

        # Click and edit another rating question
        print("Editing another rating question...")
        question_text2 = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.RATING_QUESTION_TEXT)))
        safe_click(question_text2)
        question_text2.send_keys(Keys.CONTROL + "a")
        question_text2.send_keys("testing 3")
        time.sleep(1)

        # Click NPS
        print("Clicking NPS...")
        nps_element = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.NPS_TEXT)))
        safe_click(nps_element)
        time.sleep(1)

        # Click Preview button
        print("Clicking Preview button...")
        preview_btn = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.PREVIEW_BUTTON)))
        safe_click(preview_btn)
        time.sleep(2)

        # Close preview
        print("Closing preview...")
        close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.CLOSE_BUTTON)))
        safe_click(close_btn)
        time.sleep(1)

        # Click Update Form button
        print("Clicking Update Form button...")
        update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.UPDATE_FORM_BUTTON)))
        safe_click(update_btn)
        time.sleep(2)

        # Verify success message is displayed
        print("Verifying form creation success message...")
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Form created successfully.']")))
        assert success_message.is_displayed(), "Success message 'Form created successfully.' not displayed"
        print("✓ Success message verified: 'Form created successfully.'")
        time.sleep(1)

        # Click Copy button
        print("Clicking Copy button...")
        copy_btn = wait.until(EC.element_to_be_clickable((By.XPATH, SurveyFormElements.COPY_BUTTON)))
        safe_click(copy_btn)
        time.sleep(2)

        # Verify copy message is displayed
        print("Verifying form copy message...")
        copy_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Form URL  copied successfully']")))
        assert copy_message.is_displayed(), "Success message 'Form URL copied successfully' not displayed"
        print("✓ Success message verified: 'Form URL copied successfully'")
        time.sleep(1)

        # Get the survey form URL from the DOM (avoiding clipboard permission issues)
        print("Getting survey form URL from DOM...")
        
        # Try to find the URL in input fields or link elements
        survey_url = None
        try:
            # Look for input field or text element containing the survey URL
            url_elements = driver.find_elements(By.XPATH, "//input[contains(@value, 'surveyform') or contains(@value, 'survey')] | //a[contains(@href, 'surveyform')] | //*[contains(text(), 'http') and contains(text(), 'surveyform')]")
            for element in url_elements:
                url = element.get_attribute('value') or element.get_attribute('href') or element.text
                if url and 'http' in url and 'surveyform' in url:
                    survey_url = url.strip()
                    break
        except Exception as e:
            print(f"Could not find URL in DOM: {e}")
        
        # If not found in DOM, try to simulate Ctrl+V to get from clipboard
        if not survey_url:
            print("URL not found in DOM, using keyboard paste method...")
            # Open new tab first
            driver.execute_script("window.open('about:blank');")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            
            # Focus on address bar and paste
            driver.execute_script("document.body.innerHTML = '<input id=\"urlInput\" type=\"text\" style=\"width:100%;padding:20px;font-size:16px;\">';")
            url_input = driver.find_element(By.ID, "urlInput")
            url_input.click()
            url_input.send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            survey_url = url_input.get_attribute('value')
        
        print(f"Survey URL: {survey_url}")
        
        # Validate URL
        if not survey_url or not survey_url.startswith('http'):
            raise Exception(f"Invalid survey URL retrieved: {survey_url}")
        
        # If we haven't opened a new tab yet, do it now
        if len(driver.window_handles) == 1:
            driver.execute_script("window.open('');")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
        
        # Navigate to the survey form URL
        driver.get(survey_url)
        print(f"Navigated to survey form in new tab")
        
        time.sleep(3)
        
        # Verify the form is visible
        print("Verifying survey form is visible...")
        form_container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'form-container') or contains(@class, 'survey-form')]")))
        
        if form_container.is_displayed():
            print("✅ Survey form is visible and loaded successfully")
        else:
            print("❌ Survey form is not visible")
            
        # Verify form title
        try:
            form_title_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Survey Form Testing')]")
            if form_title_element.is_displayed():
                print("✅ Form title 'Survey Form Testing' is visible")
        except:
            print("⚠️ Could not verify form title")

        print("✅ Survey Form creation workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after Survey Form workflow")
