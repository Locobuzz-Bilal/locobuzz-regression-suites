import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


def capture_full_page_screenshot(driver, filename):
    """Capture full-page screenshot using Chrome DevTools Protocol - maintains viewport width"""
    # Use CDP to get full page screenshot with original layout
    screenshot_data = driver.execute_cdp_cmd('Page.captureScreenshot', {
        'format': 'png',
        'captureBeyondViewport': True
    })
    
    # Decode and save
    import base64
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(screenshot_data['data']))
    
    print(f"📸 Full-page screenshot saved: {filename}")
    return filename


def convert_png_to_searchable_pdf_no_cuts(png_path, pdf_path):
    """Convert PNG to searchable PDF using Tesseract's built-in PDF generator (NO CUTS + PERFECT TEXT ALIGNMENT)"""
    try:
        from PIL import Image
        import pytesseract
        
        # Set Tesseract path
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        print("📄 Creating searchable PDF with perfect text alignment...")
        print("🔍 Running OCR (this takes time for large images)...")
        
        # Open image
        img = Image.open(png_path)
        
        # Use Tesseract's built-in PDF generator - it creates properly aligned text layer
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
        
        # Save PDF
        with open(pdf_path, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ Searchable PDF created: {pdf_path}")
        print("📋 NO PAGE BREAKS + Text perfectly aligned and copyable!")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


@pytest.mark.selenium
def test_check():
    """Test full-page screenshot on Apple website"""
    driver = None

    try:
        print("🌐 Opening Chrome browser...")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use Chrome directly (no webdriver-manager)
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        
        print("Loading Apple website...")
        driver.get("https://www.apple.com/")
        time.sleep(3)  # Let page load completely
        
        # Close any popups/banners (like country selector)
        try:
            driver.execute_script("""
                // Close any modal/overlay elements
                var closeButtons = document.querySelectorAll('button[aria-label*="close"], button.close, .modal-close');
                closeButtons.forEach(btn => btn.click());
            """)
        except:
            pass
        
        # Create screenshots directory
        screenshots_dir = "tests/screenshots/test"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Force scroll to absolute top and wait for any animations
        driver.execute_script("window.scrollTo(0, 0); document.documentElement.scrollTop = 0; document.body.scrollTop = 0;")
        time.sleep(1.5)
        
        # Take full-page screenshot
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshots_dir, f"apple_fullpage_{timestamp}.png")
        capture_full_page_screenshot(driver, screenshot_path)
        
        # Create PDF - disable links
        print("📄 Creating PDF with copyable text...")
        pdf_path = os.path.join(screenshots_dir, f"apple_fullpage_{timestamp}.pdf")
        import base64
        
        driver.execute_script("""
            var links = document.querySelectorAll('a');
            links.forEach(link => link.removeAttribute('href'));
        """)
        
        result = driver.execute_cdp_cmd('Page.printToPDF', {
            'printBackground': True,
            'displayHeaderFooter': False,
            'paperWidth': 8.27,
            'paperHeight': 100,
            'marginTop': 0,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,
            'scale': 1.0
        })
        
        with open(pdf_path, 'wb') as f:
            f.write(base64.b64decode(result['data']))
        
        print(f"✅ PDF created - all text is copyable!")
        
        print("✅ Files created!")
        print(f"📂 PNG: {screenshot_path}")
        print(f"📂 PDF: {pdf_path}")
        print("💯 PDF has NO clickable links - just copy text!")
        
        # Keep browser open for 5 seconds to see results
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error: {e}")
        pytest.fail(f"Test failed: {e}")

    finally:
        if driver:
            driver.quit() bilal shaikh f
        print("🧹 Browser closed")
