# # tests/conftest.py

# import os
# import time
# import pytest
# from pathlib import Path

# SCREENSHOTS_DIR = Path("screenshots")
# SCREENSHOTS_DIR.mkdir(exist_ok=True)

# def _capture_selenium_screenshot(driver, nodeid):
#     screenshot_path = SCREENSHOTS_DIR / f"{nodeid.replace('::', '_')}_{int(time.time())}.png"
#     driver.save_screenshot(str(screenshot_path))
#     return str(screenshot_path)

# def _capture_playwright_screenshot(page, nodeid):
#     screenshot_path = SCREENSHOTS_DIR / f"{nodeid.replace('::', '_')}_{int(time.time())}.png"
#     page.screenshot(path=str(screenshot_path), full_page=True)
#     return str(screenshot_path)

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # Run all other hooks to obtain report object
#     outcome = yield
#     rep = outcome.get_result()

#     # We only look at the call phase of a test
#     if rep.when == "call" and rep.failed:
#         # Attempt Selenium driver
#         driver = getattr(item.instance, "browser", None)
#         if driver:
#             path = _capture_selenium_screenshot(driver, item.nodeid)
#             extra = getattr(rep, "extra", [])
#             rep.extra = extra + [{'name': 'Screenshot', 'mime_type': 'image/png', 'path': path}]

#         # Attempt Playwright page
#         page = getattr(item.instance, "page", None)
#         if page:
#             path = _capture_playwright_screenshot(page, item.nodeid)
#             extra = getattr(rep, "extra", [])
#             rep.extra = extra + [{'name': 'Screenshot', 'mime_type': 'image/png', 'path': path}]

#         # If neither available, fallback or do nothing

# @pytest.fixture(scope="function")
# def browser():
#     # Setup Selenium WebDriver or Playwright browser instance fixture here if needed
#     # User should manage actual initialization in tests for maximum flexibility
#     # This fixture just provided as placeholder to share browser instance with conftest hooks
#     driver = None
#     yield driver
#     # Teardown driver here if initialized

# @pytest.fixture(scope="function")
# def page():
#     # Similarly, placeholder Playwright 'page' fixture
#     p = None
#     yield p
#     # Teardown page here if initialized
















#20OCT25

# import time
# from pathlib import Path
# import pytest

# # Folder for screenshots
# SCREENSHOTS_DIR = Path("screenshots")
# SCREENSHOTS_DIR.mkdir(exist_ok=True)

# def _capture_selenium_screenshot(driver, nodeid):
#     path = SCREENSHOTS_DIR / f"{nodeid.replace('::','_')}_{int(time.time())}.png"
#     driver.save_screenshot(str(path))
#     return str(path)

# def _capture_playwright_screenshot(page, nodeid):
#     path = SCREENSHOTS_DIR / f"{nodeid.replace('::','_')}_{int(time.time())}.png"
#     page.screenshot(path=str(path), full_page=True)
#     return str(path)

# # Hook to capture screenshots on test failure
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()

#     if rep.when == "call" and rep.failed:
#         # Selenium driver attached to test function
#         driver = getattr(item.instance, "browser", None)
#         if driver:
#             path = _capture_selenium_screenshot(driver, item.nodeid)
#             print(f"📸 Selenium screenshot captured: {path}")

#         # Playwright page attached to test function
#         page = getattr(item.instance, "page", None)
#         if page:
#             path = _capture_playwright_screenshot(page, item.nodeid)
#             print(f"📸 Playwright screenshot captured: {path}")

#22OCT25
# import time
# from pathlib import Path
# import pytest

# # Folder for screenshots
# SCREENSHOTS_DIR = Path("screenshots")
# SCREENSHOTS_DIR.mkdir(exist_ok=True)

# def capture_selenium_screenshot(driver, nodeid, step_name="step"):
#     timestamp = int(time.time())
#     filename = f"{nodeid.replace('::','_')}_{step_name}_{timestamp}.png"
#     path = SCREENSHOTS_DIR / filename
#     driver.save_screenshot(str(path))
#     print(f"\n📸 Screenshot ({step_name}): file://{path}\n")
#     return str(path)

# def capture_playwright_screenshot(page, nodeid, step_name="step"):
#     timestamp = int(time.time())
#     filename = f"{nodeid.replace('::','_')}_{step_name}_{timestamp}.png"
#     path = SCREENSHOTS_DIR / filename
#     page.screenshot(path=str(path), full_page=True)
#     print(f"\n📸 Screenshot ({step_name}): file://{path}\n")
#     return str(path)

# # Hook to capture screenshots on test failure
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()

#     if rep.when == "call" and rep.failed:
#         # Selenium driver attached to test function
#         driver = getattr(item.instance, "browser", None)
#         if driver:
#             path = capture_selenium_screenshot(driver, item.nodeid, "FAILURE")
#             print(f"❌ Test failed: {rep.longreprtext.splitlines()[-1]}")
#             print(f"   Screenshot link: file://{path}")

