"""
Premium Suite Report Generator.

Produces a refined, classy HTML report (light theme, generous whitespace,
tabular numerals, hairline detailing) that renders equally well on screen and
when printed to PDF via headless Chrome. Backgrounds are print-safe.
"""

import base64
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple


def _fmt_duration(seconds: float) -> str:
    seconds = float(seconds or 0)
    if seconds < 60:
        return f"{seconds:.0f}s"
    m, s = divmod(int(round(seconds)), 60)
    return f"{m}m {s:02d}s"


def generate_premium_report(
    results: List[Dict],
    environment: str = "PreProd",
    module_ticket_ids: Optional[Dict[str, str]] = None,
    generated_at: Optional[datetime] = None,
    title: str = "CX Regression Report",
    subtitle: str = "Automated regression · social channel suites",
    monogram: str = "CX",
    total_duration: Optional[float] = None,
    output_file: Optional[str] = None,
) -> str:
    """Build a premium HTML report string (and optionally write it to disk).

    total_duration: wall-clock time for the "Total Time" tile. Pass the parallel
    wall-clock (e.g. max of per-suite durations) here; if omitted it falls back
    to the serial sum of the per-suite durations.
    """
    module_ticket_ids = module_ticket_ids or {}
    now = generated_at or datetime.now()

    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = sum(1 for r in results if r.get("status") == "FAIL")
    skipped = sum(1 for r in results if r.get("status") in ("SKIP", "ERROR"))
    if total_duration is None:
        total_duration = sum(float(r.get("duration", 0) or 0) for r in results)
    success_rate = (passed / total * 100) if total else 0

    all_pass = failed == 0 and skipped == 0
    accent = "#0f9d6c" if all_pass else ("#c0392b" if failed else "#c07a1e")
    verdict = "All Suites Passed" if all_pass else ("Failures Detected" if failed else "Passed with Warnings")

    date_long = now.strftime("%B %d, %Y")

    # ---- rows ----
    rows = ""
    for i, r in enumerate(results):
        module = r.get("module", "—")
        status = r.get("status", "SKIP")
        duration = r.get("duration", 0)
        ticket = module_ticket_ids.get(module, "—")

        if status == "PASS":
            pill = '<span class="pill pill-pass">Passed</span>'
        elif status == "FAIL":
            pill = '<span class="pill pill-fail">Failed</span>'
        else:
            pill = '<span class="pill pill-skip">Skipped</span>'

        rows += f"""
            <tr>
                <td class="c-index">{i + 1:02d}</td>
                <td class="c-module">{module}</td>
                <td class="c-ticket">{ticket}</td>
                <td class="c-status">{pill}</td>
                <td class="c-duration">{_fmt_duration(duration)}</td>
            </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {date_long}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  :root {{
    --ink: #14161c;
    --ink-soft: #5b616e;
    --ink-faint: #9aa0ad;
    --line: #eceef1;
    --line-soft: #f4f5f7;
    --paper: #ffffff;
    --bg: #eef0f3;
    --accent: {accent};
  }}
  html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'Helvetica Neue', Arial, sans-serif;
    background: var(--bg);
    color: var(--ink);
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    padding: 48px 24px;
  }}
  .sheet {{
    max-width: 940px;
    margin: 0 auto;
    background: var(--paper);
    border-radius: 16px;
    box-shadow: 0 1px 2px rgba(16,22,38,0.04), 0 24px 60px -24px rgba(16,22,38,0.22);
    overflow: hidden;
  }}
  .accent-rule {{ height: 4px; background: linear-gradient(90deg, var(--accent), color-mix(in srgb, var(--accent) 55%, #000) 100%); }}

  /* Header */
  .head {{ padding: 40px 48px 32px; display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; }}
  .brand {{ display: flex; align-items: center; gap: 16px; }}
  .monogram {{
    width: 52px; height: 52px; border-radius: 13px; flex-shrink: 0;
    background: linear-gradient(140deg, #1b1e27, #3a3f4d);
    color: #fff; display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 17px; letter-spacing: 0.5px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.12);
  }}
  .titles h1 {{ font-size: 23px; font-weight: 650; letter-spacing: -0.4px; color: var(--ink); }}
  .titles p {{ font-size: 13px; color: var(--ink-soft); margin-top: 3px; }}
  .head-meta {{ text-align: right; flex-shrink: 0; }}
  .env-pill {{
    display: inline-block; font-size: 11px; font-weight: 600; letter-spacing: 0.6px;
    text-transform: uppercase; color: var(--ink-soft);
    background: var(--line-soft); border: 1px solid var(--line);
    padding: 6px 12px; border-radius: 999px;
  }}
  .head-meta .date {{ font-size: 13px; color: var(--ink); font-weight: 550; margin-top: 12px; }}
  .head-meta .time {{ font-size: 12px; color: var(--ink-faint); margin-top: 2px; }}

  /* Verdict band */
  .verdict {{
    margin: 0 48px; padding: 22px 26px; border-radius: 13px;
    background: color-mix(in srgb, var(--accent) 8%, #fff);
    border: 1px solid color-mix(in srgb, var(--accent) 22%, #fff);
    display: flex; align-items: center; justify-content: space-between; gap: 20px;
  }}
  .verdict-left {{ display: flex; align-items: center; gap: 16px; }}
  .check {{
    width: 42px; height: 42px; border-radius: 50%; flex-shrink: 0;
    background: var(--accent); color: #fff;
    display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700;
  }}
  .verdict-left h2 {{ font-size: 18px; font-weight: 640; color: var(--ink); letter-spacing: -0.2px; }}
  .verdict-left span {{ font-size: 12.5px; color: var(--ink-soft); }}
  .rate {{ text-align: right; }}
  .rate b {{ font-size: 30px; font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; letter-spacing: -0.5px; }}
  .rate small {{ display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.7px; color: var(--ink-faint); margin-top: 2px; }}

  /* Metrics */
  .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); margin: 30px 48px 8px; border: 1px solid var(--line); border-radius: 13px; overflow: hidden; }}
  .metric {{ padding: 22px 24px; border-right: 1px solid var(--line); }}
  .metric:last-child {{ border-right: none; }}
  .metric .k {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.7px; color: var(--ink-faint); font-weight: 600; }}
  .metric .v {{ font-size: 28px; font-weight: 700; letter-spacing: -0.6px; margin-top: 8px; font-variant-numeric: tabular-nums; color: var(--ink); }}
  .metric .v.pass {{ color: var(--accent); }}

  /* Table */
  .section {{ padding: 26px 48px 8px; }}
  .section-title {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.9px; color: var(--ink-faint); font-weight: 700; margin-bottom: 14px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  thead th {{
    text-align: left; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.8px;
    color: var(--ink-faint); font-weight: 700; padding: 0 16px 12px; border-bottom: 1px solid var(--line);
  }}
  thead th.c-duration, tbody td.c-duration {{ text-align: right; }}
  tbody td {{ padding: 16px; border-bottom: 1px solid var(--line-soft); font-size: 14px; vertical-align: middle; }}
  tbody tr:last-child td {{ border-bottom: none; }}
  .c-index {{ color: var(--ink-faint); font-variant-numeric: tabular-nums; font-size: 12.5px; width: 44px; }}
  .c-module {{ font-weight: 600; color: var(--ink); }}
  .c-ticket {{ font-family: 'SF Mono', 'JetBrains Mono', 'Menlo', 'Consolas', monospace; font-size: 13px; color: var(--ink-soft); }}
  .c-duration {{ font-variant-numeric: tabular-nums; color: var(--ink-soft); font-size: 13px; }}
  .pill {{ display: inline-flex; align-items: center; gap: 7px; padding: 5px 12px; border-radius: 999px; font-size: 12px; font-weight: 600; }}
  .pill::before {{ content: ''; width: 7px; height: 7px; border-radius: 50%; }}
  .pill-pass {{ background: #e7f6ee; color: #0b7a53; }}
  .pill-pass::before {{ background: #0f9d6c; }}
  .pill-fail {{ background: #fbeaea; color: #a02b23; }}
  .pill-fail::before {{ background: #c0392b; }}
  .pill-skip {{ background: #fdf3e3; color: #9a6516; }}
  .pill-skip::before {{ background: #c07a1e; }}

  /* Footer */
  .foot {{ margin-top: 20px; padding: 24px 48px 34px; border-top: 1px solid var(--line); display: flex; justify-content: space-between; align-items: center; }}
  .foot .fl {{ font-size: 12.5px; color: var(--ink-soft); }}
  .foot .fl b {{ color: var(--ink); font-weight: 600; }}
  .foot .fr {{ font-size: 11.5px; color: var(--ink-faint); }}

  @page {{ size: A4; margin: 12mm; }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .sheet {{ box-shadow: none; border-radius: 0; max-width: 100%; }}
    tbody tr {{ page-break-inside: avoid; }}
    /* Compact spacing so the whole report fits on one page. */
    .head {{ padding: 22px 40px 16px; }}
    .verdict {{ margin: 0 40px; padding: 16px 22px; }}
    .metrics {{ margin: 20px 40px 4px; }}
    .metric {{ padding: 15px 22px; }}
    .metric .v {{ font-size: 25px; }}
    .section {{ padding: 18px 40px 4px; }}
    tbody td {{ padding: 11px 16px; }}
    .foot {{ margin-top: 14px; padding: 16px 40px 20px; }}
  }}
</style>
</head>
<body>
  <div class="sheet">
    <div class="accent-rule"></div>

    <div class="head">
      <div class="brand">
        <div class="monogram">{monogram}</div>
        <div class="titles">
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
      </div>
      <div class="head-meta">
        <span class="env-pill">{environment} Environment</span>
        <div class="date">{date_long}</div>
      </div>
    </div>

    <div class="verdict">
      <div class="verdict-left">
        <div class="check">{'&#10003;' if all_pass else '!'}</div>
        <div>
          <h2>{verdict}</h2>
          <span>{passed} of {total} suites passed · executed {date_long}</span>
        </div>
      </div>
      <div class="rate">
        <b>{success_rate:.0f}%</b>
        <small>Success rate</small>
      </div>
    </div>

    <div class="metrics">
      <div class="metric"><div class="k">Passed</div><div class="v pass">{passed}</div></div>
      <div class="metric"><div class="k">Failed</div><div class="v">{failed}</div></div>
      <div class="metric"><div class="k">Suites</div><div class="v">{total}</div></div>
      <div class="metric"><div class="k">Total Time</div><div class="v">{_fmt_duration(total_duration)}</div></div>
    </div>

    <div class="section">
      <div class="section-title">Suite Results</div>
      <table>
        <thead>
          <tr>
            <th class="c-index">#</th>
            <th>Suite</th>
            <th>Ticket ID</th>
            <th>Status</th>
            <th class="c-duration">Duration</th>
          </tr>
        </thead>
        <tbody>{rows}
        </tbody>
      </table>
    </div>

    <div class="foot">
      <div class="fl"><b>LocoBuzz Automation</b> — Quality Assurance &amp; Testing</div>
      <div class="fr">Generated {date_long}</div>
    </div>
  </div>
</body>
</html>"""

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

    return html


