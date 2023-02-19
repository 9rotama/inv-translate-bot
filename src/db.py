from motor import motor_asyncio as motor
from os import environ

db_connection = environ["DB_CONNECTION"]

dbclient = motor.AsyncIOMotorClient(db_connection)
db = dbclient["re-translate-bot"]
channels_collection = db.channels

async def add_channel(channel_id):
    await channels_collection.insert_one({
        "channel_id": channel_id,
        "started": False,           # 翻訳開始状態かどうか
        "langs": ["en"],            # 中継言語
        "show_origin_text": True,   # 原文を表示するかどうか
        "origin_lang": "ja"         # 原文の言語
    })

async def get_channel(channel_id):
    config = await channels_collection.find_one({
        "channel_id": channel_id
    }, {
        "_id": False
    })
    if config is None:
        return False
    return config

async def set_channel(channel_id, started, langs, show_origin_text, origin_lang):
    new_config = {
        "channel_id": channel_id,
        "started": started,
        "langs": langs,
        "show_origin_text": show_origin_text,
        "origin_lang": origin_lang
    }
    await channels_collection.replace_one({
        "channel_id": channel_id  # channel_idで条件を指定
    }, new_config)

