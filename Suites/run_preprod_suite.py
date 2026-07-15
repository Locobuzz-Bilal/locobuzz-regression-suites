"""
PreProd Regression Suite Runner
Runs all PreProd test modules: Manual Reg, Chatbot, and Bulk Actions
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

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

from helpers.enterprise_email_report import EnterpriseResultRow, build_enterprise_email_html
from helpers.simple_suite_report import generate_simple_suite_report
from helpers.premium_suite_report import save_premium_report
from config.config import TICKET_IDS

# Define all PreProd test files
PREPROD_TESTS = {
    "Manual Regression": "PreProd Regression/preprod_reg.py/preprod_reg.py", #requires config update
    "Chatbot Workflow": "tests/selenium/chatbot/test_chatbot_workflow.py", #insta dm automatically assigs to chatbot
    "LinkedIn Regression": "tests/selenium/linkedin/test_linkedin_regpp.py", # LinkedIn preprod regression
    "Publish Workflow": "tests/selenium/publish/test_publish_workflow.py", #no ticket actions
    #  "Bulk Actions": "tests/selenium/PreProd/Bulk Actions/test_bulk_actions.py", #works with author name
}

# Ticket IDs used by each test module (sourced from config/config.py so
# rotating a ticket only requires editing TICKET_IDS).
TEST_TICKET_IDS = {
    "Manual Regression":   f"{TICKET_IDS['facebook'].strip()} (Facebook)",
    "Chatbot Workflow":    f"{TICKET_IDS['insta-chatbot'].strip()} (Instagram DM → Chatbot)",
    "LinkedIn Regression": f"{TICKET_IDS['linkedin'].strip()} (LinkedIn)",
    "Publish Workflow":    "None (No ticket actions)",
}

# Bare ticket numbers for the premium report's "Ticket ID" column.
PREMIUM_TICKET_IDS = {
    "Manual Regression":   TICKET_IDS["facebook"].strip(),
    "Chatbot Workflow":    TICKET_IDS["insta-chatbot"].strip(),
    "LinkedIn Regression": TICKET_IDS["linkedin"].strip(),
    "Publish Workflow":    "—",
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
    print(f"{Color.CYAN}{Color.BOLD}{'REGRESSION TEST SUITE - PREPROD ENVIRONMENT':^80}{Color.END}")
    print("="*80 + "\n")

def print_module_header(module_name):
    print(f"\n{Color.BLUE}{'='*80}{Color.END}")
    print(f"{Color.BOLD}{Color.YELLOW}Running: {module_name}{Color.END}")
    print(f"{Color.BLUE}{'='*80}{Color.END}\n")

def run_test(module_name, test_path):
    """Run a single test and return result"""
    start_time = time.time()
    
    print_module_header(module_name)
    
    # Run the test
    test_file = PROJECT_ROOT / test_path
    if not test_file.exists():
        print(f"{Color.RED}❌ Test file not found: {test_file}{Color.END}")
        return {
            "module": module_name,
            "status": "SKIP",
            "duration": 0,
            "reason": "File not found"
        }
    
    try:
        # Run pytest on the test file with isolated cache
        cache_dir = PROJECT_ROOT / ".pytest_cache" / module_name.replace(" ", "_")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short", 
             "-o", f"cache_dir={cache_dir}"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,  # Capture to parse retries
            text=True,
            # Test output contains emoji/unicode; without an explicit utf-8 decode
            # Windows falls back to cp1252, the reader thread dies, and stdout comes
            # back as None -> "NoneType + str" crash that shows up as a false ERROR.
            encoding="utf-8",
            errors="replace",
        )

        duration = time.time() - start_time
        status = "PASS" if result.returncode == 0 else "FAIL"
        
        # Parse output for retries
        output = result.stdout + result.stderr
        retries = 0
        if "rerun" in output.lower() or "RERUN" in output:
            retries = output.count("RERUN")
        
        # Print output to console
        print(output)
        
        return {
            "module": module_name,
            "status": status,
            "duration": duration,
            "exit_code": result.returncode,
            "retries": retries,
            "test_file": test_path
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
    print(f"{Color.CYAN}{Color.BOLD}{'PREPROD SUITE - FINAL SUMMARY':^80}{Color.END}")
    print("="*80 + "\n")
    
    total_duration = sum(r['duration'] for r in results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    skipped = sum(1 for r in results if r['status'] in ['SKIP', 'ERROR'])
    
    # Module-wise results
    print(f"{Color.BOLD}Test Results:{Color.END}")
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
        
        print(f"{icon} {module:25s} | {status_color}{status:6s}{Color.END} | "
              f"Duration: {duration:6.1f}s")
        
        if 'reason' in result:
            print(f"   Reason: {result['reason']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
    
    print("-" * 80)
    
    # Overall stats
    print(f"\n{Color.BOLD}Overall Statistics:{Color.END}")
    print(f"  Total Tests: {len(results)}")
    print(f"  {Color.GREEN}Passed: {passed}{Color.END}")
    print(f"  {Color.RED}Failed: {failed}{Color.END}")
    print(f"  {Color.YELLOW}Skipped: {skipped}{Color.END}")
    print(f"  Total Duration: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
    
    # Final verdict
    print(f"\n{Color.BOLD}Final Verdict:{Color.END} ", end="")
    if failed == 0 and skipped == 0:
        print(f"{Color.GREEN}ALL TESTS PASSED ✅{Color.END}")
    elif failed == 0:
        print(f"{Color.YELLOW}ALL PASSED WITH SOME SKIPPED ⚠️{Color.END}")
    else:
        print(f"{Color.RED}SOME TESTS FAILED ❌{Color.END}")
    
    print("\n" + "="*80 + "\n")

def send_summary_email(results):
    """Send PreProd suite summary email using enterprise template"""
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
        # Calculate stats
        total_duration = sum(r['duration'] for r in results)
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        skipped = sum(1 for r in results if r['status'] in ['SKIP', 'ERROR'])
        total_retries = sum(r.get('retries', 0) for r in results)
        pass_rate = (passed/len(results)*100) if results else 0
        
        # Determine overall status emoji (used in subject)
        if failed == 0 and skipped == 0:
            status_emoji = "✅"
        elif failed == 0:
            status_emoji = "⚠️"
        else:
            status_emoji = "❌"
        
        # Format timestamp
        now = datetime.now()
        timestamp = now.strftime("%B %d, %Y at %H:%M:%S IST")
        today_str = now.strftime("%d-%b-%Y").upper()
        
        # Detect environment (PreProd suite always uses PreProd)
        environment = "PreProd"
        
        ticket_config_html = "".join(
            f"<tr><td style=\"padding: 5px 0; color: #a1a1aa; font-size: 13px; width: 35%;\">{module_name}:</td>"
            f"<td style=\"padding: 5px 0; color: #bae6fd; font-size: 13px; font-weight: 600; font-family: 'Courier New', monospace;\">{ticket_id}</td></tr>"
            for module_name, ticket_id in TEST_TICKET_IDS.items()
        )

        rows = []
        for idx, result in enumerate(results, 1):
            module = result.get('module', '—')
            status = result.get('status', 'SKIP')
            duration = float(result.get('duration', 0.0) or 0.0)
            ticket_id = TEST_TICKET_IDS.get(str(module), '—')
            test_file = str(result.get('test_file') or '')
            script_name = test_file.split('/')[-1] if '/' in test_file else test_file.split('\\')[-1]
            details = f"File: {script_name}" if script_name else ""
            if result.get('retries'):
                details = (details + " | " if details else "") + f"Retries: {result.get('retries')}"
            if result.get('reason'):
                details = (details + " | " if details else "") + str(result.get('reason'))
            if result.get('error'):
                details = (details + " | " if details else "") + str(result.get('error'))

            rows.append(
                EnterpriseResultRow(
                    index=idx,
                    name=str(module),
                    reference=f"Ticket: {ticket_id}",
                    status=str(status),
                    duration_seconds=duration,
                    details=details or "—",
                )
            )

        html = build_enterprise_email_html(
            suite_title="Enterprise Test Execution Report",
            suite_subtitle=f"{environment} Environment • Automated Regression Suite",
            environment=environment,
            rows=rows,
            total_duration_seconds=total_duration,
            generated_at=now.strftime('%B %d, %Y %H:%M:%S IST'),
            run_by=os.getenv("REPORT_RUN_BY") or "Automation",
            config_title="Module Ticket Configuration",
            config_rows_html=ticket_config_html,
        )
        
        # Send email
        subject = f"PreProd Regression Suite - {status_emoji} {pass_rate:.0f}% Success - {today_str}"
        
        yagmail.SMTP(sender, pwd).send(to=tos, subject=subject, contents=[html])
        print(f"\n{Color.GREEN}✅ Enterprise email report sent successfully to {', '.join(tos)}{Color.END}")
        
        # Also save HTML report locally
        report_filename = f"preprod_suite_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"{Color.GREEN}💾 HTML report also saved locally as: {report_filename}{Color.END}")
        
    except Exception as e:
        print(f"{Color.RED}❌ Failed to send summary email: {e}{Color.END}")
        import traceback
        traceback.print_exc()

def _send_fallback_email(results, sender, pwd, tos):
    """Fallback email function with basic HTML"""
    try:
        today_str = datetime.now().strftime("%d-%b-%Y").upper()
        
        # Calculate stats
        total_duration = sum(r['duration'] for r in results)
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        skipped = sum(1 for r in results if r['status'] in ['SKIP', 'ERROR'])
        
        # Determine overall status
        if failed == 0 and skipped == 0:
            overall_status = "✅ ALL PASSED"
            status_color = "#28a745"
        elif failed == 0:
            overall_status = "⚠️ PASSED WITH WARNINGS"
            status_color = "#ffc107"
        else:
            overall_status = "❌ SOME FAILED"
            status_color = "#dc3545"
        
        # Calculate additional stats
        total_retries = sum(r.get('retries', 0) for r in results)
        avg_duration = total_duration / len(results) if results else 0
        pass_rate = (passed/len(results)*100) if results else 0
        
        # Build HTML email with inline styles for maximum email client compatibility
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 20px; font-family: Arial, Helvetica, sans-serif; background-color: #f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 700px; margin: 0 auto; background-color: #ffffff;">
                
                <!-- Header Banner -->
                <tr>
                    <td style="background-color: #2c3e50; padding: 30px 25px; text-align: center; border-bottom: 4px solid {status_color};">
                        <h1 style="margin: 0 0 8px 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: 1px;">LOCOBUZZ AUTOMATION REPORT</h1>
                        <p style="margin: 0; color: #95a5a6; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px;">PreProd Regression Suite</p>
                    </td>
                </tr>
                
                <!-- Status Banner -->
                <tr>
                    <td style="background-color: {status_color}; padding: 25px; text-align: center;">
                        <h2 style="margin: 0 0 10px 0; color: #ffffff; font-size: 24px; font-weight: bold;">{overall_status}</h2>
                        <p style="margin: 0; color: #ffffff; font-size: 14px; opacity: 0.95;"> PreProd Environment | {today_str}</p>
                    </td>
                </tr>
                
                <!-- Executive Summary -->
                <tr>
                    <td style="padding: 30px 25px; background-color: #ffffff; border-bottom: 1px solid #e0e0e0;">
                        <p style="margin: 0 0 20px 0; color: #2c3e50; font-size: 15px; line-height: 1.6;">
                            The PreProd regression suite execution has <strong style="color: {status_color};">{"PASSED" if failed == 0 and skipped == 0 else "FAILED" if failed > 0 else "COMPLETED WITH WARNINGS"}</strong>. 
                            Out of {len(results)} test modules, <strong style="color: #28a745;">{passed} passed</strong>{f', <strong style="color: #dc3545;">{failed} failed</strong>' if failed > 0 else ''}{f', and <strong style="color: #ffc107;">{skipped} skipped</strong>' if skipped > 0 else ''}. 
                            Total execution time was <strong>{total_duration:.1f} seconds</strong> ({total_duration/60:.1f} minutes).
                        </p>
                    </td>
                </tr>
                
                <!-- Key Metrics -->
                <tr>
                    <td style="padding: 0; background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td width="33.33%" style="padding: 25px 15px; text-align: center; border-right: 1px solid #dee2e6;">
                                    <div style="color: #6c757d; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 10px;">⏱️ DURATION</div>
                                    <div style="color: #2c3e50; font-size: 28px; font-weight: 700; margin: 5px 0;">{total_duration:.1f}s</div>
                                    <div style="color: #7f8c8d; font-size: 12px;">{total_duration/60:.1f} minutes</div>
                                </td>
                                <td width="33.33%" style="padding: 25px 15px; text-align: center; border-right: 1px solid #dee2e6;">
                                    <div style="color: #6c757d; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 10px;">✅ PASSED</div>
                                    <div style="color: #28a745; font-size: 28px; font-weight: 700; margin: 5px 0;">{passed}</div>
                                    <div style="color: #7f8c8d; font-size: 12px;">{pass_rate:.0f}% success rate</div>
                                </td>
                                <td width="33.33%" style="padding: 25px 15px; text-align: center;">
                                    <div style="color: #6c757d; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 10px;">❌ FAILED</div>
                                    <div style="color: #dc3545; font-size: 28px; font-weight: 700; margin: 5px 0;">{failed}</div>
                                    <div style="color: #7f8c8d; font-size: 12px;">{(failed/len(results)*100) if results else 0:.0f}% failure rate</div>
                                </td>
                            </tr>
                            <tr>
                                <td width="33.33%" style="padding: 25px 15px; text-align: center; border-right: 1px solid #dee2e6; border-top: 1px solid #dee2e6;">
                                    <div style="color: #6c757d; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 10px;">⚠️ SKIPPED</div>
                                    <div style="color: #ffc107; font-size: 28px; font-weight: 700; margin: 5px 0;">{skipped}</div>
                                    <div style="color: #7f8c8d; font-size: 12px;">Error cases</div>
                                </td>
                                <td width="33.33%" style="padding: 25px 15px; text-align: center; border-right: 1px solid #dee2e6; border-top: 1px solid #dee2e6;">
                                    <div style="color: #6c757d; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 10px;">📦 TOTAL</div>
                                    <div style="color: #2c3e50; font-size: 28px; font-weight: 700; margin: 5px 0;">{len(results)}</div>
                                    <div style="color: #7f8c8d; font-size: 12px;">Test modules</div>
                                </td>
                                <td width="33.33%" style="padding: 25px 15px; text-align: center; border-top: 1px solid #dee2e6;">
                                    <div style="color: #6c757d; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 10px;">🔄 RETRIES</div>
                                    <div style="color: #fd7e14; font-size: 28px; font-weight: 700; margin: 5px 0;">{total_retries}</div>
                                    <div style="color: #7f8c8d; font-size: 12px;">Total reruns</div>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                
                <!-- Section Title -->
                <tr>
                    <td style="padding: 30px 25px 15px 25px; background-color: #ffffff;">
                        <h2 style="margin: 0; color: #2c3e50; font-size: 18px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid #2c3e50; padding-bottom: 12px;">
                            📋 Detailed Test Results
                        </h2>
                    </td>
                </tr>
                
                <!-- Test Results Table -->
                <tr>
                    <td style="padding: 0 25px 30px 25px; background-color: #ffffff;">
                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border: 1px solid #dee2e6;">
                            <thead>
                                <tr style="background-color: #34495e;">
                                    <th style="padding: 16px 12px; text-align: left; color: #ffffff; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; border-bottom: 2px solid #2c3e50;">Module</th>
                                    <th style="padding: 16px 12px; text-align: left; color: #ffffff; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; border-bottom: 2px solid #2c3e50;">Ticket ID</th>
                                    <th style="padding: 16px 12px; text-align: left; color: #ffffff; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; border-bottom: 2px solid #2c3e50;">Status</th>
                                    <th style="padding: 16px 12px; text-align: center; color: #ffffff; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; border-bottom: 2px solid #2c3e50;">Duration</th>
                                    <th style="padding: 16px 12px; text-align: center; color: #ffffff; font-size: 11px; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; border-bottom: 2px solid #2c3e50;">Retries</th>
                                </tr>
                            </thead>
                            <tbody>
        """
        
        for idx, result in enumerate(results, 1):
            module = result['module']
            status = result['status']
            duration = result['duration']
            retries = result.get('retries', 0)
            test_file = result.get('test_file', 'N/A')
            
            # Extract just the filename from path
            script_name = test_file.split('/')[-1] if '/' in test_file else test_file.split('\\')[-1]
            
            # Get ticket ID for this module
            ticket_id = TEST_TICKET_IDS.get(module, 'N/A')
            
            if status == 'PASS':
                status_bg = '#d4edda'
                status_color = '#155724'
                icon = "✅"
            elif status == 'FAIL':
                status_bg = '#f8d7da'
                status_color = '#721c24'
                icon = "❌"
            else:
                status_bg = '#fff3cd'
                status_color = '#856404'
                icon = "⚠️"
            
            retry_display = f'{retries}' if retries > 0 else '—'
            row_bg = '#ffffff' if idx % 2 == 1 else '#f8f9fa'
            
            html += f"""
                                <tr style="background-color: {row_bg};">
                                    <td style="padding: 14px 10px; border-bottom: 1px solid #dee2e6;">
                                        <strong style="color: #2c3e50;">{module}</strong><br>
                                        <span style="font-family: 'Courier New', monospace; font-size: 12px; color: #6c757d; background-color: #f1f3f5; padding: 2px 6px; border-radius: 3px;">{script_name}</span>
                                    </td>
                                    <td style="padding: 14px 10px; border-bottom: 1px solid #dee2e6;">
                                        <span style="font-family: 'Courier New', monospace; font-size: 13px; color: #495057; background-color: #e7f3ff; padding: 4px 8px; border-radius: 4px; border-left: 3px solid #007bff;">🎫 {ticket_id}</span>
                                    </td>
                                    <td style="padding: 14px 10px; border-bottom: 1px solid #dee2e6;">
                                        <span style="display: inline-block; background-color: {status_bg}; color: {status_color}; padding: 6px 12px; border-radius: 15px; font-weight: 600; font-size: 12px;">
                                            {icon} {status}
                                        </span>
                                    </td>
                                    <td style="padding: 14px 10px; text-align: center; border-bottom: 1px solid #dee2e6; font-weight: 600; color: #495057;">
                                        {duration:.2f}s
                                    </td>
                                    <td style="padding: 14px 10px; text-align: center; border-bottom: 1px solid #dee2e6; font-weight: 600; color: {'#fd7e14' if retries > 0 else '#6c757d'};">
                                        {retry_display}
                                    </td>
                                </tr>
            """
        
        html += f"""
                            </tbody>
                        </table>
                    </td>
                </tr>
                
                <!-- Summary Stats Bar -->
                <tr>
                    <td style="padding: 20px 25px; background-color: #f8f9fa; border-top: 2px solid #dee2e6;">
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td style="text-align: center; padding: 8px;">
                                    <span style="color: #6c757d; font-size: 12px; font-weight: 600;">AVG DURATION</span><br>
                                    <span style="color: #495057; font-size: 16px; font-weight: bold;">{avg_duration:.1f}s</span>
                                </td>
                                <td style="text-align: center; padding: 8px; border-left: 1px solid #dee2e6; border-right: 1px solid #dee2e6;">
                                    <span style="color: #6c757d; font-size: 12px; font-weight: 600;">SUCCESS RATE</span><br>
                                    <span style="color: {'#28a745' if pass_rate >= 80 else '#dc3545' if pass_rate < 50 else '#ffc107'}; font-size: 16px; font-weight: bold;">{pass_rate:.1f}%</span>
                                </td>
                                <td style="text-align: center; padding: 8px;">
                                    <span style="color: #6c757d; font-size: 12px; font-weight: 600;">TOTAL RETRIES</span><br>
                                    <span style="color: #495057; font-size: 16px; font-weight: bold;">{total_retries}</span>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                
                <!-- Footer -->
                <tr>
                    <td style="padding: 30px 25px; background-color: #2c3e50; text-align: center; border-top: 3px solid #34495e;">
                        <p style="margin: 0 0 12px 0; color: #ecf0f1; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px;">LocoBuzz Automation</p>
                        <p style="margin: 5px 0; color: #95a5a6; font-size: 12px; line-height: 1.6;">Comprehensive regression validation for PreProd environment</p>
                        <p style="margin: 15px 0 8px 0; color: #7f8c8d; font-size: 11px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p style="margin: 0; color: #7f8c8d; font-size: 11px;">Automated by Bilal Shaikh | QA Engineer | LocoBuzz</p>
                    </td>
                </tr>
                
            </table>
        </body>
        </html>
        """
        
        subject = f"PreProd Regression Suite - {overall_status} - {today_str}"
        
        yagmail.SMTP(sender, pwd).send(to=tos, subject=subject, contents=[html])
        print(f"\n{Color.GREEN}✅ Summary email sent successfully to {', '.join(tos)}{Color.END}")
        
    except Exception as e:
        print(f"{Color.RED}❌ Failed to send summary email: {e}{Color.END}")

