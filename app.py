from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Subscription
from forms import SubscriptionForm
from config import Config
from datetime import date, timedelta
from scheduler import start_scheduler

# ---- Flaskアプリの作成（これが先！）----
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# DB作成 & どこにできたか表示
with app.app_context():
    db.create_all()
    try:
        print("DB path ->", db.engine.url.database)
    except Exception as e:
        print("DB path print error:", e)

# スケジューラ起動（失敗しても落ちないようガード）
try:
    start_scheduler(app)
except Exception as e:
    print("Scheduler error:", e)

# ---- ここから下にルートを定義 ----
@app.route("/")
def index():
    subs = Subscription.query.order_by(Subscription.next_billing_date.asc()).all()
    monthly_total = round(sum(s.monthly_equiv() for s in subs), 2)
    annual_total = round(sum(s.annual_equiv() for s in subs), 2)

    urgent_days = app.config["REMINDER_DAYS"]
    upcoming = [s for s in subs if s.is_due_within(urgent_days)]
    soon_free_end = [
        s for s in subs
        if s.free_trial_until and (s.free_trial_until - date.today()) <= timedelta(days=urgent_days)
    ]

    return render_template(
        "index.html",
        subs=subs,
        monthly_total=monthly_total,
        annual_total=annual_total,
        upcoming=upcoming,          # ← カンマ必須！
        soon_free_end=soon_free_end,
        urgent_days=urgent_days,
    )

@app.route("/new", methods=["GET", "POST"])
def new():
    form = SubscriptionForm()
    if form.validate_on_submit():
        s = Subscription(
            name=form.name.data,
            price=form.price.data,
            currency=form.currency.data or "JPY",
            cycle=form.cycle.data,
            next_billing_date=form.next_billing_date.data,
            free_trial_only=form.free_trial_only.data,
            free_trial_until=form.free_trial_until.data,
            notes=form.notes.data or "",
        )
        db.session.add(s)
        db.session.commit()
        flash("登録しました！", "success")
        return redirect(url_for("index"))

    if request.method == "POST":
        print("DEBUG form.errors:", form.errors)
        flash("入力内容を確認してください（未入力や日付形式など）", "error")

    return render_template("new.html", form=form)

@app.route("/edit/<int:sid>", methods=["GET", "POST"])
def edit(sid):
    s = Subscription.query.get_or_404(sid)
    form = SubscriptionForm(obj=s)
    if form.validate_on_submit():
        form.populate_obj(s)
        db.session.commit()
        flash("更新しました！", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", form=form, sub=s)

@app.route("/delete/<int:sid>", methods=["POST"])
def delete(sid):
    s = Subscription.query.get_or_404(sid)
    db.session.delete(s)
    db.session.commit()
    flash("削除しました", "success")
    return redirect(url_for("index"))

# 開発用: 1件だけ投入（確認したら消してOK）


if __name__ == "__main__":
    app.run(debug=True)