#         # Playwright page attached to test function
#         page = getattr(item.instance, "page", None)
#         if page:
#             path = capture_playwright_screenshot(page, item.nodeid, "FAILURE")
#             print(f"❌ Test failed: {rep.longreprtext.splitlines()[-1]}")
#             print(f"   Screenshot link: file://{path}")

# # Add global rerun logic (optional, overrides per-test rerun)
# def pytest_configure(config):
#     reruns = 2  # rerun failed tests twice
#     config.option.reruns = reruns


# import os
# import time
# import glob
# import shutil
# from pathlib import Path
# import pytest

# # .env loader (simple)
# def _load_dotenv():
#     env_file = Path(__file__).resolve().parents[1] / ".env"
#     if env_file.exists():
#         for line in env_file.read_text().splitlines():
#             if "=" in line and not line.strip().startswith("#"):
#                 k, v = line.split("=", 1)
#                 os.environ.setdefault(k.strip(), v.strip())
# _load_dotenv()

# try:
#     import yagmail
# except ImportError:
#     yagmail = None
#     print("Install yagmail: pip install yagmail")

# MODULE_NAME = "Twitter"
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# today_str = time.strftime("%d-%b-%Y").upper()

# SELENIUM_SCRIPTS = [
#     "tests/selenium/twitter/test_reply_and_assign.py",
#     "tests/selenium/twitter/test_reply_and_await.py",
#     "tests/selenium/twitter/test_reply_and_onHold.py",
#     "tests/selenium/twitter/test_reply_and_escalate.py",
#     "tests/selenium/twitter/test_csd_approve.py",
#     "tests/selenium/twitter/test_reply_and_close.py",
#     "tests/selenium/twitter/test_otherActions_openTicket.py",
#     "tests/selenium/twitter/test_otherActions_closedTicket.py"
# ]

# def get_next_run_folder(base_dir: Path):
#     base_dir.mkdir(parents=True, exist_ok=True)
#     existing = sorted(glob.glob(str(base_dir / "run_*")))
#     if not existing:
#         return base_dir / "run_1"
#     last_run = existing[-1]
#     last_num = int(last_run.split("_")[-1])
#     return base_dir / f"run_{last_num + 1}"

# def send_email(zip_file_path: Path, summary: str, exit_code: int):
#     sender = os.getenv("EMAIL_USER")
#     password = os.getenv("EMAIL_PASS")
#     recipients_raw = os.getenv("EMAIL_TO", "")
#     recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]
#     if not (sender and password and recipients):
#         print("Email skip: missing env vars.")
#         return
#     if yagmail is None:
#         print("yagmail missing.")
#         return
#     status = "PASS ✅" if exit_code == 0 else "FAIL ❌"
#     subject = f"{MODULE_NAME} Suite {status} ({today_str})"
#     body = f"{summary}\n\nReport ZIP attached."
#     try:
#         yag = yagmail.SMTP(sender, password)
#         yag.send(to=recipients, subject=subject, contents=[body], attachments=str(zip_file_path))
#         print(f"Email sent: {', '.join(recipients)}")
#     except Exception as e:
#         print(f"Email failed: {e}")

# def run_suite():
#     print(f"\nRunning {MODULE_NAME} suite for {today_str}\n")
#     start_time = time.time()

#     base_results = PROJECT_ROOT / "Suites" / "allure-results" / MODULE_NAME / today_str
#     base_reports = PROJECT_ROOT / "Suites" / "allure-report" / MODULE_NAME / today_str

#     results_dir = get_next_run_folder(base_results)
#     report_dir = base_reports / f"report_{results_dir.name}"

#     if results_dir.exists():
#         shutil.rmtree(results_dir, ignore_errors=True)
#     results_dir.mkdir(parents=True, exist_ok=True)
#     report_dir.mkdir(parents=True, exist_ok=True)

#     print(f"Results folder: {results_dir}")
#     print(f"Report folder : {report_dir}")

#     pytest_args = [
#         *SELENIUM_SCRIPTS,
#         "-v", "-s", "--tb=short", "--cache-clear",
#         "--reruns", "2", "--reruns-delay", "2",
#         f"--module-name={MODULE_NAME}",
#         f"--alluredir={results_dir}",
#     ]

#     exit_code = pytest.main(pytest_args)

#     print("\nGenerating Allure report...")
#     os.system(f'allure generate "{results_dir}" --clean -o "{report_dir}"')

#     zip_path = PROJECT_ROOT / f"{MODULE_NAME}_Allure_Report_{today_str}_{results_dir.name}.zip"
#     shutil.make_archive(zip_path.with_suffix(''), 'zip', report_dir)
#     print(f"Zip created: {zip_path}")

#     duration = time.time() - start_time
#     status = "PASS" if exit_code == 0 else "FAIL"
#     summary = (
#         f"Module: {MODULE_NAME}\nDate: {today_str}\nStatus: {status}\n"
#         f"Duration: {duration:.1f}s\nResults Dir: {results_dir}\nReport Dir: {report_dir}"
#     )

#     send_email(zip_path, summary, exit_code)

#     print("\nSummary:\n" + summary)
#     if exit_code == 0:
#         print("Suite PASS")
#     else:
#         print("Suite FAIL")

