# # perfect code for stitching full-page screenshots and converting to searchable PDF
# import pytest
# import time
# import os
# import base64
# from PIL import Image
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import pytesseract


# def scroll_and_stitch_fullpage(driver, output_path="fullpage_stitched.png", scroll_pause=1):
#     """Scrolls page viewport-by-viewport, takes screenshots, and stitches them perfectly."""
#     total_height = driver.execute_script("return document.body.scrollHeight")
#     viewport_height = driver.execute_script("return window.innerHeight")

#     print(f"📏 Total page height: {total_height}px | Viewport: {viewport_height}px")

#     stitched_image = None
#     temp_files = []

#     scroll_y = 0
#     part = 0

#     while scroll_y < total_height:
#         driver.execute_script(f"window.scrollTo(0, {scroll_y});")
#         time.sleep(scroll_pause)

#         part_file = f"temp_part_{part}.png"
#         driver.save_screenshot(part_file)
#         temp_files.append(part_file)
#         part += 1

#         scroll_y += viewport_height

#     # Stitch vertically
#     print("🧵 Stitching screenshots...")
#     imgs = [Image.open(x) for x in temp_files]
#     widths, heights = zip(*(i.size for i in imgs))

#     total_height = sum(heights)
#     max_width = max(widths)
#     stitched_image = Image.new('RGB', (max_width, total_height))

#     y_offset = 0
#     for im in imgs:
#         stitched_image.paste(im, (0, y_offset))
#         y_offset += im.height

#     stitched_image.save(output_path)

#     # cleanup temp
#     for f in temp_files:
#         os.remove(f)

#     print(f"✅ Full stitched image saved: {output_path}")
#     return output_path


# def convert_to_searchable_pdf(image_path, pdf_path):
#     """Converts PNG to searchable PDF using Tesseract (clear, aligned, copyable text)."""
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#     print("📄 Running OCR to create searchable PDF...")
#     img = Image.open(image_path)
#     pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
#     with open(pdf_path, 'wb') as f:
#         f.write(pdf_bytes)
#     print(f"✅ Searchable PDF created: {pdf_path}")


# @pytest.mark.selenium
# def test_fullpage_pdf():
#     driver = None
#     try:
#         print("🌐 Opening Chrome...")

#         chrome_options = Options()
#         chrome_options.add_argument("--start-maximized")
#         chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#         chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         chrome_options.add_experimental_option("useAutomationExtension", False)

#         driver = webdriver.Chrome(options=chrome_options)
#         driver.maximize_window()

#         # 🔐 Go to product login page (replace URL below)
#         driver.get("https://www.apple.com/")
#         time.sleep(3)

#         # 🚫 Remove sticky headers/footers for clean capture
#         driver.execute_script("""
#             var elems = document.querySelectorAll('*');
#             elems.forEach(el => {
#                 if (getComputedStyle(el).position === 'sticky' || getComputedStyle(el).position === 'fixed') {
#                     el.style.position = 'static';
#                 }
#             });
#         """)

#         # 📂 Output dir
#         output_dir = "tests/screenshots/test"
#         os.makedirs(output_dir, exist_ok=True)

#         timestamp = time.strftime("%Y%m%d_%H%M%S")
#         stitched_path = os.path.join(output_dir, f"stitched_{timestamp}.png")
#         pdf_path = os.path.join(output_dir, f"stitched_{timestamp}.pdf")

#         # 📸 Scroll + stitch
#         scroll_and_stitch_fullpage(driver, stitched_path)

#         # 🧾 Convert to searchable PDF
#         convert_to_searchable_pdf(stitched_path, pdf_path)

#         print("\n✅ All done!")
#         print(f"🖼️ PNG: {stitched_path}")
#         print(f"📄 PDF: {pdf_path}")
#         time.sleep(3)

#     except Exception as e:
#         print(f"❌ Error: {e}")
#         pytest.fail(str(e))

#     finally:
#         if driver:
#             driver.quit()
#         print("🧹 Browser closed.")




# import pytest
# import time
# import os
# from PIL import Image
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pytesseract


# # ---------------------------------------------------------------------
# # 1️⃣  Scroll + Stitch Function
# # ---------------------------------------------------------------------
# def scroll_and_stitch_fullpage(driver, output_path="fullpage_stitched.png", scroll_pause=1):
#     """Scrolls viewport-by-viewport, takes screenshots, and stitches them perfectly."""
#     total_height = driver.execute_script("return document.body.scrollHeight")
#     viewport_height = driver.execute_script("return window.innerHeight")
#     print(f"📏 Total height: {total_height}px | Viewport: {viewport_height}px")

