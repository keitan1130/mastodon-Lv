import os
import math
from datetime import datetime, timezone
from mastodon import Mastodon, StreamListener

ACCESS_TOKEN = os.environ.get('MASTODON_ACCESS_TOKEN')
API_BASE_URL = os.environ.get('MASTODON_API_BASE_URL')

if not ACCESS_TOKEN or not API_BASE_URL:
    raise ValueError("環境変数 MASTODON_ACCESS_TOKEN または MASTODON_API_BASE_URL が設定されていません。")

# Mastodonインスタンスの初期化
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=API_BASE_URL
)

class MentionsListener(StreamListener):
    def on_notification(self, notification):
        # 通知が「メンション」でない場合は無視
        if notification['type'] != 'mention':
            return

        status = notification['status']
        content = status['content']

        # トゥート本文に「マス廃レベル」が含まれていない場合は無視
        if 'マス廃レベル' not in content:
            return


        account = status['account']
        acct = account['acct']  # ユーザーID (例: username)
        created_at = account['created_at']  # 登録日時 (datetimeオブジェクト/UTC)
        statuses_count = account['statuses_count']  # トゥート数

        now = datetime.now(timezone.utc)

        delta = now - created_at
        days = delta.days

        if days < 1:
            days = 1

        daily_average = statuses_count / days

        # マス廃Lv (2.74ごとの倍率で切り下げ)
        level = math.floor(daily_average / 2.74)

        reply_text = (
            f"@{acct}\n"
            f"マス歴:{days}日\n"
            f"トゥート数:{statuses_count}\n"
            f"日平均:{daily_average:.2f}\n"
            f"マス廃Lv.{level}"
        )

        try:
            mastodon.status_post(
                status=reply_text,
                in_reply_to_id=status['id'],  # メンション元のトゥートへのリプライとして紐付け
                visibility=status['visibility'] # 元トゥートの公開範囲(公開、未収載、フォロワー限定など)に合わせる
            )
            print(f"@{acct} へ返信しました (Lv.{level})")
        except Exception as e:
            print(f"送信エラー: {e}")

if __name__ == '__main__':
    print("Botを起動しました。メンションを待機しています...")
    listener = MentionsListener()
    # ユーザーのホームタイムラインと通知のストリームを受信
    mastodon.stream_user(listener)
