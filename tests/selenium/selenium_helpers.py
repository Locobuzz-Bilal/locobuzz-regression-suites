from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def safe_click(driver, wait, locator, timeout=20):
    wait.until(EC.element_to_be_clickable(locator)).click()

def safe_fill(driver, wait, locator, text, timeout=20):
    element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
    element.clear()
    element.send_keys(text)

def wait_for_element(driver, wait, locator, timeout=20):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
