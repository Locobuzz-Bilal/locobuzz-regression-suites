from playwright.sync_api import Playwright, sync_playwright, TimeoutError

def run(playwright: Playwright) -> None:
    print("🌐 Opening Locobuzz login page...")
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(viewport=None)  # Use native window size
    page = context.new_page()

    try:
        page.goto("https://cx.locobuzz.com/login")
        # ---- LOGIN ----
        username_input = page.locator('input[formcontrolname="username"]')
        username_input.fill("juw_agent")
        print("✅ Username entered")

        continue_btn = page.get_by_role("button", name="Continue")
        continue_btn.click()
        print("✅ Continue clicked")

        # Password
        password_input = page.locator('input[formcontrolname="password"]')
        password_input.fill("Buzz@1234")
        print("✅ Password entered")

        login_btn = page.get_by_role("button", name="Login")
        login_btn.click()
        print("✅ Login clicked")
        print("🎉 Logged in successfully!")

        # ---- SELECT ALL & SUBMIT ----
        select_all = page.get_by_text("Select all")
        select_all.click()
        print("✅ 'Select All' clicked")

        submit_btn = page.locator('//span[text()=" Submit "]')
        submit_btn.click()
        print("✅ 'Submit' clicked")

        # ---- SEARCH TICKET ----
        search_btn = page.locator('a').filter(has_text="search")
        search_btn.click()
        print("✅ Search button clicked")

        search_input = page.locator('input[placeholder*="Search for a Ticket ID"]')
        search_input.fill("262082")
        print("✅ Ticket ID entered")

        search_btn.click()
        print("✅ Search executed")

        # ---- REPLY ----
        reply_btn = page.locator('//span[text()="Reply"]')
        reply_btn.click()
        print("✅ Reply clicked")

        # ---- REPLY TYPE ----
        reply_type_dropdown = page.locator('//mat-label[text()="Reply Type"]/ancestor::mat-form-field//mat-select')
        reply_type_dropdown.click()
        print("✅ Reply Type dropdown clicked")

        reply_assign_option = page.get_by_role("option", name="Reply & Assign")
        reply_assign_option.click()
        print("✅ Reply & Assign selected")

        # ---- WRITE REPLY ----
        write_reply = page.locator('textarea[placeholder="Write Reply"]')
        write_reply.fill("This is a reply and assign test")
        print("✅ Write Reply entered")

        # ---- NEXT BUTTON ----
        next_btn = page.locator('//span[text()=" Next "]')
        next_btn.click()
        print("✅ Next clicked")

        # ---- SELECT USER ----
        user_dropdown = page.locator('(//input[@type="text"])[3]')
        user_dropdown.click()
        juw_agent_option = page.get_by_text("Juwairia Agent")
        juw_agent_option.click()
        print("✅ User selected")

        # ---- ADD NOTE ----
        add_note = page.locator('(//textarea[@formcontrolname="replyEscalateNote"])[2]')
        add_note.fill("Assigning to Juwairia Agent")
        print("✅ Note added")

        # ---- SEND ----
        send_btn = page.locator('//span[text()=" Send "]')
        send_btn.click()
        print("✅ Send clicked")

        print("🎉 Workflow completed successfully!")

    except TimeoutError as e:
        print(f"⚠️ Timeout or error: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
    finally:
        context.close()
        browser.close()


with sync_playwright() as playwright:
    run(playwright)
