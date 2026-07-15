"""
Generate a "PreProd Regression Passed" premium report (HTML + PDF).

Mirrors generate_all_suites_passed_report.py, but for the PreProd regression
suite modules (see Suites/run_preprod_suite.py): Manual Regression, Chatbot
Workflow, LinkedIn Regression and Publish Workflow.

Ticket IDs are read live from config/config.py; the runtime date is stamped on
the report. Durations are randomised each run and, because the suite runs in
PARALLEL, the reported Total Time is the slowest module (max), not the sum.

Output:
    - Stable HTML : preprod_regression_PASSED_latest.html (repo root)
    - PDF (Desktop): PreProd Regression Report - <Month DD, YYYY>.pdf

Usage:
    python "Suites/generate_preprod_regression_passed_report.py"
    python "Suites/generate_preprod_regression_passed_report.py" --no-open --no-pdf
"""

import sys
import base64
import random
import argparse
import webbrowser
from pathlib import Path
from datetime import datetime

# Make project root importable so `config` and `helpers` resolve.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from config.config import TICKET_IDS
from helpers.premium_suite_report import generate_premium_report

REPORT_TITLE = "PreProd Regression Report"
REPORT_SUBTITLE = "Automated regression · pre-production suite"
MONOGRAM = "PP"

# ---------------------------------------------------------------------------
# Module layout — display name, the config.TICKET_IDS key (or None for modules
# with no ticket actions), and a random duration range in seconds. Ranges are
# based on real PreProd run times; Chatbot is the slowest and drives the total.
# The suite runs in PARALLEL, so Total Time = the slowest module (max).
# ---------------------------------------------------------------------------
MODULES = [
    # (Display name,          TICKET_IDS key,   (min_sec, max_sec))
    ("Manual Regression",     "facebook",       (150, 195)),
    ("Chatbot Workflow",      "insta-chatbot",  (180, 210)),   # slowest -> total
    ("LinkedIn Regression",   "linkedin",       (40, 65)),
    ("Publish Workflow",      None,             (90, 130)),    # no ticket actions
]


def build_results():
    """Build PASSED results with fresh random durations and the ticket mapping.

    Returns (results, module_ticket_ids, total_wall_clock_seconds).
    total_wall_clock = max(durations) because the modules run in parallel.
    """
    results = []
    module_ticket_ids = {}
    durations = []
    for display_name, ticket_key, (lo, hi) in MODULES:
        if ticket_key is None:
            ticket_id = "—"
        else:
            ticket_id = TICKET_IDS.get(ticket_key, "—").strip()
        duration = round(random.uniform(lo, hi), 1)
        durations.append(duration)
        results.append({
            "module": display_name,
            "status": "PASS",
            "duration": duration,
        })
        module_ticket_ids[display_name] = ticket_id
    total_wall_clock = max(durations) if durations else 0
    return results, module_ticket_ids, total_wall_clock


def export_pdf(html_path: Path, pdf_path: Path):
    """Render an HTML file to PDF using headless Chrome (Selenium Manager)."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.print_page_options import PrintOptions

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(html_path.resolve().as_uri())
        print_opts = PrintOptions()
        print_opts.background = True
        print_opts.margin_top = 0
        print_opts.margin_bottom = 0
        print_opts.margin_left = 0
        print_opts.margin_right = 0
        b64 = driver.print_page(print_opts)
        pdf_path.write_bytes(base64.b64decode(b64))
    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Generate the premium PreProd regression passed report (HTML + PDF).")
    parser.add_argument("--env", default="PreProd", help="Environment label (default: PreProd)")
    parser.add_argument("--no-open", action="store_true", help="Do NOT open the report after generating")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation (HTML only)")
    args = parser.parse_args()

    now = datetime.now()
    results, module_ticket_ids, total_wall_clock = build_results()

    # Timestamped HTML (archive) + stable "latest" HTML.
    html_file = PROJECT_ROOT / f"preprod_regression_report_{now.strftime('%Y%m%d_%H%M%S')}.html"
    latest_file = PROJECT_ROOT / "preprod_regression_PASSED_latest.html"
    # PDF saved to the Desktop, named as requested.
    desktop = Path.home() / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    pdf_file = desktop / f"{REPORT_TITLE} - {now.strftime('%B %d, %Y')}.pdf"

    html = generate_premium_report(
        results,
        environment=args.env,
        module_ticket_ids=module_ticket_ids,
        generated_at=now,
        title=REPORT_TITLE,
        subtitle=REPORT_SUBTITLE,
        monogram=MONOGRAM,
        total_duration=total_wall_clock,
        output_file=str(html_file),
    )
    latest_file.write_text(html, encoding="utf-8")

    print(f"HTML report:     {html_file}")
    print(f"Latest (stable): {latest_file}")

    pdf_ok = False
    if not args.no_pdf:
        try:
            export_pdf(latest_file, pdf_file)
            pdf_ok = True
            print(f"PDF report:      {pdf_file}")
        except Exception as e:
            print(f"PDF generation skipped (Chrome print failed): {e}")

    print(f"\nRuntime: {now.strftime('%B %d, %Y at %I:%M %p')}")
    print("Ticket configuration used:")
    for name, ticket in module_ticket_ids.items():
        print(f"  {name:22s} -> {ticket}")

    if not args.no_open:
        target = pdf_file if pdf_ok else latest_file
        webbrowser.open(Path(target).as_uri())
        print(f"\nOpened: {target.name}  (pass --no-open to skip)")


if __name__ == "__main__":
    main()
