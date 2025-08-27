import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///subs.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # メール設定（SMTP）
    MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASS = os.getenv("SMTP_PASS", "")
    REMINDER_DAYS = int(os.getenv("REMINDER_DAYS", "3"))  # 何日前に通知するか
    REMINDER_TO = os.getenv("REMINDER_TO", "")  # 受信メール
