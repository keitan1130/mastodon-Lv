# 軽量なPython公式イメージを利用
FROM python:3.11-slim

# コンテナ内の作業ディレクトリを指定
WORKDIR /app

# 依存関係のファイルをコピー
COPY requirements.txt .

# 依存関係のインストール（キャッシュを残さないことでイメージサイズを削減）
RUN pip install --no-cache-dir -r requirements.txt

# ボットのスクリプトをコピー
COPY bot.py .

# スクリプトを実行
CMD ["python", "bot.py"]