def export_pdf(html_path: Path, pdf_path: Path) -> None:
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
        driver.get(Path(html_path).resolve().as_uri())
        print_opts = PrintOptions()
        print_opts.background = True          # keep colours in the PDF
        print_opts.margin_top = 0
        print_opts.margin_bottom = 0
        print_opts.margin_left = 0
        print_opts.margin_right = 0
        b64 = driver.print_page(print_opts)
        Path(pdf_path).write_bytes(base64.b64decode(b64))
    finally:
        driver.quit()


def save_premium_report(
    results: List[Dict],
    environment: str,
    module_ticket_ids: Dict[str, str],
    title: str,
    subtitle: str,
    monogram: str,
    total_duration: float,
    html_dir: Path,
    latest_name: str,
    pdf_dir: Optional[Path] = None,
    generated_at: Optional[datetime] = None,
) -> Tuple[Path, Optional[Path]]:
    """Write the premium HTML report and print it to PDF.

    Returns (html_path, pdf_path_or_None). PDF failures are non-fatal — the HTML
    is always written, so a missing Chrome never breaks a suite run.

    total_duration should be the PARALLEL wall-clock time of the run, not the
    sum of the per-module durations.
    """
    now = generated_at or datetime.now()
    html_dir = Path(html_dir)
    pdf_dir = Path(pdf_dir) if pdf_dir else (Path.home() / "Desktop")

    latest_path = html_dir / latest_name
    html = generate_premium_report(
        results,
        environment=environment,
        module_ticket_ids=module_ticket_ids,
        generated_at=now,
        title=title,
        subtitle=subtitle,
        monogram=monogram,
        total_duration=total_duration,
        output_file=str(latest_path),
    )

    pdf_path = None
    try:
        pdf_dir.mkdir(parents=True, exist_ok=True)
        candidate = pdf_dir / f"{title} - {now.strftime('%B %d, %Y')}.pdf"
        export_pdf(latest_path, candidate)
        pdf_path = candidate
    except Exception as e:
        print(f"PDF generation skipped (Chrome print failed): {e}")

    return latest_path, pdf_path
