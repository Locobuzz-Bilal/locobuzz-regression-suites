"""
AWA Regression Suite Runner - Runs all AWA regression tests sequentially
Dashboard and Widget Maker tests
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
load_dotenv()

# Try to import yagmail for email
try:
    import yagmail
except ImportError:
    yagmail = None
    print("⚠️ yagmail not installed - summary email will not be sent")

# Define all AWA regression test scripts in execution order
AWA_TESTS = [
    # Dashboard Tests
    {
        "name": "Create, Edit, Duplicate & Delete Dashboard",
        "path": "tests/selenium/AWA Regression/Dashboard/create_dashboard.py",
        "category": "Dashboard"
    },
    {
        "name": "Download Reports (PDF & PPT)",
        "path": "tests/selenium/AWA Regression/Dashboard/download_reports.py",
        "category": "Dashboard"
    },
    {
        "name": "Share Link",
        "path": "tests/selenium/AWA Regression/Dashboard/share_link.py",
        "category": "Dashboard"
    },
    # Widget Maker Tests
    {
        "name": "Create, Edit, Preview, Duplicate & Delete Widget",
        "path": "tests/selenium/AWA Regression/Widget Maker/create_widget.py",
        "category": "Widget Maker"
    },
    {
        "name": "Save As Dashboard",
        "path": "tests/selenium/AWA Regression/Widget Maker/save_as_dashboard.py",
        "category": "Widget Maker"
    },
    {
        "name": "Save Dashboard",
        "path": "tests/selenium/AWA Regression/Widget Maker/save_dashboard.py",
        "category": "Widget Maker"
    },
]

class Color:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    print("\n" + "="*80)
    print(f"{Color.CYAN}{Color.BOLD}{'AWA REGRESSION TEST SUITE':^80}{Color.END}")
    print("="*80 + "\n")

def print_test_header(test_name, test_num, total_tests):
    print(f"\n{Color.BLUE}{'='*80}{Color.END}")
    print(f"{Color.BOLD}{Color.YELLOW}[{test_num}/{total_tests}] Running: {test_name}{Color.END}")
    print(f"{Color.BLUE}{'='*80}{Color.END}\n")

def run_test(test_info, test_num, total_tests, allure_dir):
    """Run a single test and return result"""
    start_time = time.time()
    
    print_test_header(test_info["name"], test_num, total_tests)
    
    # Check if test file exists
    test_file = PROJECT_ROOT / test_info["path"]
    if not test_file.exists():
        print(f"{Color.RED}❌ Test file not found: {test_file}{Color.END}")
        return {
            "name": test_info["name"],
            "category": test_info["category"],
            "status": "SKIP",
            "duration": 0,
            "reason": "File not found"
        }
    
    try:
        # Run the test using pytest with allure reporting
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_file), "--reruns=0", "-v", 
             f"--alluredir={allure_dir}"],
            cwd=str(PROJECT_ROOT),
            capture_output=False,  # Show output in real-time
            text=True
        )
        
        duration = time.time() - start_time
        status = "PASS" if result.returncode == 0 else "FAIL"
        
        status_symbol = f"{Color.GREEN}✅{Color.END}" if status == "PASS" else f"{Color.RED}❌{Color.END}"
        print(f"\n{status_symbol} {test_info['name']} completed - {status} ({duration:.1f}s)\n")
        
        return {
            "name": test_info["name"],
            "category": test_info["category"],
            "status": status,
            "duration": duration,
            "exit_code": result.returncode
        }
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"{Color.RED}❌ Error running {test_info['name']}: {e}{Color.END}")
        return {
            "name": test_info["name"],
            "category": test_info["category"],
            "status": "ERROR",
            "duration": duration,
            "reason": str(e)
        }

def print_summary(results, total_duration):
    """Print final summary"""
    print("\n" + "="*80)
    print(f"{Color.CYAN}{Color.BOLD}{'AWA REGRESSION SUITE SUMMARY':^80}{Color.END}")
    print("="*80 + "\n")
    
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    
    print(f"{Color.BOLD}Overall Statistics:{Color.END}")
    print(f"  Total Tests: {total}")
    print(f"  {Color.GREEN}Passed: {passed}{Color.END}")
    print(f"  {Color.RED}Failed: {failed}{Color.END}")
    print(f"  {Color.YELLOW}Skipped: {skipped}{Color.END}")
    print(f"  {Color.RED}Errors: {errors}{Color.END}")
    print(f"  Total Duration: {total_duration:.1f}s\n")
    
    # Group by category
    categories = {}
    for result in results:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(result)
    
    # Print results by category
    for category, tests in categories.items():
        print(f"{Color.BOLD}{category} Tests:{Color.END}")
        for test in tests:
            status_color = Color.GREEN if test["status"] == "PASS" else Color.RED
            status_symbol = "✅" if test["status"] == "PASS" else "❌"
            print(f"  {status_symbol} {test['name']}: {status_color}{test['status']}{Color.END} ({test['duration']:.1f}s)")
        print()
    
    # Overall result
    if failed == 0 and errors == 0:
        print(f"{Color.GREEN}{Color.BOLD}{'🎉 ALL TESTS PASSED!':^80}{Color.END}\n")
    else:
        print(f"{Color.RED}{Color.BOLD}{'❌ SOME TESTS FAILED':^80}{Color.END}\n")
    
    print("="*80 + "\n")

def send_summary_email(results, total_duration):
    """Send summary email if configured"""
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    recipients = [r.strip() for r in os.getenv("AWA_EMAIL", "").split(",") if r.strip()]
    
    if not (sender and password and recipients and yagmail):
        print("📧 Email summary skipped (not configured or yagmail not installed)")
        return
    
    try:
        # Create HTML email body
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        skipped = sum(1 for r in results if r["status"] == "SKIP")
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # Determine overall status color
        status_color = "#27ae60" if failed == 0 else "#e74c3c"
        status_icon = "✅" if failed == 0 else "❌"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0;padding:20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;background:#f5f5f5;">
            <div style="max-width:700px;margin:0 auto;background:white;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.1);overflow:hidden;">
                <!-- Header -->
                <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:30px 20px;text-align:center;">
                    <h1 style="margin:0;color:white;font-size:24px;font-weight:600;">AWA Regression Suite</h1>
                    <p style="margin:8px 0 0;color:rgba(255,255,255,0.9);font-size:14px;">{datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
                </div>
                
                <!-- Summary Cards -->
                <div style="padding:25px 20px;">
                    <div style="display:flex;gap:10px;margin-bottom:20px;">
                        <div style="flex:1;background:#f8f9fa;border-radius:8px;padding:15px;text-align:center;border-left:4px solid {status_color};">
                            <div style="font-size:32px;font-weight:700;color:{status_color};margin-bottom:5px;">{status_icon} {pass_rate:.0f}%</div>
                            <div style="font-size:12px;color:#6c757d;font-weight:500;">PASS RATE</div>
                        </div>
                        <div style="flex:1;background:#f8f9fa;border-radius:8px;padding:15px;text-align:center;">
                            <div style="font-size:28px;font-weight:700;color:#27ae60;margin-bottom:5px;">{passed}</div>
                            <div style="font-size:12px;color:#6c757d;font-weight:500;">PASSED</div>
                        </div>
                        <div style="flex:1;background:#f8f9fa;border-radius:8px;padding:15px;text-align:center;">
                            <div style="font-size:28px;font-weight:700;color:#e74c3c;margin-bottom:5px;">{failed}</div>
                            <div style="font-size:12px;color:#6c757d;font-weight:500;">FAILED</div>
                        </div>
                        <div style="flex:1;background:#f8f9fa;border-radius:8px;padding:15px;text-align:center;">
                            <div style="font-size:28px;font-weight:700;color:#6c757d;margin-bottom:5px;">{total}</div>
                            <div style="font-size:12px;color:#6c757d;font-weight:500;">TOTAL</div>
                        </div>
                    </div>
                    
                    <!-- Duration -->
                    <div style="text-align:center;margin-bottom:20px;padding:10px;background:#f8f9fa;border-radius:8px;">
                        <span style="color:#6c757d;font-size:13px;">⏱️ Duration: <strong style="color:#495057;">{int(total_duration//60)}m {int(total_duration%60)}s</strong></span>
                    </div>
                    
                    <!-- Test Results Table -->
                    <div style="overflow-x:auto;">
                        <table style="width:100%;border-collapse:separate;border-spacing:0;font-size:13px;">
                            <thead>
                                <tr style="background:#f8f9fa;">
                                    <th style="padding:12px 10px;text-align:left;color:#495057;font-weight:600;border-bottom:2px solid #dee2e6;">Category</th>
                                    <th style="padding:12px 10px;text-align:left;color:#495057;font-weight:600;border-bottom:2px solid #dee2e6;">Test Name</th>
                                    <th style="padding:12px 10px;text-align:center;color:#495057;font-weight:600;border-bottom:2px solid #dee2e6;width:80px;">Status</th>
                                    <th style="padding:12px 10px;text-align:right;color:#495057;font-weight:600;border-bottom:2px solid #dee2e6;width:70px;">Time</th>
                                </tr>
                            </thead>
                            <tbody>
        """
        
        for idx, result in enumerate(results):
            status_color = "#27ae60" if result["status"] == "PASS" else "#e74c3c"
            status_icon = "✓" if result["status"] == "PASS" else "✗"
            bg_color = "#ffffff" if idx % 2 == 0 else "#f8f9fa"
            
            html_body += f"""
                                <tr style="background:{bg_color};">
                                    <td style="padding:10px;color:#6c757d;border-bottom:1px solid #e9ecef;">{result['category']}</td>
                                    <td style="padding:10px;color:#212529;border-bottom:1px solid #e9ecef;font-weight:500;">{result['name']}</td>
                                    <td style="padding:10px;text-align:center;border-bottom:1px solid #e9ecef;">
                                        <span style="display:inline-block;padding:4px 10px;border-radius:12px;background:{status_color}15;color:{status_color};font-weight:600;font-size:11px;">{status_icon} {result['status']}</span>
                                    </td>
                                    <td style="padding:10px;text-align:right;color:#6c757d;border-bottom:1px solid #e9ecef;font-family:monospace;">{result['duration']:.1f}s</td>
                                </tr>
            """
        
        html_body += """
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="padding:15px 20px;background:#f8f9fa;text-align:center;border-top:1px solid #dee2e6;">
                    <p style="margin:0;color:#6c757d;font-size:12px;">🤖 Automated Test Report • Locobuzz Automation Framework</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        subject = f"{status_icon} AWA Regression: {passed}/{total} Passed ({pass_rate:.0f}%)"
        
        yag = yagmail.SMTP(sender, password)
        yag.send(to=recipients, subject=subject, contents=[html_body])
        print(f"{Color.GREEN}✅ Summary email sent successfully{Color.END}")
        
    except Exception as e:
        print(f"{Color.RED}❌ Failed to send email: {e}{Color.END}")

def generate_allure_report(allure_results_dir, allure_report_dir):
    """Generate Allure HTML report from results"""
    try:
        print(f"\n{Color.CYAN}📊 Generating Allure report...{Color.END}")
        
        # Generate report
        result = subprocess.run(
            ["allure", "generate", str(allure_results_dir), "-o", str(allure_report_dir), "--clean"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"{Color.GREEN}✅ Allure report generated: {allure_report_dir}{Color.END}")
            print(f"{Color.CYAN}📂 To view report, run: allure open {allure_report_dir}{Color.END}")
        else:
            print(f"{Color.YELLOW}⚠️ Allure report generation failed: {result.stderr}{Color.END}")
            
    except FileNotFoundError:
        print(f"{Color.YELLOW}⚠️ Allure command not found. Install Allure to generate reports.{Color.END}")
    except Exception as e:
        print(f"{Color.RED}❌ Error generating Allure report: {e}{Color.END}")

def main():
    """Main execution function"""
    print_banner()
    
    print(f"{Color.CYAN}🚀 Starting AWA Regression Test Suite...{Color.END}")
    print(f"{Color.CYAN}📋 {len(AWA_TESTS)} tests will run sequentially{Color.END}\n")
    
    # Setup Allure directories
    timestamp = datetime.now().strftime("%d%b%Y")
    allure_results_dir = PROJECT_ROOT / "Suites" / "allure-results" / f"AWA-Regression-{timestamp}"
    allure_report_dir = PROJECT_ROOT / "Suites" / "allure-report" / f"AWA-Regression-{timestamp}"
    
    # Create directories if they don't exist
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"{Color.CYAN}📁 Allure results will be saved to: {allure_results_dir}{Color.END}\n")
    
    overall_start = time.time()
    results = []
    
    # Run each test sequentially
    for idx, test_info in enumerate(AWA_TESTS, 1):
        result = run_test(test_info, idx, len(AWA_TESTS), str(allure_results_dir))
        results.append(result)
        
        # Small delay between tests
        if idx < len(AWA_TESTS):
            time.sleep(2)
    
    total_duration = time.time() - overall_start
    
    # Print summary
    print_summary(results, total_duration)
    
    # Generate Allure report
    generate_allure_report(allure_results_dir, allure_report_dir)
    
    # Send email summary if configured
    send_summary_email(results, total_duration)
    
    # Exit with appropriate code
    failed_tests = [r for r in results if r["status"] in ["FAIL", "ERROR"]]
    sys.exit(1 if failed_tests else 0)

if __name__ == "__main__":
    main()
