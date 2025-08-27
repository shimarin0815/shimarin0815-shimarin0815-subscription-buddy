from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from models import db, Subscription
from datetime import date, timedelta
import smtplib
from email.mime.text import MIMEText

def send_mail(subject: str, body: str, app):
    if not app.config["SMTP_HOST"] or not app.config["REMINDER_TO"]:
        return  # メール未設定ならスキップ
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = app.config["MAIL_FROM"]
    msg["To"] = app.config["REMINDER_TO"]

    with smtplib.SMTP(app.config["SMTP_HOST"], app.config["SMTP_PORT"]) as s:
        s.starttls()
        if app.config["SMTP_USER"]:
            s.login(app.config["SMTP_USER"], app.config["SMTP_PASS"])
        s.send_message(msg)

def daily_check():
    app = current_app._get_current_object()
    days = app.config["REMINDER_DAYS"]
    subs = Subscription.query.all()
    due_list = [s for s in subs if s.is_due_within(days)]

    free_end_list = [s for s in subs
                     if s.free_trial_until and (s.free_trial_until - date.today()) <= timedelta(days=days)]

    parts = []
    if due_list:
        parts.append("【もうすぐ支払い】\n" + "\n".join(
            f"- {s.name}: {s.price:.0f}{s.currency}（{s.cycle}） / {s.next_billing_date}"
            for s in due_list))
    if free_end_list:
        parts.append("\n【無料期間おわり注意】\n" + "\n".join(
            f"- {s.name}: 無料終了 {s.free_trial_until}"
            for s in free_end_list))
    if parts:
        body = "\n".join(parts)
        send_mail("サブスク管理くん ▶ リマインド", body, app)

def start_scheduler(app):
    scheduler = BackgroundScheduler(daemon=True, timezone="Asia/Tokyo")
    scheduler.add_job(daily_check, "cron", hour=9, minute=0)  # 毎朝9時
    scheduler.start()
