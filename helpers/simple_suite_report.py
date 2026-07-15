"""
Simple Suite Report Generator
Creates clean, easy-to-read HTML reports for suite execution
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict


def generate_simple_suite_report(
    results: List[Dict],
    environment: str = "PreProd",
    output_file: str = None,
    module_ticket_ids: Dict[str, str] = None
) -> str:
    """
    Generate a simple, clean HTML report for suite execution

    Args:
        results: List of result dictionaries with keys: module, status, duration
        environment: Environment name (PreProd, CX, etc.)
        output_file: Optional path to save the report
        module_ticket_ids: Optional {module_name: ticket_ref} mapping. When
            supplied, a "Ticket Reference" column is added to the suite table.

    Returns:
        HTML string
    """
    module_ticket_ids = module_ticket_ids or {}
    show_ticket_col = bool(module_ticket_ids)
    
    # Calculate stats
    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    skipped = sum(1 for r in results if r['status'] in ['SKIP', 'ERROR'])
    
    total_duration = sum(r.get('duration', 0) for r in results)
    success_rate = (passed / total * 100) if total > 0 else 0
    
    # Determine overall status
    if failed == 0 and skipped == 0:
        overall_status = "All Tests Passed"
        status_color = "#27ae60"
    elif failed == 0:
        overall_status = "Passed with Warnings"
        status_color = "#e67e22"
    else:
        overall_status = "Tests Failed"
        status_color = "#c0392b"
    
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    report_date = datetime.now().strftime("%B %d, %Y")

    # Build suite rows
    suite_rows = ""
    for result in results:
        module = result.get('module', 'Unknown')
        status = result.get('status', 'SKIP')
        duration = result.get('duration', 0)

        if status == 'PASS':
            status_html = '<span class="status-cell status-pass">Passed</span>'
        elif status == 'FAIL':
            status_html = '<span class="status-cell status-fail">Failed</span>'
        else:
            status_html = '<span class="status-cell status-skip">Skipped</span>'

        ticket_cell = ""
        if show_ticket_col:
            ticket_ref = module_ticket_ids.get(module, "—")
            ticket_cell = f'<td class="ticket-ref">{ticket_ref}</td>'

        suite_rows += f'''
        <tr>
            <td><div class="suite-name">{module}</div></td>
            {ticket_cell}
            <td>{status_html}</td>
            <td class="suite-duration">{duration:.1f}s</td>
        </tr>
        '''

    ticket_th = '<th>Ticket Reference</th>' if show_ticket_col else ''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Suite Execution Report - {environment}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            background: #f0f2f5;
            padding: 40px 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 1px 3px rgba(0, 0, 0, 0.06);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 40px 50px;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 400px;
            height: 100%;
            background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 100%);
            transform: skewX(-15deg);
            transform-origin: top right;
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        .header h1 {{
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        
        .header-meta {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin-top: 12px;
            font-size: 14px;
            opacity: 0.85;
        }}
        
        .header-meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .header-meta-item::before {{
            content: '';
            width: 4px;
            height: 4px;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
        }}
        
        .env-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 6px 14px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .status-banner {{
            background: {status_color};
            padding: 30px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }}
        
        .status-banner-left {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        
        .status-icon {{
            width: 48px;
            height: 48px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 700;
            color: white;
        }}
        
        .status-content h2 {{
            font-size: 22px;
            font-weight: 600;
            color: white;
            margin-bottom: 4px;
        }}
        
        .status-content p {{
            font-size: 13px;
            color: rgba(255, 255, 255, 0.85);
        }}
        
        .status-badge {{
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 8px 18px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            background: #fafbfc;
            border-bottom: 1px solid #e1e4e8;
        }}
        
        .metric {{
            padding: 35px 30px;
            text-align: center;
            border-right: 1px solid #e1e4e8;
            position: relative;
            transition: background 0.2s;
        }}
        
        .metric:last-child {{
            border-right: none;
        }}
        
        .metric:hover {{
            background: #f6f8fa;
        }}
        
        .metric-icon {{
            width: 40px;
            height: 40px;
            margin: 0 auto 12px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 700;
        }}
        
        .metric-icon.pass {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
        }}
        
        .metric-icon.fail {{
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            color: #721c24;
        }}
        
        .metric-icon.skip {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            color: #856404;
        }}
        
        .metric-icon.total {{
            background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
            color: #0c5460;
        }}
        
        .metric-value {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 6px;
            line-height: 1;
        }}
        
        .metric-value.pass {{ color: #28a745; }}
        .metric-value.fail {{ color: #dc3545; }}
        .metric-value.skip {{ color: #ffc107; }}
        .metric-value.total {{ color: #17a2b8; }}
        
        .metric-label {{
            font-size: 11px;
            color: #6a737d;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
        }}
        
        .content {{
            padding: 50px;
        }}
        
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 16px;
            border-bottom: 2px solid #e1e4e8;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #24292e;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .section-subtitle {{
            font-size: 13px;
            color: #6a737d;
        }}
        
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            overflow: hidden;
        }}
        
        thead {{
            background: linear-gradient(180deg, #fafbfc 0%, #f6f8fa 100%);
        }}
        
        th {{
            padding: 16px 20px;
            text-align: left;
            font-size: 11px;
            font-weight: 700;
            color: #24292e;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border-bottom: 2px solid #e1e4e8;
        }}
        
        td {{
            padding: 18px 20px;
            border-bottom: 1px solid #e1e4e8;
            font-size: 14px;
        }}
        
        tbody tr {{
            transition: background 0.15s;
        }}
        
        tbody tr:hover {{
            background: #f6f8fa;
        }}
        
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .suite-name {{
            font-weight: 600;
            color: #24292e;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .suite-name::before {{
            content: '';
            width: 6px;
            height: 6px;
            background: #0366d6;
            border-radius: 50%;
            flex-shrink: 0;
        }}
        
        .suite-duration {{
            font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
            color: #6a737d;
            font-size: 13px;
            font-weight: 500;
        }}

        .ticket-ref {{
            font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            color: #0366d6;
            font-weight: 500;
            white-space: nowrap;
        }}
        
        .status-cell {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        
        .status-cell::before {{
            content: '';
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }}
        
        .status-pass {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-pass::before {{
            background: #28a745;
        }}
        
        .status-fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .status-fail::before {{
            background: #dc3545;
        }}
        
        .status-skip {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .status-skip::before {{
            background: #ffc107;
        }}
        
        .summary-section {{
            margin-top: 40px;
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }}
        
        .summary-card {{
            background: linear-gradient(135deg, #f6f8fa 0%, #fafbfc 100%);
            border: 1px solid #e1e4e8;
            border-radius: 8px;
            padding: 24px;
        }}
        
        .summary-card h3 {{
            font-size: 13px;
            font-weight: 600;
            color: #24292e;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }}
        
        .summary-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e1e4e8;
        }}
        
        .summary-item:last-child {{
            border-bottom: none;
        }}
        
        .summary-label {{
            font-size: 13px;
            color: #6a737d;
            font-weight: 500;
        }}
        
        .summary-value {{
            font-size: 13px;
            color: #24292e;
            font-weight: 600;
            font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
        }}
        
        .performance-card {{
            background: linear-gradient(135deg, #0366d6 0%, #0256c7 100%);
            color: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(3, 102, 214, 0.3);
        }}
        
        .performance-card h3 {{
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 20px;
            opacity: 0.9;
        }}
        
        .performance-metric {{
            margin-bottom: 16px;
        }}
        
        .performance-metric:last-child {{
            margin-bottom: 0;
        }}
        
        .performance-label {{
            font-size: 11px;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}
        
        .performance-value {{
            font-size: 24px;
            font-weight: 700;
            font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
        }}
        
        .footer {{
            background: #f6f8fa;
            padding: 30px 50px;
            border-top: 1px solid #e1e4e8;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .footer-left {{
            font-size: 13px;
            color: #6a737d;
        }}
        
        .footer-left strong {{
            color: #24292e;
            font-weight: 600;
        }}
        
        .footer-right {{
            font-size: 12px;
            color: #959da5;
        }}
        
        @media print {{
            @page {{
                size: A4;
                margin: 10mm;
            }}
            
            body {{
                background: white;
                padding: 0;
                margin: 0;
            }}
            
            .container {{
                box-shadow: none;
                max-width: 100%;
                margin: 0;
            }}
            
            .header {{
                padding: 15px 20px;
                page-break-after: avoid;
            }}
            
            .header h1 {{
                font-size: 18px;
                margin-bottom: 4px;
            }}
            
            .header-meta {{
                margin-top: 6px;
                font-size: 11px;
            }}
            
            .status-banner {{
                padding: 12px 20px;
                page-break-after: avoid;
            }}
            
            .status-icon {{
                width: 32px;
                height: 32px;
                font-size: 18px;
            }}
            
            .status-content h2 {{
                font-size: 16px;
                margin-bottom: 2px;
            }}
            
            .status-content p {{
                font-size: 11px;
            }}
            
            .status-badge {{
                padding: 5px 12px;
                font-size: 11px;
            }}
            
            .metrics {{
                page-break-after: avoid;
                page-break-inside: avoid;
            }}
            
            .metric {{
                padding: 12px 10px;
            }}
            
            .metric-icon {{
                width: 28px;
                height: 28px;
                margin-bottom: 6px;
                font-size: 14px;
            }}
            
            .metric-value {{
                font-size: 24px;
                margin-bottom: 4px;
            }}
            
            .metric-label {{
                font-size: 9px;
            }}
            
            .content {{
                padding: 15px 20px;
                page-break-inside: avoid;
            }}
            
            .section-header {{
                margin-bottom: 12px;
                padding-bottom: 8px;
            }}
            
            .section-title {{
                font-size: 14px;
            }}
            
            .section-subtitle {{
                font-size: 11px;
            }}
            
            table {{
                page-break-inside: avoid;
                font-size: 11px;
            }}
            
            th {{
                padding: 8px 10px;
                font-size: 9px;
            }}
            
            td {{
                padding: 8px 10px;
                font-size: 11px;
            }}
            
            .suite-name {{
                font-size: 12px;
            }}
            
            .suite-duration {{
                font-size: 11px;
            }}
            
            .status-cell {{
                padding: 4px 8px;
                font-size: 10px;
            }}
            
            .status-cell::before {{
                width: 6px;
                height: 6px;
            }}
            
            .summary-section {{
                margin-top: 12px;
                page-break-inside: avoid;
                gap: 10px;
            }}
            
            .summary-card {{
                padding: 12px;
            }}
            
            .summary-card h3 {{
                font-size: 11px;
                margin-bottom: 10px;
            }}
            
            .summary-item {{
                padding: 6px 0;
            }}
            
            .summary-label, .summary-value {{
                font-size: 11px;
            }}
            
            .performance-card {{
                padding: 12px;
            }}
            
            .performance-card h3 {{
                font-size: 11px;
                margin-bottom: 12px;
            }}
            
            .performance-metric {{
                margin-bottom: 10px;
            }}
            
            .performance-label {{
                font-size: 9px;
                margin-bottom: 4px;
            }}
            
            .performance-value {{
                font-size: 18px;
            }}
            
            .footer {{
                padding: 10px 20px;
                page-break-before: avoid;
                font-size: 10px;
            }}
            
            .footer-left {{
                font-size: 11px;
            }}
            
            .footer-right {{
                font-size: 10px;
            }}
        }}
        
        @media (max-width: 768px) {{
            .metrics {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .summary-section {{
                grid-template-columns: 1fr;
            }}
            
            .content {{
                padding: 30px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-content">
                <h1>Test Suite Execution Report</h1>
                <div class="header-meta">
                    <span class="env-badge">{environment} Environment</span>
                    <div class="header-meta-item">{report_date}</div>
                    <div class="header-meta-item">{timestamp}</div>
                </div>
            </div>
        </div>
        
        <!-- Status Banner -->
        <div class="status-banner">
            <div class="status-banner-left">
                <div class="status-icon">{'✓' if failed == 0 and skipped == 0 else '✗' if failed > 0 else '!'}</div>
                <div class="status-content">
                    <h2>{overall_status}</h2>
                    <p>Test execution completed at {timestamp}</p>
                </div>
            </div>
            <div class="status-badge">{success_rate:.0f}% Success Rate</div>
        </div>
        
        <!-- Metrics -->
        <div class="metrics">
            <div class="metric">
                <div class="metric-icon pass">{passed}</div>
                <div class="metric-value pass">{passed}</div>
                <div class="metric-label">Passed</div>
            </div>
            <div class="metric">
                <div class="metric-icon fail">{failed}</div>
                <div class="metric-value fail">{failed}</div>
                <div class="metric-label">Failed</div>
            </div>
            <div class="metric">
                <div class="metric-icon skip">{skipped}</div>
                <div class="metric-value skip">{skipped}</div>
                <div class="metric-label">Skipped</div>
            </div>
            <div class="metric">
                <div class="metric-icon total">{total}</div>
                <div class="metric-value total">{total}</div>
                <div class="metric-label">Total Suites</div>
            </div>
        </div>
        
        <!-- Content -->
        <div class="content">
            <div class="section-header">
                <div>
                    <div class="section-title">Test Suite Results</div>
                    <div class="section-subtitle">Detailed execution status for all test suites</div>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Suite Name</th>
                        {ticket_th}
                        <th>Status</th>
                        <th>Duration</th>
                    </tr>
                </thead>
                <tbody>
                    {suite_rows}
                </tbody>
            </table>
            
            <div style="margin-top: 20px; padding: 14px 18px; background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; font-size: 13px; color: #24292e;">
                <strong>For Reference - ClickUp ID:</strong> 
                <a href="https://app.clickup.com/t/86d1gc2bt" style="color: #0366d6; text-decoration: none; font-weight: 500;">https://app.clickup.com/t/86d1gc2bt</a>
            </div>
            
            <!-- Summary Section -->
            <div class="summary-section">
                <div class="summary-card">
                    <h3>Execution Summary</h3>
                    <div class="summary-item">
                        <span class="summary-label">Total Test Suites</span>
                        <span class="summary-value">{total}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Success Rate</span>
                        <span class="summary-value">{success_rate:.1f}%</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Total Duration</span>
                        <span class="summary-value">{total_duration:.1f}s</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Average Duration</span>
                        <span class="summary-value">{(total_duration/total if total > 0 else 0):.1f}s</span>
                    </div>
                </div>
                
                <div class="performance-card">
                    <h3>Performance Metrics</h3>
                    <div class="performance-metric">
                        <div class="performance-label">Total Time</div>
                        <div class="performance-value">{total_duration/60:.1f}m</div>
                    </div>
                    <div class="performance-metric">
                        <div class="performance-label">Avg per Suite</div>
                        <div class="performance-value">{(total_duration/total if total > 0 else 0):.1f}s</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="footer-left">
                <strong>LocoBuzz Automation Framework</strong> | Quality Assurance & Testing
            </div>
            <div class="footer-right">
                Report generated on {timestamp}
            </div>
        </div>
    </div>
</body>
</html>'''
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
    return html