# if __name__ == "__main__":
#     run_suite()







# import time
# from pathlib import Path
# import pytest

# # Folder for screenshots
# SCREENSHOTS_DIR = Path("screenshots")
# SCREENSHOTS_DIR.mkdir(exist_ok=True)

# def capture_selenium_screenshot(driver, nodeid, step_name="step"):
#     timestamp = int(time.time())
#     filename = f"{nodeid.replace('::','_')}_{step_name}_{timestamp}.png"
#     path = SCREENSHOTS_DIR / filename
#     driver.save_screenshot(str(path))
#     print(f"\n📸 Screenshot ({step_name}): file://{path}\n")
#     return str(path)

# def capture_playwright_screenshot(page, nodeid, step_name="step"):
#     timestamp = int(time.time())
#     filename = f"{nodeid.replace('::','_')}_{step_name}_{timestamp}.png"
#     path = SCREENSHOTS_DIR / filename
#     page.screenshot(path=str(path), full_page=True)
#     print(f"\n📸 Screenshot ({step_name}): file://{path}\n")
#     return str(path)

# # Hook to capture screenshots on test failure
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()

#     if rep.when == "call" and rep.failed:
#         # Selenium driver attached to test function
#         driver = getattr(item.instance, "browser", None)
#         if driver:
#             path = capture_selenium_screenshot(driver, item.nodeid, "FAILURE")
#             print(f"❌ Test failed: {rep.longreprtext.splitlines()[-1]}")
#             print(f"   Screenshot link: file://{path}")

#         # Playwright page attached to test function
#         page = getattr(item.instance, "page", None)
#         if page:
#             path = capture_playwright_screenshot(page, item.nodeid, "FAILURE")
#             print(f"❌ Test failed: {rep.longreprtext.splitlines()[-1]}")
#             print(f"   Screenshot link: file://{path}")

# # Add global rerun logic (optional, overrides per-test rerun)
# def pytest_configure(config):
#     reruns = 2  # rerun failed tests twice
#     config.option.reruns = reruns
















import os
import time
from pathlib import Path
import pytest

try:
    import allure
except ImportError:
    allure = None

# Screenshots folder
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

def _timestamp():
    return time.strftime("%Y%m%d_%H%M%S")

def capture_selenium_screenshot(driver, nodeid, step_name="step"):
    filename = f"{nodeid.replace('::','_')}_{step_name}_{_timestamp()}.png"
    path = SCREENSHOTS_DIR / filename
    driver.save_screenshot(str(path))
    print(f"\n📸 Screenshot ({step_name}): file://{path}\n")
    if allure:
        try:
            allure.attach.file(str(path), name=f"{step_name}", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
    return str(path)

def capture_playwright_screenshot(page, nodeid, step_name="step"):
    filename = f"{nodeid.replace('::','_')}_{step_name}_{_timestamp()}.png"
    path = SCREENSHOTS_DIR / filename
    page.screenshot(path=str(path), full_page=True)
    print(f"\n📸 Screenshot ({step_name}): file://{path}\n")
    if allure:
        try:
            allure.attach.file(str(path), name=f"{step_name}", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
    return str(path)

# Failure screenshots
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = getattr(getattr(item, "instance", None), "browser", None)
        if driver:
            path = capture_selenium_screenshot(driver, item.nodeid, "FAILURE")
            print(f"❌ Selenium failure: {path}")
        page = getattr(getattr(item, "instance", None), "page", None)
        if page:
            path = capture_playwright_screenshot(page, item.nodeid, "FAILURE")
            print(f"❌ Playwright failure: {path}")

# Autouse fixture to record real test duration (used for email fallback)
@pytest.fixture(autouse=True)
def _record_duration(request):
    start = time.time()
    yield
    dur = time.time() - start
    durations_file = os.getenv("TEST_DURATIONS_FILE")
    if durations_file:
        try:
            with open(durations_file, "a", encoding="utf-8") as f:
                f.write(f"{request.node.nodeid}|{dur:.6f}\n")
        except Exception as e:
            print("Duration write fail:", e)
    # Optional: attach duration to Allure description
    if allure:
        try:
            allure.dynamic.description_html(f"<p>Measured duration: {dur:.3f}s</p>")
        except Exception:
            pass

# Global rerun (only if not already set via CLI)
def pytest_configure(config):
    env_reruns = os.getenv("GLOBAL_RERUNS")
    env_delay = os.getenv("GLOBAL_RERUNS_DELAY")
    
    # Check if reruns was explicitly set via command line
    if not hasattr(config.option, 'reruns') or config.option.reruns is None:
        reruns = int(env_reruns) if env_reruns else 2
        config.option.reruns = reruns
    # If --reruns=0 was explicitly passed, respect it
    elif config.option.reruns == 0:
        print("Reruns disabled via --reruns=0 flag")
    
    if not hasattr(config.option, 'reruns_delay') or config.option.reruns_delay is None:
        delay = int(env_delay) if env_delay else 2
        config.option.reruns_delay = delay
    
    print(f"Global reruns: {config.option.reruns} (delay {config.option.reruns_delay}s)")
