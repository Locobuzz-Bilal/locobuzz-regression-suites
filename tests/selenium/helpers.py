from playwright.sync_api import Page
import time

def login_and_search_ticket(page: Page, username: str, password: str, ticket_id: str):
    print("🔹 Waiting for login page to load...")
    page.wait_for_load_state("networkidle")

    # --- USERNAME ---
    username_locator = page.locator("input[formcontrolname='username'], input[name='username']")
    username_locator.wait_for(state="visible", timeout=15000)

    if username_locator.get_attribute("readonly") == "true":
        print("⚠️ Username field is readonly, skipping fill.")
    else:
        username_locator.fill(username)
        print("✅ Username filled")

    # --- PASSWORD ---
    password_locator = page.locator("input[type='password']")
    password_locator.wait_for(state="visible", timeout=15000)
    password_locator.fill(password)
    print("✅ Password filled")

    # --- LOGIN BUTTON ---
    login_button = page.get_by_role("button", name="Login")
    login_button.wait_for(state="visible", timeout=10000)
    login_button.click()
    print("🚀 Clicked Login button")

    # --- Wait for redirect or dashboard load ---
    try:
        page.wait_for_url("**/dashboard", timeout=20000)
        print("✅ Login successful — Dashboard loaded")
    except:
        print("⚠️ Dashboard not detected yet, maybe OTP or redirect page")

    # --- Search for ticket if dashboard opened ---
    if "dashboard" in page.url or "cx.locobuzz.com" in page.url:
        print(f"🔍 Searching for Ticket ID: {ticket_id}")
        search_box = page.locator("input[placeholder*='Search']")
        search_box.wait_for(state="visible", timeout=10000)
        search_box.fill(ticket_id)
        page.keyboard.press("Enter")
        time.sleep(3)
        print("✅ Ticket search complete")
    else:
        print("❌ Could not reach dashboard, skipping ticket search")
