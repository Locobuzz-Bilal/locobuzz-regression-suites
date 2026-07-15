import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
import time

# ====== CONFIG ======
PROJECT_ROOT = Path(__file__).resolve().parents[1]

SENDER_EMAIL = os.getenv("SMTP_EMAIL")
SENDER_PASS = os.getenv("SMTP_PASS")

# Receivers list
RECIPIENTS = [
    "bilalshaikh9916@gmail.com"
    # "qa-lead@company.com",
    # "your.email@company.com"
]

# Subject
today_str = time.strftime("%d-%b-%Y")
SUBJECT = f"Automation Test Execution Report | {today_str}"

# Attachment auto-detect (latest Allure report folder screenshot)
ATTACHMENTS = []

# Allure report folder (auto detect newest)
def find_latest_allure_report():
    base = PROJECT_ROOT / "Suites" / "allure-report"
    if not base.exists():
        print("⚠️ No allure-report folder found!")
        return None

    # pick latest date folder
    dates = sorted([d for d in base.iterdir() if d.is_dir()], reverse=True)
    latest_date = dates[0]

    # pick latest run folder
    reports = sorted([d for d in latest_date.iterdir() if d.is_dir()], reverse=True)
    return reports[0]

# HTML Email Body
HTML_BODY = f"""
<html>
  <body style="font-family: Arial; margin:0; padding:10;">
    <h2 style="color:#333;">✅ Automation Execution Completed</h2>
    <p><b>Date:</b> {today_str}</p>
    <p>Please find the attached execution report (PDF/HTML/Results).</p>
    
    <br>
    <p style="font-size:14px; color:#777;">
      Regards,<br>
      Bilal | Automation Engineer
    </p>
  </body>
</html>
"""

def send_email():
    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENTS)
    msg.set_content("HTML not supported. Please view in HTML mode.")
    msg.add_alternative(HTML_BODY, subtype="html")

    print("\n📌 Locating latest Allure report...")

    latest = find_latest_allure_report()
    if latest:
        print(f"📎 Attaching: {latest}")
        for file in latest.glob("*"):
            if file.suffix in [".html", ".pdf"]:
                with open(file, "rb") as f:
                    msg.add_attachment(
                        f.read(),
                        maintype="application",
                        subtype="octet-stream",
                        filename=file.name
                    )
                print(f"✅ Attached: {file.name}")

    # SMTP Setup
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.send_message(msg)

    print("\n📤 Email successfully sent!")

if __name__ == "__main__":
    send_email()
