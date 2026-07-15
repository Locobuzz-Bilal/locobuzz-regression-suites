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
import sys
import time
import platform
from pathlib import Path

# Add parent directory to path to allow imports when running directly
sys.path.insert(0, str(Path(__file__).parent.parent))

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


def locobuzzLogin(username_value, password_value, headless=False):
    """
    Login to Locobuzz platform.
    
    Automatically detects:
        - Windows (local run)
        - Linux / AWS CodeBuild
    Uses:
        - webdriver-manager for Windows
        - system ChromeDriver (/usr/local/bin/chromedriver) on Linux/CodeBuild
    """

    # Auto-detect CI/CD environment and force headless mode
    is_ci = os.getenv("CODEBUILD_BUILD_ID") or os.getenv("CI") or os.getenv("GITHUB_ACTIONS")
    if is_ci:
        headless = True
        print("🔧 CI/CD environment detected - forcing headless mode")

    options = Options()
    # Common stability flags
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Headless and Linux/Docker specific flags
    if headless or is_ci:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--window-size=1920,1080")
        print("🖥️  Running in headless mode with Linux/Docker optimizations")
    else:
        options.add_argument("--start-maximized")
        # Add more stability for visible mode
        options.add_argument("--disable-popup-blocking")
    
    # Use Selenium's built-in manager (more reliable than webdriver-manager)
    try:
        browser = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Chrome launch failed: {e}")
        raise

    wait = WebDriverWait(browser, 15)

    try:
        # -------- Open Login Page --------
        print(f"🌐 Loading URL: {LoginPageElements.CX_URL}")
        browser.get(LoginPageElements.CX_URL)
        
        # Wait for page to fully load
        time.sleep(3)
        
        # Maximize can intermittently crash in some Chrome builds; make it best-effort.
        if not headless:
            try:
                browser.maximize_window()
            except Exception as mx_e:
                print(f"Warning: maximize_window failed: {mx_e}; proceeding without explicit maximize")
        
        # Wait for login page to be ready
        print("⏳ Waiting for login page to load...")
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        
        # Username
        print("📝 Entering username...")
        username = wait.until(EC.presence_of_element_located((By.XPATH, LoginPageElements.USERNAME_INPUT)))
        username.send_keys(username_value)

        continueBtn = wait.until(
            EC.element_to_be_clickable((By.XPATH, LoginPageElements.CONTINUE_BUTTON))
        )
        continueBtn.click()
        time.sleep(2)

        print("🔐 Entering password...")
        password = wait.until(
            EC.presence_of_element_located((By.XPATH, LoginPageElements.PASSWORD_INPUT))
        )
        password.send_keys(password_value)

        loginBtn = wait.until(
            EC.element_to_be_clickable((By.XPATH, LoginPageElements.LOGIN_BUTTON))
        )
        loginBtn.click()

        # Wait longer for dashboard to fully load after login
        print("⏳ Waiting for dashboard to load...")
        time.sleep(5)
        print("✅ Login successful!")
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
