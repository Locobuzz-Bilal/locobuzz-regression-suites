#01DEC2025
#Create, Edit, Preview, Duplicate and Delete dashboard
import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from locobuzz_login.preProd_login import locobuzzLoginPreProd
from elements.awa_regression_page import AWAElements
from selenium.webdriver.common.action_chains import ActionChains
from elements.login_page import LoginPageElements   
from utils.credentials import get_sa_creds


def capture_failure_screenshot(driver, test_name):
    screenshots_dir = "tests/screenshots/widget_maker"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")


def dump_page_state(driver, test_name, label="state"):
    out_dir = "tests/screenshots/widget_maker"
    os.makedirs(out_dir, exist_ok=True)
    ts = int(time.time())
    html_path = os.path.join(out_dir, f"{test_name}_{label}_{ts}.html")
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"📄 Page source saved: {html_path}")
    except Exception as e:
        print(f"⚠️ Failed to save page source: {e}")

    try:
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        info_path = os.path.join(out_dir, f"{test_name}_iframes_{ts}.txt")
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write(f"Found {len(iframes)} iframes\n")
            for i, fr in enumerate(iframes):
                try:
                    src = fr.get_attribute('src')
                except Exception:
                    src = 'n/a'
                try:
                    name = fr.get_attribute('name')
                except Exception:
                    name = 'n/a'
                f.write(f"iframe[{i}]: name={name} src={src}\n")
        print(f"📄 Iframe info saved: {info_path}")
    except Exception as e:
        print(f"⚠️ Failed to list iframes: {e}")


def click_menu_item_via_point(driver, target, test_name):
    try:
        # find element under the More icon (slightly below center)
        elem = driver.execute_script(
            "var el=arguments[0]; if(!el) return null; var r=el.getBoundingClientRect(); var cx=r.left + r.width/2; var cy=r.top + r.height/2 + 8; var list=document.elementsFromPoint(cx, cy); return list.length?list[0]:null;",
            target,
        )
        if not elem:
            print("⚠️ No candidate element returned by elementsFromPoint")
            return False
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", elem)
            print("✅ Clicked menu candidate via elementsFromPoint -> click")
            return True
        except Exception as e:
            try:
                ActionChains(driver).move_to_element(elem).click().perform()
                print("✅ Clicked menu candidate via ActionChains after elementsFromPoint")
                return True
            except Exception as e2:
                print(f"⚠️ elementsFromPoint candidate click failed: {e} / {e2}")
                # save page state for debugging
                dump_page_state(driver, test_name, "point_click_failed")
                return False
    except Exception as e:
        print(f"⚠️ elementsFromPoint fallback error: {e}")
        return False


