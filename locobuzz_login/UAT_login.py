import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from elements.login_page import LoginPageElements

def locobuzzLogin(username_value, password_value, headless=False):
    """
    Login to Locobuzz platform
    
    Args:
        username_value: Username for login
        password_value: Password for login
        headless: Run in headless mode (default: False - visible browser)
    
    Returns:
        WebDriver instance after successful login
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    
    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, 15)
    
    try:
        browser.get(LoginPageElements.UAT_URL)
        if not headless:
            browser.maximize_window()
        
        # Username
        username = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.USERNAME_INPUT)))
        username.send_keys(username_value)
        
        # Continue button
        continueBtn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginPageElements.CONTINUE_BUTTON)))
        continueBtn.click()
        
        # Password
        password = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.PASSWORD_INPUT)))
        password.send_keys(password_value)
        
        # Login button
        loginBtn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginPageElements.LOGIN_BUTTON)))
        loginBtn.click()
        
        time.sleep(2)
        return browser
        
    except Exception as e:
        print(f"Login error: {e}")
        browser.quit()
        raise

if __name__ == "__main__":
    # Test login
    driver = locobuzzLogin("juwairiak", "yVhjecK9g@22", headless=False)
    input("Press Enter to quit...")
    driver.quit()