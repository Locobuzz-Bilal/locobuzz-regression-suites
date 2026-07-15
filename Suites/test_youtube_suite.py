
import os
import sys
import time
import glob
import shutil
import json
import re
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from helpers.enterprise_email_report import EnterpriseResultRow, build_enterprise_email_html

# ----- .env loader -----
def _load_dotenv():
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
_load_dotenv()

# ----- Email -----
try:
    import yagmail
except ImportError:
    yagmail = None
    print("Install: pip install yagmail")

# Display name and safe folder name
MODULE_NAME_DISPLAY = "YouTube"
def _slug(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '_', s).strip('_').lower()
SAFE_MODULE_FOLDER = _slug(MODULE_NAME_DISPLAY)

MODULE_NAME = "Regression - YouTube Reply Workflow"
today_str = time.strftime("%d-%b-%Y").upper()

def get_next_run_folder(base_dir: Path) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    runs = sorted(glob.glob(str(base_dir / "run_*")))
    if not runs: return base_dir / "run_1"
    num = int(runs[-1].split("_")[-1])
    return base_dir / f"run_{num+1}"

def format_duration(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{s:06.3f}"

def _normalize_fullname(fn: str) -> str:
    if not fn: return ""
    parts = fn.split(".")
    if len(parts) < 2: return fn
    test_name = parts[-1]
    file_name = parts[-2] + ".py"
    path_parts = parts[:-2]
    return str(Path(*path_parts) / file_name) + "::" + test_name

# ----- Timing plugin -----
class TimingCollector:
    def __init__(self):
        self.items = {}
    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            rec = self.items.get(report.nodeid, {"retries":0})
            if "duration" in rec:
                rec["retries"] += 1
            rec["duration"] = report.duration
            rec["outcome"] = report.outcome
            self.items[report.nodeid] = rec

# ----- Allure parsing -----
def _parse_allure_results(results_dir: Path):
    out = {}
    for f in results_dir.glob("*-result.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            dotted = data.get("fullName","")
            labels = {l.get("name"): l.get("value") for l in data.get("labels", []) if isinstance(l, dict)}
            script = labels.get("testClass","") or labels.get("package","")
            method = labels.get("testMethod","") or data.get("name","")
            path_style = _normalize_fullname(dotted)
            out[path_style] = {"script": script, "method": method}
        except Exception as e:
            print("Allure parse fail:", e)
    return out

# ----- Email HTML -----
def build_email_html(module, date_str, total_run, report_dir: Path, exit_code: int, results_dir: Path, timing: TimingCollector):
    meta_map = _parse_allure_results(results_dir)
    rows = []
    for nodeid, info in timing.items.items():
        meta = meta_map.get(nodeid, {})
        script = meta.get("script") or Path(nodeid.split("::")[0]).name.replace(".py","")
        name = meta.get("method") or nodeid.split("::")[-1]
        rows.append({
            "script": script,
            "name": name,
            "status": info["outcome"],
            "duration_s": info["duration"],
            "retries": info["retries"]
        })

    total = len(rows)
    passed  = sum(r["status"]=="passed" for r in rows)
    failed  = sum(r["status"]=="failed" for r in rows)
    skipped = sum(r["status"]=="skipped" for r in rows)
    broken  = 0
    avg     = (sum(r["duration_s"] for r in rows)/total) if total else 0.0
    status_txt = "PASS" if (exit_code==0 and failed==0 and total>0) else "FAIL"
    color = "#146c43" if status_txt=="PASS" else "#c0342e"

    status_colors = {"passed":"#146c43","failed":"#c0342e","skipped":"#666"}
    widths = {"idx":"55px","script":"230px","name":"270px","status":"120px","dur":"150px","retry":"80px"}

    def cell_style(base_width, extra=""):
        return f"border:1px solid #d0d0d0;padding:7px 10px;vertical-align:middle;width:{base_width};{extra}"
    def chip(st):
        c = status_colors.get(st,"#444")
        return f"<span style='display:inline-block;background:{c}15;color:{c};padding:2px 9px;border-radius:12px;font-size:11px;font-weight:600'>{st.upper()}</span>"

    body_html = []
    for i,r in enumerate(sorted(rows, key=lambda x: (x["script"], x["name"]))):
        body_html.append(
            "<tr>"
            f"<td style='{cell_style(widths['idx'],'text-align:center;font-weight:600;color:#555')}'>{i+1}</td>"
            f"<td style='{cell_style(widths['script'])}' title='{r['script']}'>{r['script']}</td>"
            f"<td style='{cell_style(widths['name'])}' title='{r['name']}'>{r['name']}</td>"
            f"<td style='{cell_style(widths['status'],'text-align:center')}'>{chip(r['status'])}</td>"
            f"<td style='{cell_style(widths['dur'],'font-family:Consolas,monospace')}'>{format_duration(r['duration_s'])}</td>"
            f"<td style='{cell_style(widths['retry'],'text-align:center')}'>{r['retries']}</td>"
            "</tr>"
        )
    if not body_html:
        body_html.append(f"<tr><td colspan='6' style='{cell_style('100%','text-align:center')}'><em>No tests executed.</em></td></tr>")

    header = (
        "<tr style='background:#f3f3f3'>"
        f"<th style='{cell_style(widths['idx'],'text-align:center;font-weight:600')}'><span>#</span></th>"
        f"<th style='{cell_style(widths['script'],'text-align:left;font-weight:600')}'><span>Script</span></th>"
        f"<th style='{cell_style(widths['name'],'text-align:left;font-weight:600')}'><span>Test</span></th>"
        f"<th style='{cell_style(widths['status'],'text-align:center;font-weight:600')}'><span>Status</span></th>"
        f"<th style='{cell_style(widths['dur'],'text-align:left;font-weight:600')}'><span>Duration</span></th>"
        f"<th style='{cell_style(widths['retry'],'text-align:center;font-weight:600')}'><span>Retries</span></th>"
        "</tr>"
    )

    html = f"""
    <html>
    <body style="font-family:Segoe UI,Arial,sans-serif;margin:16px;color:#222">
      <h2 style="margin:0 0 6px;font-weight:600;color:{color}">{module} Suite {status_txt}</h2>
      <div style="font-size:13px;margin:4px 0 14px;line-height:1.5">
        <strong>Total Run:</strong> {format_duration(total_run)} |
        Date {date_str} |
        Total {total} |
        <span style='color:#146c43;font-weight:600'>Passed {passed}</span> |
        <span style='color:#c0342e;font-weight:600'>Failed {failed}</span> |
        Broken {broken} | Skipped {skipped} |
        Avg/Test {avg:.2f}s
      </div>
      <table style="border-collapse:collapse;border:1px solid #c8c8c8;font-size:12.5px;table-layout:fixed">
        <thead>{header}</thead>
        <tbody>{''.join(body_html)}</tbody>
      </table>
      <div style="font-size:11px;color:#666;margin-top:12px">
        Results: {results_dir}<br>Report: {report_dir}
      </div>
    </body>
    </html>
    """
    return html

# ----- Send Email -----
def send_email_html(report_dir: Path, results_dir: Path, duration: float, exit_code: int, timing: TimingCollector):
    sender = os.getenv("EMAIL_USER"); pwd = os.getenv("EMAIL_PASS")
    tos = [t.strip() for t in os.getenv("EMAIL_TO","").split(",") if t.strip()]
    if not (sender and pwd and tos) or yagmail is None:
        print("Email skipped."); return

    meta_map = _parse_allure_results(results_dir)
    rows: list[EnterpriseResultRow] = []
    for idx, (nodeid, info) in enumerate(sorted(timing.items.items(), key=lambda kv: kv[0]), 1):
        meta = meta_map.get(nodeid, {})
        script = meta.get("script") or Path(nodeid.split("::")[0]).name.replace(".py", "")
        name = meta.get("method") or nodeid.split("::")[-1]

        outcome = (info.get("outcome") or "").lower()
        status = "PASS" if outcome == "passed" else "FAIL" if outcome in {"failed", "broken", "error"} else "SKIP"
        duration_s = float(info.get("duration") or 0.0)
        retries = int(info.get("retries") or 0)
        rows.append(
            EnterpriseResultRow(
                index=idx,
                name=str(name or "—"),
                reference=str(script or "—"),
                status=status,
                duration_seconds=duration_s,
                details=f"Retries: {retries}",
            )
        )

    environment = os.getenv("REPORT_ENVIRONMENT") or os.getenv("ENVIRONMENT") or "CX"
    config_rows_html = (
        f"<tr><td style=\"padding: 5px 0; color: #a1a1aa; font-size: 13px; width: 35%;\">Results:</td>"
        f"<td style=\"padding: 5px 0; color: #bae6fd; font-size: 13px; font-weight: 600; font-family: 'Courier New', monospace;\">{results_dir}</td></tr>"
        f"<tr><td style=\"padding: 5px 0; color: #a1a1aa; font-size: 13px;\">Report:</td>"
        f"<td style=\"padding: 5px 0; color: #bae6fd; font-size: 13px; font-weight: 600; font-family: 'Courier New', monospace;\">{report_dir}</td></tr>"
    )

    html = build_enterprise_email_html(
        suite_title="Enterprise Test Execution Report",
        suite_subtitle=f"{MODULE_NAME_DISPLAY} • Automated Regression",
        environment=environment,
        rows=rows,
        total_duration_seconds=float(duration or 0.0),
        run_by=os.getenv("REPORT_RUN_BY") or "Automation",
        config_title="Execution Configuration",
        config_rows_html=config_rows_html,
    )

    subject = f"{MODULE_NAME_DISPLAY} Suite {today_str}"
    try:
        yagmail.SMTP(sender, pwd).send(to=tos, subject=subject, contents=[html])
        print("✅ Email sent.")
    except Exception as e:
        print("❌ Email failed:", e)

def get_next_run_folder(base_dir: Path) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    runs = sorted(glob.glob(str(base_dir / "run_*")))
    if not runs: return base_dir / "run_1"
    num = int(runs[-1].split("_")[-1])
    return base_dir / f"run_{num+1}"

# Allure directories
base_results = PROJECT_ROOT / "Suites" / "allure-results" / MODULE_NAME / today_str
base_report  = PROJECT_ROOT / "Suites" / "allure-report" / MODULE_NAME / today_str
results_dir = get_next_run_folder(base_results)
report_dir  = base_report / f"report_{results_dir.name}"

if results_dir.exists():
    shutil.rmtree(results_dir, ignore_errors=True)
results_dir.mkdir(parents=True, exist_ok=True)
report_dir.mkdir(parents=True, exist_ok=True)

print(f"✅ Results folder: {results_dir}")
print(f"✅ Report folder : {report_dir}")

# Selenium scripts (youtube)
SELENIUM_SCRIPTS = [
    # "tests/selenium/youtube/test_reply_and_assign.py",
    # "tests/selenium/youtube/test_reply_and_await.py",
    # "tests/selenium/youtube/test_reply_and_onHold.py",
    # "tests/selenium/youtube/test_reply_and_escalate.py",
    # "tests/selenium/youtube/test_csd_approve.py",
    # "tests/selenium/youtube/test_reply_and_close.py",
    # "tests/selenium/youtube/test_otherActions_openTicket.py",
    # "tests/selenium/youtube/test_otherActions_closedTicket.py"

    "tests/selenium/youtube/test_youtube_regression.py"
]

def run_suite():
    print(f"\nRunning {MODULE_NAME} suite for {today_str}\n")
    start = time.time()

    timing = TimingCollector()

    cache_dir = PROJECT_ROOT / ".pytest_cache" / SAFE_MODULE_FOLDER
    pytest_args = [
        *SELENIUM_SCRIPTS,
        "-v", "-s", "--tb=short", "--cache-clear",
        "--reruns", "2", "--reruns-delay", "2",
        f"--alluredir={results_dir}",
        "-o", f"cache_dir={cache_dir}",
    ]

    exit_code = pytest.main(pytest_args, plugins=[timing])

    print("\nGenerating Allure report...")
    os.system(f'allure generate "{results_dir}" --clean -o "{report_dir}"')

    duration = time.time() - start
    send_email_html(report_dir, results_dir, duration, exit_code, timing)

    status = "PASS" if exit_code == 0 else "FAIL"
    print(f"\nSummary:\nModule: {MODULE_NAME}\nDate: {today_str}\nStatus: {status}\nDuration: {duration:.1f}s")
    print(f"Results Dir: {results_dir}")
    print(f"Report Dir : {report_dir}")
    print("Suite PASS" if exit_code == 0 else "Suite FAIL")
    
    return exit_code

if __name__ == "__main__":
    run_suite()
