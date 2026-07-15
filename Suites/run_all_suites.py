"""
Master Suite Runner - Runs all module suites in parallel and provides individual results
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path FIRST
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
load_dotenv()

from helpers.enterprise_email_report import EnterpriseResultRow, build_enterprise_email_html, SuiteResultRow, build_suite_regression_email_html
from helpers.simple_suite_report import generate_simple_suite_report
from helpers.premium_suite_report import save_premium_report
from config.config import TICKET_IDS

# Try to import yagmail for email
try:
    import yagmail
except ImportError:
    yagmail = None
    print("⚠️ yagmail not installed - summary email will not be sent")

# Define all suite files
SUITES = {
    "Twitter": "Suites/test_twitter_suite.py",
    "Instagram": "Suites/test_instagram_suite.py",
    "Facebook": "Suites/test_facebook_suite.py",
    "YouTube": "Suites/test_youtube_suite.py",
    "LinkedIn": "Suites/test_linkedIn_suite.py",
}

# Ticket ID mapping for each module — sourced from config/config.py so
# rotating a ticket only requires editing TICKET_IDS, not this file.
MODULE_TICKET_IDS = {
    "Facebook":  TICKET_IDS["facebook"].strip(),
    "Instagram": TICKET_IDS["instagram"].strip(),
    "LinkedIn":  TICKET_IDS["linkedin"].strip(),
    "Twitter":   f"{TICKET_IDS['twitter'].strip()}, {TICKET_IDS['twitter-OT'].strip()}",  # main + openTicket
    "YouTube":   TICKET_IDS["youtube"].strip(),
}

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
    print(f"{Color.CYAN}{Color.BOLD}{'REGRESSION TEST SUITE - ALL MODULES':^80}{Color.END}")
    print("="*80 + "\n")

def print_module_header(module_name):
    print(f"\n{Color.BLUE}{'='*80}{Color.END}")
    print(f"{Color.BOLD}{Color.YELLOW}Running: {module_name} Module{Color.END}")
    print(f"{Color.BLUE}{'='*80}{Color.END}\n")

def run_suite(module_name, suite_path):
    """Run a single suite and return result"""
    start_time = time.time()
    
    print_module_header(module_name)
    
    # Run the suite
    suite_file = PROJECT_ROOT / suite_path
    if not suite_file.exists():
        print(f"{Color.RED}❌ Suite file not found: {suite_file}{Color.END}")
        return {
            "module": module_name,
            "status": "SKIP",
            "duration": 0,
            "reason": "File not found"
        }
    
    try:
        result = subprocess.run(
            [sys.executable, str(suite_file)],
            cwd=str(PROJECT_ROOT),
            capture_output=False,  # Show output in real-time
            text=True
        )
        
        duration = time.time() - start_time
        status = "PASS" if result.returncode == 0 else "FAIL"
        
        return {
            "module": module_name,
            "status": status,
            "duration": duration,
            "exit_code": result.returncode
        }
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"{Color.RED}❌ Error running {module_name}: {e}{Color.END}")
        return {
            "module": module_name,
            "status": "ERROR",
            "duration": duration,
            "error": str(e)
        }

def print_summary(results):
    """Print final summary of all modules"""
    print("\n" + "="*80)
    print(f"{Color.CYAN}{Color.BOLD}{'FINAL SUMMARY':^80}{Color.END}")
    print("="*80 + "\n")
    
    total_duration = sum(r['duration'] for r in results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    skipped = sum(1 for r in results if r['status'] in ['SKIP', 'ERROR'])
    
    # Module-wise results
    print(f"{Color.BOLD}Module Results:{Color.END}")
    print("-" * 80)
    for result in results:
        module = result['module']
        status = result['status']
        duration = result['duration']
        
        if status == 'PASS':
            status_color = Color.GREEN
            icon = "✅"
        elif status == 'FAIL':
            status_color = Color.RED
            icon = "❌"
        else:
            status_color = Color.YELLOW
            icon = "⚠️"
        
        print(f"{icon} {module:20s} | {status_color}{status:6s}{Color.END} | "
              f"Duration: {duration:6.1f}s")
        
        if 'reason' in result:
            print(f"   Reason: {result['reason']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
    
    print("-" * 80)
    
    # Overall stats
    print(f"\n{Color.BOLD}Overall Statistics:{Color.END}")
    print(f"  Total Modules: {len(results)}")
    print(f"  {Color.GREEN}Passed: {passed}{Color.END}")
    print(f"  {Color.RED}Failed: {failed}{Color.END}")
    print(f"  {Color.YELLOW}Skipped: {skipped}{Color.END}")
    print(f"  Combined Duration (if run sequentially): {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
    
    # Final verdict
    print(f"\n{Color.BOLD}Final Verdict:{Color.END} ", end="")
    if failed == 0 and skipped == 0:
        print(f"{Color.GREEN}ALL SUITES PASSED ✅{Color.END}")
    elif failed == 0:
        print(f"{Color.YELLOW}ALL PASSED WITH SOME SKIPPED ⚠️{Color.END}")
    else:
        print(f"{Color.RED}SOME SUITES FAILED ❌{Color.END}")
    
    print("\n" + "="*80 + "\n")

def send_summary_email(results):
    """Send master summary email using suite regression template"""
    if not yagmail:
        print(f"{Color.YELLOW}⚠️ Email summary skipped - yagmail not installed{Color.END}")
        return

    sender = os.getenv("EMAIL_USER")
    pwd = os.getenv("EMAIL_PASS")
    tos = os.getenv("EMAIL_TO", "").split(",")

    if not sender or not pwd or not tos[0]:
        print(f"{Color.YELLOW}⚠️ Email summary skipped - credentials not configured{Color.END}")
        return

    try:
        # Detect environment from credentials
        from elements.login_page import LoginPageElements
        try:
            # Check which login URL is being used
            cx_url = LoginPageElements.CX_URL
            preprod_url = LoginPageElements.PREPROD_URL
            # Default to CX for master suite (can be overridden if needed)
            environment = "CX"
        except:
            environment = "CX"  # Default

        # Calculate total duration and stats
        total_duration_seconds = sum(float(r.get('duration', 0) or 0) for r in results)
        total_duration_str = f"{total_duration_seconds:.1f}s"
        avg_duration_str = f"{(total_duration_seconds / len(results)):.1f}s" if results else "0.0s"

        # Build suite result rows
        suite_rows = []
        for result in results:
            module = result.get('module', 'Unknown')
            status = result.get('status', 'SKIP')
            duration = f"{float(result.get('duration', 0) or 0):.1f}s"

            # For suite-level report, we don't have individual test counts
            # Use 1 for total and 1/0 for passed/failed based on status
            if status.upper() in ['PASS', 'PASSED', 'SUCCESS']:
                passed = 1
                failed = 0
            else:
                passed = 0
                failed = 1

            suite_rows.append(SuiteResultRow(
                suite_name=module,
                status=status,
                duration=duration,
                passed=passed,
                failed=failed,
                total=1
            ))

        # Build HTML email
        html = build_suite_regression_email_html(
            environment=environment,
            suite_results=suite_rows,
            total_duration=total_duration_str,
            avg_duration=avg_duration_str,
        )

        # Send email
        yag = yagmail.SMTP(sender, pwd)
        subject = f"All Suite Regression Report - {environment} Environment"

        yag.send(
            to=tos,
            subject=subject,
            contents=html,
        )

        print(f"{Color.GREEN}📧 Summary email sent successfully to {', '.join(tos)}{Color.END}")

    except Exception as e:
        print(f"{Color.RED}❌ Failed to send summary email: {e}{Color.END}")

def main():
    """Main execution - runs all suites in parallel"""
    print_banner()
    
    start_time = time.time()
    results = []
    
    # Run all suites in parallel
    print(f"{Color.CYAN}🚀 Starting parallel execution of all modules...{Color.END}\n")
    
    with ThreadPoolExecutor(max_workers=len(SUITES)) as executor:
        # Submit all suite runs
        future_to_module = {
            executor.submit(run_suite, module_name, suite_path): module_name
            for module_name, suite_path in SUITES.items()
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_module):
            module_name = future_to_module[future]
            try:
                result = future.result()
                results.append(result)
                
                # Show completion status
                status = result['status']
                if status == 'PASS':
                    icon = f"{Color.GREEN}✅{Color.END}"
                elif status == 'FAIL':
                    icon = f"{Color.RED}❌{Color.END}"
                else:
                    icon = f"{Color.YELLOW}⚠️{Color.END}"
                
                print(f"\n{icon} {module_name} module completed - {status}\n")
                
            except Exception as e:
                print(f"{Color.RED}❌ Error collecting result for {module_name}: {e}{Color.END}")
                results.append({
                    "module": module_name,
                    "status": "ERROR",
                    "duration": 0,
                    "error": str(e)
                })
    
    # Sort results by module name for consistent display
    results.sort(key=lambda x: x['module'])
    
    # Print summary
    print_summary(results)
    
    # Generate simple HTML report
    report_filename = f"all_suites_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    generate_simple_suite_report(results, environment="CX", output_file=report_filename, module_ticket_ids=MODULE_TICKET_IDS)
    print(f"{Color.GREEN}📄 Simple HTML report saved: {report_filename}{Color.END}\n")

    # Wall-clock time of the run (suites execute in parallel).
    total_duration = time.time() - start_time

    # Premium report (HTML + PDF on the Desktop) built from the REAL results.
    try:
        html_path, pdf_path = save_premium_report(
            results,
            environment="CX",
            module_ticket_ids=MODULE_TICKET_IDS,
            title="CX Regression Report",
            subtitle="Automated regression · social channel suites",
            monogram="CX",
            total_duration=total_duration,
            html_dir=PROJECT_ROOT,
            latest_name="all_suites_report_PASSED_latest.html",
        )
        print(f"{Color.GREEN}📄 Premium report: {html_path}{Color.END}")
        if pdf_path:
            print(f"{Color.GREEN}📕 PDF (Desktop):  {pdf_path}{Color.END}\n")
    except Exception as e:
        print(f"{Color.YELLOW}⚠️ Premium report generation failed: {e}{Color.END}\n")

    # Send summary email
    send_summary_email(results)

    print(f"{Color.CYAN}⏱️  Total execution time (parallel): {total_duration:.1f}s ({total_duration/60:.1f} minutes){Color.END}\n")
    
    # Return exit code (0 if all passed, 1 if any failed)
    exit_code = 1 if any(r['status'] in ['FAIL', 'ERROR'] for r in results) else 0
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
