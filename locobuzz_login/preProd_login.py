# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from elements.login_page import LoginPageElements

# def locobuzzLogin(username_value, password_value, headless=False):
#     """
#     Login to Locobuzz platform
    
#     Args:
#         username_value: Username for login
#         password_value: Password for login
#         headless: Run in headless mode (default: False - visible browser)
    
#     Returns:
#         WebDriver instance after successful login
#     """
#     options = Options()
#     if headless:
#         options.add_argument("--headless=new")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--window-size=1920,1080")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
    
#     # Use webdriver-manager to auto-download and manage ChromeDriver
#     service = ChromeService(ChromeDriverManager().install())
#     browser = webdriver.Chrome(service=service, options=options)
#     wait = WebDriverWait(browser, 15)
    
#     try:
#         browser.get(LoginPageElements.CX_URL)
#         if not headless:
#             browser.maximize_window()
        
#         # Username
#         username = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.USERNAME_INPUT)))
#         username.send_keys(username_value)
        
#         # Continue button
#         continueBtn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginPageElements.CONTINUE_BUTTON)))
#         continueBtn.click()
        
#         # Password
#         password = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.PASSWORD_INPUT)))
#         password.send_keys(password_value)
        
#         # Login button
#         loginBtn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginPageElements.LOGIN_BUTTON)))
#         loginBtn.click()
        
#         time.sleep(2)
#         return browser
        
#     except Exception as e:
#         print(f"Login error: {e}")
#         browser.quit()
#         raise

# if __name__ == "__main__":
#     # Test login
#     driver = locobuzzLogin("juwairiak", "yVhjecK9g@22", headless=False)
#     input("Press Enter to quit...")
#     driver.quit()


import os
import time
import platform
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from elements.login_page import LoginPageElements

# Load environment variables
load_dotenv()


def locobuzzLoginPreProd(username_value, password_value, headless=False):
    """
    Login to Locobuzz platform.
    
    Automatically detects:
        - Windows (local run)
        - Linux / AWS CodeBuild
    Uses:
        - webdriver-manager for Windows
        - system ChromeDriver (/usr/local/bin/chromedriver) on Linux/CodeBuild
    """

    options = Options()
    # Common stability flags
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--start-maximized")
    # Headless specific flags
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    
    # Use Selenium's built-in manager (more reliable than webdriver-manager)
    try:
        browser = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Chrome launch failed: {e}")
        raise

    wait = WebDriverWait(browser, 15)

    try:
        # -------- Open Login Page --------
        browser.get(LoginPageElements.PREPROD_URL)
        # Maximize can intermittently crash in some Chrome builds; make it best-effort.
        if not headless:
            try:
                browser.maximize_window()
            except Exception as mx_e:
                print(f"Warning: maximize_window failed: {mx_e}; proceeding without explicit maximize")
        
        # Username
        username = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.USERNAME_INPUT)))
        username.send_keys(username_value)

        continueBtn = wait.until(
            EC.element_to_be_clickable((By.XPATH, LoginPageElements.CONTINUE_BUTTON))
        )
        continueBtn.click()

        password = wait.until(
            EC.presence_of_element_located((By.XPATH, LoginPageElements.PASSWORD_INPUT))
        )
        password.send_keys(password_value)

        loginBtn = wait.until(
            EC.element_to_be_clickable((By.XPATH, LoginPageElements.LOGIN_BUTTON))
        )
        loginBtn.click()

        time.sleep(2)
        return browser

    except Exception as e:
        print(f"Login error: {e}")
        browser.quit()
        raise


if __name__ == "__main__":
    # LOCAL TEST (will use WebDriverManager + visible browser)
    driver = locobuzzLogin("juwairiak", "yVhjecK9g@22", headless=False)
    input("Press Enter to quit...")
    driver.quit()
