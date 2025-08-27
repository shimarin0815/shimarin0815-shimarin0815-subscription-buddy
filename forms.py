from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, BooleanField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class SubscriptionForm(FlaskForm):
    name = StringField("サービス名", validators=[DataRequired(), Length(max=100)])
    price = DecimalField("金額", places=2, validators=[DataRequired(), NumberRange(min=0)])
    currency = StringField("通貨", default="JPY")  # 任意。未入力なら JPY を使う
    cycle = SelectField(
        "支払サイクル",
        choices=[("monthly", "月払い"), ("annual", "年払い")],
        validators=[DataRequired()],
    )
    next_billing_date = DateField("次回支払日", format="%Y-%m-%d", validators=[DataRequired()])
    free_trial_only = BooleanField("無料期間のみ（解約予定）")
    # ← ここがポイント：任意入力なので Optional()
    free_trial_until = DateField("無料終了日（任意）", format="%Y-%m-%d", validators=[Optional()])
    notes = TextAreaField("メモ", validators=[Optional(), Length(max=500)])

    submit = SubmitField("保存")
