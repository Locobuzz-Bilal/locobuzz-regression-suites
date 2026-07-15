from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Iterable, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE_PATH = Path(__file__).resolve().parent / "email_report_template_optimized.html"


@dataclass(frozen=True)
class EnterpriseResultRow:
    index: int
    name: str
    reference: str
    status: str
    duration_seconds: float
    details: str = ""


@dataclass(frozen=True)
class SuiteResultRow:
    suite_name: str
    status: str
    duration: str
    passed: int
    failed: int
    total: int


def _status_chip_html(status: str) -> str:
    s = (status or "").strip().upper()
    if s in {"PASS", "PASSED", "SUCCESS"}:
        return (
            '<span style="background: rgba(16, 185, 129, 0.18); color: #34d399; '
            'padding: 7px 14px; border-radius: 999px; font-weight: 800; font-size: 11px; '
            'letter-spacing: 0.6px; border: 1px solid rgba(16, 185, 129, 0.35);">'
            "PASSED"
            "</span>"
        )
    if s in {"FAIL", "FAILED", "ERROR"}:
        return (
            '<span style="background: rgba(239, 68, 68, 0.18); color: #fca5a5; '
            'padding: 7px 14px; border-radius: 999px; font-weight: 800; font-size: 11px; '
            'letter-spacing: 0.6px; border: 1px solid rgba(239, 68, 68, 0.35);">'
            "FAILED"
            "</span>"
        )
    return (
        '<span style="background: rgba(245, 158, 11, 0.18); color: #fcd34d; '
        'padding: 7px 14px; border-radius: 999px; font-weight: 800; font-size: 11px; '
        'letter-spacing: 0.6px; border: 1px solid rgba(245, 158, 11, 0.35);">'
        "SKIPPED"
        "</span>"
    )