#     temp_files = []
#     scroll_y = 0
#     part = 0

#     while scroll_y < total_height:
#         driver.execute_script(f"window.scrollTo(0, {scroll_y});")
#         time.sleep(scroll_pause)
#         part_file = f"temp_part_{part}.png"
#         driver.save_screenshot(part_file)
#         temp_files.append(part_file)
#         part += 1
#         scroll_y += viewport_height

#     print("🧵 Stitching screenshots...")
#     imgs = [Image.open(x) for x in temp_files]
#     widths, heights = zip(*(i.size for i in imgs))
#     stitched_image = Image.new("RGB", (max(widths), sum(heights)))
#     y_offset = 0
#     for im in imgs:
#         stitched_image.paste(im, (0, y_offset))
#         y_offset += im.height
#     stitched_image.save(output_path)

#     # cleanup temp
#     for f in temp_files:
#         os.remove(f)

#     print(f"✅ Full stitched image saved: {output_path}")
#     return output_path


# # ---------------------------------------------------------------------
# # 2️⃣  Convert to Searchable PDF (Color + Copyable Text)
# # ---------------------------------------------------------------------
# def convert_to_searchable_pdf(image_path, pdf_path):
#     """Converts PNG to searchable PDF using Tesseract (clear, aligned, copyable text)."""
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#     print("📄 Running OCR to create searchable PDF...")
#     img = Image.open(image_path)
#     pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
#     with open(pdf_path, 'wb') as f:
#         f.write(pdf_bytes)
#     print(f"✅ Searchable PDF created: {pdf_path}")
#     return pdf_path


# # ---------------------------------------------------------------------
# # 3️⃣  Main Test: Login → Analytics Dashboard → Capture
# # ---------------------------------------------------------------------
# @pytest.mark.selenium
# def test_newzverse_fullpage_pdf():
#     driver = None
#     try:
#         print("🌐 Launching Chrome...")

#         chrome_options = Options()
#         chrome_options.add_argument("--start-maximized")
#         chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#         chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         chrome_options.add_experimental_option("useAutomationExtension", False)

#         driver = webdriver.Chrome(options=chrome_options)
#         driver.maximize_window()

#         # -------------------------------------------------------
#         # 1️⃣ LOGIN TO NEWZVERSE
#         # -------------------------------------------------------
#         driver.get("https://app.newzverse.ai/sign-in")
#         wait = WebDriverWait(driver, 20)

#         # Enter Email
#         email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
#         email_input.send_keys("asawari.pawar@locobuzz.com")  # 🔁 replace with actual email

#         # Enter Password
#         password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
#         password_input.send_keys("Crazy2025#")  # 🔁 replace with actual password

#         # Click Login Button
#         login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space(text())='Log In']]")))
#         login_btn.click()
#         print("✅ Logged in successfully!")

#         # Wait for dashboard/homepage
#         wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#         time.sleep(5)

#         # -------------------------------------------------------
#         # 2️⃣ NAVIGATE TO ANALYTICS DASHBOARD
#         # -------------------------------------------------------
#         print("📊 Navigating to Analytics Dashboard...")
#         analytics_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class,'sidebar-menu-item')]//span[normalize-space(text())='Analytics']")))
#         analytics_btn.click()

#         # Wait for Analytics page to fully load
#         wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#         time.sleep(6)
#         print("✅ Analytics Dashboard loaded!")

#         # Flatten sticky elements for clean capture
#         driver.execute_script("""
#             document.querySelectorAll('*').forEach(el => {
#                 const s = getComputedStyle(el);
#                 if (s.position === 'sticky' || s.position === 'fixed') el.style.position = 'static';
#             });
#         """)

#         # -------------------------------------------------------
#         # 3️⃣ CAPTURE SCREENSHOT + PDF
#         # -------------------------------------------------------
#         output_dir = "tests/screenshots/test"
#         os.makedirs(output_dir, exist_ok=True)
#         timestamp = time.strftime("%Y%m%d_%H%M%S")

#         stitched_path = os.path.join(output_dir, f"newzverse_fullpage_{timestamp}.png")
#         pdf_path = os.path.join(output_dir, f"newzverse_fullpage_{timestamp}.pdf")

