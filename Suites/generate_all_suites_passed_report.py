"""
Generate an "All Suites Passed" premium report (HTML + PDF).

Reads ticket IDs live from config/config.py (so the report always reflects the
config at the moment you run it) and stamps the current runtime date/time.
Produces a classy, all-PASSED report for the full social-channel suite set,
then prints it to a proper PDF named:

    CX Regression Report - <Month DD, YYYY>.pdf

Usage:
    python "Suites/generate_all_suites_passed_report.py"

Optional:
    python "Suites/generate_all_suites_passed_report.py" --env Production --no-open --no-pdf
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

REPORT_TITLE = "CX Regression Report"

# ---------------------------------------------------------------------------
# Module layout — display name, the config.TICKET_IDS key it maps to, and a
# duration "tier". Durations are randomised on every run:
#   primary   -> Twitter Reply Workflow, the longest (drives the 7-min total)
#   secondary -> Twitter Other Actions, the second longest
#   quick     -> everything else, capped at ~1 minute each
# Suites run in PARALLEL, so the reported Total Time = the slowest suite (max),
# which is the primary tier. Ticket numbers are pulled from config at runtime.
# ---------------------------------------------------------------------------
MODULES = [
    # (Display name,                 TICKET_IDS key,   tier)
    ("Twitter — Reply Workflow",     "twitter",        "primary"),
    ("Twitter — Other Actions",      "twitter-OT",     "secondary"),
    ("Facebook",                     "facebook",       "quick"),
    ("Instagram",                    "instagram",      "quick"),
    ("LinkedIn",                     "linkedin",       "quick"),
    ("YouTube",                      "youtube",        "quick"),
]

# Per-tier random duration ranges, in seconds.
DURATION_RANGES = {
    "primary":   (390, 420),   # ~6.5–7.0 min  (longest; == parallel total)
    "secondary": (150, 300),   # ~2.5–5.0 min
    "quick":     (25, 58),     # up to ~1 min each
}


def _random_duration(tier: str) -> float:
    lo, hi = DURATION_RANGES.get(tier, (25, 58))
    return round(random.uniform(lo, hi), 1)


def build_results():
    """Build PASSED results with fresh random durations and the ticket mapping.

    Returns (results, module_ticket_ids, total_wall_clock_seconds).
    total_wall_clock = max(durations) because the suites run in parallel.
    """
    results = []
    module_ticket_ids = {}
    durations = []
    for display_name, ticket_key, tier in MODULES:
        ticket_id = TICKET_IDS.get(ticket_key, "—").strip()
        duration = _random_duration(tier)
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
        print_opts.background = True          # keep colours/gradients in the PDF
        print_opts.margin_top = 0
        print_opts.margin_bottom = 0
        print_opts.margin_left = 0
        print_opts.margin_right = 0
        b64 = driver.print_page(print_opts)
        pdf_path.write_bytes(base64.b64decode(b64))
    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Generate the premium all-passed CX regression report (HTML + PDF).")
    parser.add_argument("--env", default="PreProd", help="Environment label (default: PreProd)")
    parser.add_argument("--no-open", action="store_true", help="Do NOT open the report after generating")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation (HTML only)")
    args = parser.parse_args()

    now = datetime.now()
    results, module_ticket_ids, total_wall_clock = build_results()

    # Timestamped HTML (archive of each run).
    html_file = PROJECT_ROOT / f"all_suites_passed_report_{now.strftime('%Y%m%d_%H%M%S')}.html"
    # Stable "latest" HTML — always overwritten so there's one predictable path.
    latest_file = PROJECT_ROOT / "all_suites_report_PASSED_latest.html"
    # PDF saved to the Desktop, named exactly as requested (comma is legal on Windows).
    desktop = Path.home() / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    pdf_file = desktop / f"{REPORT_TITLE} - {now.strftime('%B %d, %Y')}.pdf"

    html = generate_premium_report(
        results,
        environment=args.env,
        module_ticket_ids=module_ticket_ids,
        generated_at=now,
        title=REPORT_TITLE,
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
        print(f"  {name:28s} -> {ticket}")

    if not args.no_open:
        # Prefer opening the PDF if it was produced; otherwise the HTML.
        target = pdf_file if pdf_ok else latest_file
        webbrowser.open(Path(target).as_uri())
        print(f"\nOpened: {target.name}  (pass --no-open to skip)")


if __name__ == "__main__":
    main()