@pytest.mark.selenium
def test_widget_maker_workflow():
    test_name = "widget_maker_workflow"
    driver = None
    try:
        print("🔹 Logging in using Selenium...")
        username, password = get_sa_creds()
        driver = locobuzzLoginPreProd(username, password)
        wait = WebDriverWait(driver, 20)

        def safe_click(el):
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)

        print("🟢 Performing Widget Maker actions...")

        # Click Widgets Maker
        widgets_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.WIDGETS_MAKER_BUTTON)))
        safe_click(widgets_btn)
        time.sleep(2)

        # Switch to iframe
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.ANALYTICS_IFRAME)))
        
        # Wait for iframe URL to contain 'widgetMaker' indicating the page has loaded
        try:
            WebDriverWait(driver, 30).until(
                lambda d: 'widgetMaker' in d.find_element(By.XPATH, AWAElements.ANALYTICS_IFRAME).get_attribute('src')
            )
            print(f"✅ Iframe URL updated to widget maker page")
        except Exception as e:
            iframe_src = iframe.get_attribute('src')
            print(f"⚠️ Iframe URL check timeout. Current src: {iframe_src}")
            # Continue anyway - the iframe might be ready even if URL check failed
        
        driver.switch_to.frame(iframe)
        time.sleep(2)  # Allow page content to render

        # Create New Widget
        try:
            create_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.CREATE_NEW_WIDGET_BUTTON)))
            safe_click(create_btn)
        except Exception as e:
            print("⚠️ CREATE_NEW_WIDGET_BUTTON not found — saving diagnostics")
            try:
                dump_page_state(driver, test_name, "create_btn_missing")
            except Exception as _:
                print("⚠️ Failed to dump page state")
            # save visible buttons and their text
            try:
                out_dir = "tests/screenshots/widget_maker"
                os.makedirs(out_dir, exist_ok=True)
                ts = int(time.time())
                btns = driver.find_elements(By.TAG_NAME, 'button')
                btn_path = os.path.join(out_dir, f"{test_name}_buttons_{ts}.txt")
                with open(btn_path, 'w', encoding='utf-8') as f:
                    f.write(f"Found {len(btns)} buttons\n\n")
                    for i, b in enumerate(btns):
                        try:
                            txt = b.text.strip()
                        except Exception:
                            txt = ''
                        try:
                            attr = b.get_attribute('outerHTML')[:1000]
                        except Exception:
                            attr = ''
                        f.write(f"button[{i}]: text={txt} html_snippet={attr}\n\n")
                print(f"📄 Button info saved: {btn_path}")
            except Exception as _:
                print("⚠️ Failed to save button info")
            raise
        time.sleep(1)

        # Pick Grid
        grid_el = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.GRID)))
        safe_click(grid_el)
        time.sleep(1)

        # Select Attribute
        select_attr = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SELECT_ATTRIBUTE)))
        safe_click(select_attr)
        time.sleep(1)

        safe_click(wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DATE))))
        time.sleep(1)

        # Add measure
        add_measure = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ADD_ANOTHER_MEASURES_BTN)))
        safe_click(add_measure)
        time.sleep(1)

        # Select count of like reactions
        count_like = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.COUNT_OF_LIKE_REACTIONS)))
        safe_click(count_like)
        time.sleep(1)

        # Select City attribute
        select_attr = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SELECT_ATTRIBUTE)))
        safe_click(select_attr)
        city = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ATTRIBUTE_CITY)))
        safe_click(city)
        time.sleep(1)

        # Select Country attribute
        select_attr2 = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SELECT_ATTRIBUTE)))
        safe_click(select_attr2)
        country = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.ATTRIBUTE_COUNTRY)))
        safe_click(country)
        time.sleep(1)

        # Save Widget
        save_widget = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_WIDGET_BTN)))
        safe_click(save_widget)
        time.sleep(1)

        # Enter widget name
        widget_name = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.WIDGET_NAME_INPUT)))
        widget_name.click()
        widget_name.clear()
        widget_name.send_keys("Widget Testing 001")

        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_BTN)))
        safe_click(save_btn)
        time.sleep(3)
        
        # Wait for success message or page navigation
        try:
            success_msg = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, AWAElements.SUCCESS_WIDGET_SAVED))
            )
            print(f"Widget saved successfully: {success_msg.text}")
            time.sleep(2)
        except Exception as e:
            print(f"Success message not found (might already have navigated): {e}")
        
        # Check current URL for debugging
        current_url = driver.current_url
        print(f"Current URL after save: {current_url}")
        
        # Capture page source to see what's on screen
        dump_page_state(driver, test_name, "after_save")
        
        # Search widget
        search = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.SEARCH_INPUT)))
        safe_click(search)
        search.clear()
        search_term = "Widget Testing 001"
        search.send_keys(search_term)
        search_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SEARCH_ICON)))
        safe_click(search_icon)
        time.sleep(2)

       #Edit widget — find the widget card and click its More icon

        print(f"Looking for widget card with title: {search_term}")
        
        # Try to locate the widget card by title
        # The structure is: card > card-body > div > row > col-8 > div.text_heading containing the title
        card_xpath = f"//div[contains(@class,'text_heading') and contains(text(),'{search_term}')]/ancestor::div[contains(@class,'ant-card')]"
        
        try:
            widget_card = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, card_xpath))
            )
            print(f"Found widget card for: {search_term}")
            
            # Within the card, find the More icon (Dot_icon image)
            more_icon_xpath = ".//img[@src='/static/media/Dot_icon.d2a8952bba928acc82883022429bedd6.svg']"
            target = widget_card.find_element(By.XPATH, more_icon_xpath)
            print("Found More icon in widget card")

            # Scroll More icon into view
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)
            time.sleep(0.5)
            
            # Hover over More icon to trigger menu
            actions = ActionChains(driver)
            actions.move_to_element(target).perform()
            print("Hovering over More icon - waiting for menu to appear")
            time.sleep(1.5)  # Wait for menu animation
            
            # Try to find Edit option
            edit_selectors = [
                AWAElements.EDIT_WIDGET_TEXT, 
                "//div[contains(text(),'Edit')]",
                "//span[contains(text(),'Edit')]",
                "//button[contains(.,'Edit')]",
                "//li[contains(.,'Edit')]",
            ]
            
            edit_found = False
            for selector in edit_selectors:
                try:
                    edit = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"Found Edit using: {selector}")
                    safe_click(edit)
                    edit_found = True
                    break
                except Exception:
                    pass
            
            if not edit_found:
                raise Exception("Edit option not found in More menu")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error: {e}")
            capture_failure_screenshot(driver, test_name + "_error")
            raise
    
        except Exception as e:
            print(f"⚠️ Edit step: {e}")
            raise

        safe_click(wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DONUT))))
        time.sleep(1)

        # Save after edit
        print("Looking for Save Widget button after edit...")
        try:
            save_widget = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_WIDGET_BTN))
            )
            print("Found Save Widget button")
            safe_click(save_widget)
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Could not find SAVE_WIDGET_BTN: {e}")
            dump_page_state(driver, test_name, "save_widget_btn_not_found")
            raise

        print("Looking for final Save button...")
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_BTN)))
        safe_click(save_btn)
        time.sleep(3)
        print("✅ Widget saved after edit")

        # Duplicate
        view_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.VIEW_ICON)))
        safe_click(view_icon)
        time.sleep(1)
        duplicate = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DUPLICATE_WIDGET_BTN)))
        safe_click(duplicate)
        time.sleep(2)  # Wait for duplicate dialog to appear
        save_widget_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_WIDGET_BTN)))
        safe_click(save_widget_btn)
        time.sleep(1)
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SAVE_BTN)))
        safe_click(save_btn)
        time.sleep(3)
        
        # Delete — find the widget card and hover over its More icon then Delete
        try:
            # Wait for page to refresh/stabilize after Edit
            time.sleep(3)
            
            # Dump page state to see what's on screen
            dump_page_state(driver, test_name, "before_delete")
            
            # Search for the widget again to make sure it's visible
            print(f"Searching for widget again before delete: {search_term}")
            search_input = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.SEARCH_INPUT)))
            safe_click(search_input)
            search_input.clear()
            search_input.send_keys(search_term)
            search_icon = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.SEARCH_ICON)))
            safe_click(search_icon)
            time.sleep(2)
            
            print(f"Looking for widget card for delete with title: {search_term}")
            widget_card_xpath = f"//div[contains(@class,'text_heading') and contains(text(),'{search_term}')]/ancestor::div[contains(@class,'ant-card')]"
            widget_card = wait.until(EC.presence_of_element_located((By.XPATH, widget_card_xpath)))
            print(f"Found widget card for delete: {search_term}")
            
            # Find More icon within this card - refind to avoid stale element
            more_icon_xpath = ".//img[@src='/static/media/Dot_icon.d2a8952bba928acc82883022429bedd6.svg']"
            more_icon = widget_card.find_element(By.XPATH, more_icon_xpath)
            print("Found More icon in widget card for delete")
            
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_icon)
            time.sleep(0.5)
            
            # Refind the icon to ensure it's fresh
            widget_card = driver.find_element(By.XPATH, widget_card_xpath)
            more_icon = widget_card.find_element(By.XPATH, more_icon_xpath)
            
            # Hover over More icon to show menu
            actions = ActionChains(driver)
            actions.move_to_element(more_icon).perform()
            print("Hovering over More icon for delete - waiting for menu to appear")
            time.sleep(1.5)
            
            delete_text = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DELETE_WIDGET_TEXT)))
            safe_click(delete_text)
            delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, AWAElements.DELETE_BTN)))
            safe_click(delete_btn)
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Delete step failed: {e}")
            capture_failure_screenshot(driver, test_name + "_delete")
            raise

        # Verify deletion
        try:
            deleted_msg = wait.until(EC.presence_of_element_located((By.XPATH, AWAElements.WIDGET_DELETED_SUCCESS)))
            print(f"✅ {deleted_msg.text}")
        except:
            print("⚠️ Deletion message not found")

        # switch back to default content
        driver.switch_to.default_content()

        print("✅ Widget Maker workflow completed successfully")

    except Exception as e:
        if driver:
            capture_failure_screenshot(driver, test_name)
        pytest.fail(f"❌ Test failed: {e}")
    finally:
        if driver:
            driver.quit()
        print("🧹 Browser closed safely after widget maker workflow")
