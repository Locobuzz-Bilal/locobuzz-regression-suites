@echo off
REM ---------------------------------------------------------------------------
REM PreProd Regression Report - premium HTML + PDF.
REM Generates the report, saves the PDF to the Desktop, and opens it.
REM Ticket IDs are read live from config\config.py at run time.
REM ---------------------------------------------------------------------------
setlocal

REM Move to the project root (this file lives in \Suites).
cd /d "%~dp0.."

set PYTHONIOENCODING=utf-8

echo.
echo  Generating PreProd Regression Report...
echo.

if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" "Suites\generate_preprod_regression_passed_report.py" %*
) else (
    python "Suites\generate_preprod_regression_passed_report.py" %*
)

echo.
pause
endlocal
