# サブスク管理くん 💖

Flask で作ったサブスク管理ツールです。  
毎月の支出を可視化して、支払い日を管理できます。

## 🚀 機能
- サブスクの新規追加・編集・削除
- 支払いサイクル（月払い / 年払い）
- 無料期間の終了日も登録可能
- 月額 / 年額の合計を自動計算



## 🛠 セットアップ方法
1. リポジトリをクローン
   ```bash
   git clone https://github.com/shimarin0815/subscription-buddy.git
   cd subscription-buddy
２.仮想環境を作成して有効化

python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Mac/Linux

３.依存パッケージをインストール
pip install -r requirements.txt

４.アプリを起動
python app.py

５. ブラウザで http://127.0.0.1:5000 を開く
