import logging

logging.basicConfig(level=logging.DEBUG)

import os
from fastapi import FastAPI, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler

# ボットトークンと署名シークレットを使ってアプリを初期化します
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)
app_handler = SlackRequestHandler(app)

api = FastAPI()


# 'hello' を含むメッセージをリッスンします
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say, logger):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    logger.info(message)
    say(f"Hello there <@{message['user']}>!")


@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("What's up?")


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)
