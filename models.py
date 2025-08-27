from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

db = SQLAlchemy()

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)            # サービス名
    price = db.Column(db.Float, nullable=False, default=0.0)   # 1回の支払額
    currency = db.Column(db.String(8), default="JPY")
    cycle = db.Column(db.String(16), default="monthly")        # "monthly" or "yearly"
    next_billing_date = db.Column(db.Date, nullable=False)
    free_trial_only = db.Column(db.Boolean, default=False)     # 無料期間のみの利用フラグ
    free_trial_until = db.Column(db.Date, nullable=True)       # 無料終了日（任意）
    notes = db.Column(db.String(200), default="")

    def monthly_equiv(self):
        # 年払いは12で割って月あたりにする
        return self.price if self.cycle == "monthly" else self.price / 12

    def annual_equiv(self):
        return self.price * 12 if self.cycle == "monthly" else self.price

    def is_due_within(self, days: int) -> bool:
        return (self.next_billing_date - date.today()) <= timedelta(days=days)
