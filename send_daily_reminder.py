"""
send_daily_reminder.py
Sends the 22:00 daily check-in reminder email.
Schedule with Windows Task Scheduler:
  - Program: python
  - Arguments: send_daily_reminder.py
  - Start in: C:\path\to\personal-life-progress-tracker
  - Trigger: Daily at 22:00
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from config import EMAIL_CONFIG


def send_reminder():
    today     = date.today().strftime('%A, %d %B %Y')
    cfg       = EMAIL_CONFIG

    subject = "Time for your daily check-in, Princess 🌸"

    html_body = f"""
    <html>
    <body style="
        font-family: 'Segoe UI', Arial, sans-serif;
        background: linear-gradient(135deg, #fff0f6, #ead6f5, #d0e8ff);
        min-height: 100vh;
        padding: 40px 20px;
        margin: 0;
    ">
        <div style="
            max-width: 520px;
            margin: 0 auto;
            background: rgba(255,255,255,0.9);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(155,89,182,0.15);
        ">
            <!-- Header -->
            <div style="text-align:center;margin-bottom:28px;">
                <div style="font-size:2.5rem;margin-bottom:8px;">🌸</div>
                <h1 style="
                    font-size: 1.5rem;
                    color: #6c3483;
                    margin: 0;
                    font-style: italic;
                ">Princess Tracker</h1>
                <p style="color:#a07ab5;font-size:0.85rem;margin:6px 0 0;">{today}</p>
            </div>

            <!-- Divider -->
            <hr style="border:none;height:1px;background:linear-gradient(90deg,#f78fb3,#9b59b6,#74b9ff);margin:0 0 28px;">

            <!-- Body -->
            <p style="color:#2d1b35;font-size:1.05rem;line-height:1.7;margin:0 0 16px;">
                Hey <strong style="color:#9b59b6;">Princess</strong>,
            </p>
            <p style="color:#2d1b35;font-size:1rem;line-height:1.8;margin:0 0 16px;">
                It's time to tick what you achieved today and fill in your major task for tomorrow.
            </p>
            <p style="color:#6b4e71;font-size:0.95rem;font-style:italic;line-height:1.7;margin:0 0 28px;">
                Small steps still count. ✨
            </p>
            <p style="color:#6b4e71;font-size:0.95rem;line-height:1.7;margin:0 0 32px;">
                Open your tracker and close the day with peace. 
            </p>

            <!-- CTA Button -->
            <div style="text-align:center;margin-bottom:28px;">
                <a href="http://localhost:5000"
                   style="
                       display:inline-block;
                       padding:14px 36px;
                       background:linear-gradient(135deg,#f78fb3,#9b59b6);
                       color:white;
                       text-decoration:none;
                       border-radius:50px;
                       font-weight:600;
                       font-size:0.95rem;
                       letter-spacing:0.04em;
                       box-shadow:0 6px 20px rgba(232,105,154,0.35);
                   ">
                    Open My Tracker 🌸
                </a>
            </div>

            <!-- Quote -->
            <p style="
                text-align:center;
                font-style:italic;
                color:#9b59b6;
                font-size:0.9rem;
                border-top:1px solid rgba(247,143,179,0.3);
                padding-top:20px;
                margin:0;
            ">
                "I am becoming the woman I prayed to be."
            </p>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = cfg['sender']
    msg['To']      = cfg['recipient']
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(cfg['smtp_host'], cfg['smtp_port']) as server:
            server.starttls()
            server.login(cfg['sender'], cfg['app_password'])
            server.sendmail(cfg['sender'], cfg['recipient'], msg.as_string())
        print(f"  Reminder sent to {cfg['recipient']}")
    except Exception as e:
        print(f"  Failed to send email: {e}")


if __name__ == '__main__':
    send_reminder()