#         scroll_and_stitch_fullpage(driver, stitched_path)
#         convert_to_searchable_pdf(stitched_path, pdf_path)

#         print("\n🎉 Capture complete!")
#         print(f"🖼️ Screenshot: {stitched_path}")
#         print(f"📄 PDF: {pdf_path}")

#         time.sleep(2)

#     except Exception as e:
#         print(f"❌ Error: {e}")
#         pytest.fail(str(e))
#     finally:
#         if driver:
#             driver.quit()
#         print("🧹 Browser closed.")



import pytest
import time
import os
import base64
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract


def wait_for_full_load(driver, extra_wait=5):
    """Wait until the page is fully loaded + small buffer."""
    WebDriverWait(driver, 40).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    time.sleep(extra_wait)
    print("✅ Page fully loaded and stable.")


def scroll_and_stitch_fullpage(driver, output_path="fullpage_stitched.png", scroll_pause=1):
    """Scrolls page viewport-by-viewport, takes screenshots, and stitches them perfectly."""
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    print(f"📏 Total height: {total_height}px | Viewport: {viewport_height}px")

    temp_files = []
    scroll_y = 0
    part = 0

    while scroll_y < total_height:
        driver.execute_script(f"window.scrollTo(0, {scroll_y});")
        time.sleep(scroll_pause)

        part_file = f"temp_part_{part}.png"
        driver.save_screenshot(part_file)
        temp_files.append(part_file)
        part += 1
        scroll_y += viewport_height

    print("🧵 Stitching screenshots...")
    imgs = [Image.open(x) for x in temp_files]
    widths, heights = zip(*(i.size for i in imgs))

    total_height = sum(heights)
    max_width = max(widths)
    stitched_image = Image.new("RGB", (max_width, total_height))

    y_offset = 0
    for im in imgs:
        stitched_image.paste(im, (0, y_offset))
        y_offset += im.height

    stitched_image.save(output_path)

    # cleanup
    for f in temp_files:
        os.remove(f)

    print(f"✅ Full stitched image saved: {output_path}")
    return output_path


def convert_to_searchable_pdf(image_path, pdf_path):
    """Convert stitched PNG to searchable PDF with original look."""
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    print("📄 Converting stitched image to searchable PDF...")
    img = Image.open(image_path)
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"✅ Searchable PDF created: {pdf_path}")
    return pdf_path


@pytest.mark.selenium
def test_newzverse_scroll_stitch_pdf():
    driver = None
    try:
        print("🌐 Launching Chrome...")
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 30)

        # ------------------------------
        # LOGIN
        # ------------------------------
        driver.get("https://app.newzverse.ai/sign-in")
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("asawari.pawar@locobuzz.com")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("Crazy2025#")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[normalize-space(text())='Log In']]"))).click()
        wait_for_full_load(driver)

        # ------------------------------
        # NAVIGATE TO ANALYTICS DASHBOARD
        # ------------------------------
        analytics_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//li[contains(@class,'sidebar-menu-item')]//span[normalize-space(text())='Analytics']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", analytics_btn)
        analytics_btn.click()
        wait_for_full_load(driver)

        # ------------------------------
        # CLEAN STICKY HEADERS
        # ------------------------------
        driver.execute_script("""
            document.querySelectorAll('*').forEach(e=>{
                const s=getComputedStyle(e);
                if(s.position==='sticky'||s.position==='fixed'){e.style.position='static'}
            });
        """)

        # ------------------------------
        # OUTPUT PATHS
        # ------------------------------
        output_dir = "tests/screenshots/test"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        stitched_path = os.path.join(output_dir, f"newzverse_stitched_{timestamp}.png")
        pdf_path = os.path.join(output_dir, f"newzverse_stitched_{timestamp}.pdf")

        # ------------------------------
        # 1️⃣ SCROLL + STITCH PNG
        # ------------------------------
        scroll_and_stitch_fullpage(driver, stitched_path)

        # ------------------------------
        # 2️⃣ CONVERT TO SEARCHABLE PDF
        # ------------------------------
        convert_to_searchable_pdf(stitched_path, pdf_path)

        print("\n🎉 Done!")
        print(f"🖼️ Screenshot: {stitched_path}")
        print(f"📄 PDF: {pdf_path}")

    except Exception as e:
        print("❌ Error:", e)
        pytest.fail(str(e))
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed.")
