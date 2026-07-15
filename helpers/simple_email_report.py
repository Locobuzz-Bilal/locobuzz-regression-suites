from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Iterable, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE_PATH = PROJECT_ROOT / "helpers" / "simple_email_report.html"


@dataclass(frozen=True)
class SimpleResultRow:
    index: int
    script_name: str
    status: str
    duration_seconds: float
    retries: int = 0


def _status_badge_html(status: str) -> str:
    s = (status or "").strip().upper()
    if s in {"PASS", "PASSED", "SUCCESS"}:
        return '<span class="status status-passed">PASSED</span>'
    if s in {"FAIL", "FAILED", "ERROR"}:
        return '<span class="status status-failed">FAILED</span>'
    return '<span class="status status-skipped">SKIPPED</span>'


def _row_html(row: SimpleResultRow) -> str:
    return (
        f'<tr>'
        f'<td style="text-align: center; font-weight: 500;">{row.index}</td>'
        f'<td style="font-weight: 500;">{escape(row.script_name)}</td>'
        f'<td>{_status_badge_html(row.status)}</td>'
        f'<td style="font-family: monospace;">{row.duration_seconds:.1f}s</td>'
        f'<td style="text-align: center;">{row.retries}</td>'
        f'</tr>'
    )


def _render(template: str, values: Mapping[str, str], *, html_safe_keys: set[str]) -> str:
    rendered = template
    for key, value in values.items():
        token = "{{" + key + "}}"
        if key in html_safe_keys:
            rendered = rendered.replace(token, value or "")
        else:
            rendered = rendered.replace(token, escape(value or ""))
    return rendered


def build_simple_email_html(
    *,
    suite_title: str,
    environment: str,
    rows: Iterable[SimpleResultRow],
    total_duration_seconds: float,
    generated_at: str | None = None,
    template_path: Path = DEFAULT_TEMPLATE_PATH,
) -> str:
    rows_list = list(rows)
    total = len(rows_list)

    passed = sum(1 for r in rows_list if (r.status or "").strip().upper() in {"PASS", "PASSED", "SUCCESS"})
    failed = sum(1 for r in rows_list if (r.status or "").strip().upper() in {"FAIL", "FAILED", "ERROR"})
    skipped = max(0, total - passed - failed)

    success_rate = (passed / total * 100.0) if total else 0.0
    avg_duration = (total_duration_seconds / total) if total else 0.0

    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
    generated_at = generated_at or datetime.now().strftime("%B %d, %Y %H:%M:%S")

    result_rows_html = "".join(_row_html(r) for r in rows_list)
    if not result_rows_html:
        result_rows_html = (
            '<tr>'
            '<td colspan="5" style="text-align: center; color: #666; font-style: italic;">No results.</td>'
            '</tr>'
        )

    template = template_path.read_text(encoding="utf-8")
    values = {
        "SUITE_TITLE": suite_title,
        "ENVIRONMENT": environment,
        "TIMESTAMP": timestamp,
        "TOTAL_TESTS": str(total),
        "PASSED_TESTS": str(passed),
        "FAILED_TESTS": str(failed),
        "TOTAL_DURATION": f"{total_duration_seconds:.1f}s",
        "SUCCESS_RATE": f"{success_rate:.1f}",
        "AVG_DURATION": f"{avg_duration:.1f}s",
        "RESULT_ROWS": result_rows_html,
        "GENERATED_AT": generated_at,
    }

    return _render(template, values, html_safe_keys={"RESULT_ROWS"})</content>
<parameter name="filePath">c:\Users\admin\Desktop\New Clone\locobuzz-regression-automation\helpers\simple_email_report.html