def main():
    """Main execution - runs all PreProd tests in parallel"""
    print_banner()
    
    start_time = time.time()
    results = []
    
    print(f"{Color.CYAN}🚀 Starting PreProd Regression Suite (Parallel Execution)...{Color.END}\n")
    print(f"{Color.BOLD}Tests to run:{Color.END}")
    for i, (name, path) in enumerate(PREPROD_TESTS.items(), 1):
        print(f"  {i}. {name}")
    print()
    
    print(f"{Color.YELLOW}⚡ Running {len(PREPROD_TESTS)} tests in parallel...{Color.END}\n")
    
    # Run all tests in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=len(PREPROD_TESTS)) as executor:
        # Submit all tests
        future_to_module = {
            executor.submit(run_test, module_name, test_path): module_name
            for module_name, test_path in PREPROD_TESTS.items()
        }
        
        # Process results as they complete
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
                
                print(f"\n{icon} {module_name} completed - {status} (Duration: {result['duration']:.1f}s)\n")
                
            except Exception as e:
                print(f"{Color.RED}❌ Exception in {module_name}: {e}{Color.END}")
                results.append({
                    "module": module_name,
                    "status": "ERROR",
                    "duration": 0,
                    "error": str(e)
                })
    
    # Sort results by original order for consistent reporting
    original_order = list(PREPROD_TESTS.keys())
    results.sort(key=lambda x: original_order.index(x['module']))
    
    # Print summary
    print_summary(results)
    
    # Generate simple HTML report
    report_filename = f"preprod_suite_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    generate_simple_suite_report(results, environment="PreProd", output_file=report_filename)
    print(f"{Color.GREEN}📄 Simple HTML report saved: {report_filename}{Color.END}\n")

    # Wall-clock time of the run (suites execute in parallel, so this is the
    # elapsed time, not the sum of module durations).
    total_duration = time.time() - start_time

    # Premium report (HTML + PDF on the Desktop) built from the REAL results.
    try:
        html_path, pdf_path = save_premium_report(
            results,
            environment="PreProd",
            module_ticket_ids=PREMIUM_TICKET_IDS,
            title="PreProd Regression Report",
            subtitle="Automated regression · pre-production suite",
            monogram="PP",
            total_duration=total_duration,
            html_dir=PROJECT_ROOT,
            latest_name="preprod_regression_PASSED_latest.html",
        )
        print(f"{Color.GREEN}📄 Premium report: {html_path}{Color.END}")
        if pdf_path:
            print(f"{Color.GREEN}📕 PDF (Desktop):  {pdf_path}{Color.END}\n")
    except Exception as e:
        print(f"{Color.YELLOW}⚠️ Premium report generation failed: {e}{Color.END}\n")

    # Send summary email
    send_summary_email(results)

    print(f"{Color.CYAN}⏱️  Total execution time: {total_duration:.1f}s ({total_duration/60:.1f} minutes){Color.END}\n")
    
    # Return exit code (0 if all passed, 1 if any failed)
    exit_code = 1 if any(r['status'] in ['FAIL', 'ERROR'] for r in results) else 0
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
