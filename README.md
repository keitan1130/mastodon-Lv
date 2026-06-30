# マス廃レベル
登録日とトゥート数からマス廃レベルを計算して返信するBotです。

## セットアップ
```bash
cp .env.example .env
```

`.env` ファイルに Mastodon のインスタンスURL、アクセストークンを設定してください。
```bash
docker compose up -d
```

## ログ
```bash
docker compose logs -f
```