def _row_html(row: EnterpriseResultRow, *, stripe: bool) -> str:
    bg = "rgba(39, 39, 42, 0.60)" if stripe else "rgba(24, 24, 27, 0.60)"
    reference = row.reference or "—"
    details = row.details or "—"
    return (
        f'<tr style="background: {bg};">'
        f'<td style="padding: 16px 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); color: #a1a1aa; font-weight: 700;">{row.index}</td>'
        f'<td style="padding: 16px 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.06);">'
        f'<div style="color: #f4f4f5; font-weight: 700; margin-bottom: 5px;">{escape(row.name)}</div>'
        "</td>"
        f'<td style="padding: 16px 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.06);">'
        f'<span style="font-family: \'Courier New\', monospace; font-size: 12px; color: #7dd3fc; background: rgba(14, 165, 233, 0.14); padding: 5px 9px; border-radius: 6px; border-left: 3px solid #0ea5e9;">{escape(reference)}</span>'
        "</td>"
        f'<td align="center" style="padding: 16px 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.06);">{_status_chip_html(row.status)}</td>'
        f'<td align="center" style="padding: 16px 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); font-weight: 700; color: #e4e4e7; font-family: \'Courier New\', monospace;">{row.duration_seconds:.1f}s</td>'
        f'<td style="padding: 16px 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); color: #cbd5e1; font-size: 13px;">{escape(details)}</td>'
        "</tr>"
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


def build_enterprise_email_html(
    *,
    suite_title: str,
    suite_subtitle: str,
    environment: str,
    rows: Iterable[EnterpriseResultRow],
    total_duration_seconds: float,
    generated_at: str | None = None,
    run_by: str | None = None,
    config_title: str = "Execution Configuration",
    config_rows_html: str = "",
    template_path: Path = DEFAULT_TEMPLATE_PATH,
) -> str:
    rows_list = list(rows)
    total = len(rows_list)

    passed = sum(1 for r in rows_list if (r.status or "").strip().upper() in {"PASS", "PASSED", "SUCCESS"})
    failed = sum(1 for r in rows_list if (r.status or "").strip().upper() in {"FAIL", "FAILED", "ERROR"})
    skipped = max(0, total - passed - failed)

    success_pct = (passed / total * 100.0) if total else 0.0
    avg_duration = (total_duration_seconds / total) if total else 0.0

    if failed == 0 and skipped == 0:
        status_text = "ALL SYSTEMS PASSED"
        status_label = "OPERATIONAL"
        status_accent = "#10b981"
    elif failed == 0:
        status_text = "PASSED WITH WARNINGS"
        status_label = "ATTENTION"
        status_accent = "#f59e0b"
    else:
        status_text = "SOME TESTS FAILED"
        status_label = "ATTENTION"
        status_accent = "#ef4444"

    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S IST")
    generated_at = generated_at or datetime.now().strftime("%B %d, %Y %H:%M:%S IST")
    run_by = run_by or "Automation"

    # Executive summary is HTML-safe because it includes inline styles.
    exec_summary_html = (
        f"The suite completed with <strong style=\"color: #ffffff; background: {status_accent}; padding: 2px 7px; border-radius: 4px;\">{escape(status_text)}</strong>. "
        f"<strong style=\"color: #0ea5e9;\">{total}</strong> items executed with "
        f"<strong style=\"color: {status_accent};\">{success_pct:.0f}%</strong> success, "
        f"total duration <strong style=\"color: #0ea5e9;\">{total_duration_seconds:.1f}s</strong>. "
        f"Failures: <strong style=\"color: {status_accent};\">{failed}</strong>, skipped: <strong style=\"color: #a1a1aa;\">{skipped}</strong>."
    )

    if not config_rows_html:
        config_rows_html = (
            f"<tr><td style=\"padding: 5px 0; color: #a1a1aa; font-size: 13px; width: 35%;\">Suite:</td>"
            f"<td style=\"padding: 5px 0; color: #bae6fd; font-size: 13px; font-weight: 600; font-family: 'Courier New', monospace;\">{escape(suite_title)}</td></tr>"
            f"<tr><td style=\"padding: 5px 0; color: #a1a1aa; font-size: 13px;\">Environment:</td>"
            f"<td style=\"padding: 5px 0; color: #bae6fd; font-size: 13px; font-weight: 600; font-family: 'Courier New', monospace;\">{escape(environment)}</td></tr>"
        )

    result_rows_html = "".join(_row_html(r, stripe=(i % 2 == 0)) for i, r in enumerate(rows_list))
    if not result_rows_html:
        result_rows_html = (
            '<tr style="background: rgba(24, 24, 27, 0.60);">'
            '<td colspan="6" style="padding: 18px 14px; color: #a1a1aa; text-align: center;">No results.</td>'
            "</tr>"
        )

    duration_minutes = f"{(total_duration_seconds / 60.0):.1f} minutes"
    pass_rate_label = f"{success_pct:.0f}% success"
    failed_label = "No failures" if failed == 0 else f"{failed} failures"

    template = template_path.read_text(encoding="utf-8")
    values = {
        "SUITE_TITLE": suite_title,
        "SUITE_SUBTITLE": suite_subtitle,
        "ENVIRONMENT": environment,
        "STATUS_LABEL": status_label,
        "STATUS_ACCENT": status_accent,
        "STATUS_TEXT": status_text,
        "TIMESTAMP": timestamp,
        "SUCCESS_PERCENTAGE": f"{success_pct:.0f}",
        "EXEC_SUMMARY_HTML": exec_summary_html,
        "CONFIG_TITLE": config_title,
        "CONFIG_ROWS": config_rows_html,
        "DURATION_SECONDS": f"{total_duration_seconds:.1f}s",
        "DURATION_MINUTES": duration_minutes,
        "PASSED_TESTS": str(passed),
        "FAILED_TESTS": str(failed),
        "PASS_RATE": f"{success_pct:.0f}%",
        "PASS_RATE_LABEL": pass_rate_label,
        "FAILED_LABEL": failed_label,
        "AVG_DURATION": f"{avg_duration:.1f}s",
        "RETRIES": "0",
        "RESULT_ROWS": result_rows_html,
        "GENERATED_AT": generated_at,
        "RUN_BY": run_by,
    }

    return _render(template, values, html_safe_keys={"EXEC_SUMMARY_HTML", "CONFIG_ROWS", "RESULT_ROWS"})


def build_suite_regression_email_html(
    *,
    environment: str,
    suite_results: Iterable[SuiteResultRow],
    total_duration: str,
    avg_duration: str,
    template_path: Path = DEFAULT_TEMPLATE_PATH,
) -> str:
    """Build HTML email for all suite regression report."""
    suite_list = list(suite_results)
    total_suites = len(suite_list)
    passed_suites = sum(1 for s in suite_list if (s.status or "").strip().upper() in {"PASS", "PASSED", "SUCCESS"})
    failed_suites = total_suites - passed_suites
    success_rate = (passed_suites / total_suites * 100) if total_suites > 0 else 0

    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S IST")

    # Generate suite rows HTML
    suite_rows_html = ""
    for suite in suite_list:
        status_class = "status-passed" if suite.status.upper() in {"PASS", "PASSED", "SUCCESS"} else "status-failed"
        status_badge = f'<span class="badge badge-passed">PASSED</span>' if suite.status.upper() in {"PASS", "PASSED", "SUCCESS"} else f'<span class="badge badge-failed">FAILED</span>'

        suite_rows_html += f'<tr><td>{escape(suite.suite_name)}</td><td class="{status_class}">{status_badge}</td><td>{escape(suite.duration)}</td><td>{suite.passed}</td><td>{suite.failed}</td><td>{suite.total}</td></tr>'

    template = template_path.read_text(encoding="utf-8")
    values = {
        "TIMESTAMP": timestamp,
        "ENVIRONMENT": environment,
        "TOTAL_SUITES": str(total_suites),
        "PASSED_SUITES": str(passed_suites),
        "FAILED_SUITES": str(failed_suites),
        "SUCCESS_RATE": f"{success_rate:.0f}",
        "SUITE_ROWS": suite_rows_html,
        "TOTAL_DURATION": total_duration,
        "AVG_DURATION": avg_duration,
    }

    return _render(template, values, html_safe_keys={"SUITE_ROWS"})
