# This example requires the 'message_content' intent.

import discord
import trans
from PIL import Image
import requests
import io

command_prefix = "^"

class MyClient(discord.Client):
    isStarted = False;
    langs = ["en"]

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(command_prefix+'start'):
            if not self.isStarted:
                await message.channel.send('翻訳開始!')
                self.isStarted = True;
                return
            else:
                return

        if message.content.startswith(command_prefix+'bye'):
            if self.isStarted:
                await message.channel.send('翻訳を終了します')
                self.isStarted = False;
                return
            else:
                return

        if message.content.startswith(command_prefix+'set'):
            args = message.content.split(' ')[1:]

            if len(args) == 0:
                await message.channel.send("設定中の言語```ja 👉 " + ' 👉 '.join(self.langs) + " 👉 ja```")
                return
            else:
                for arg in args:
                    if not arg in trans.LANGUAGES:
                        await message.channel.send("無効な言語が指定されています")
                        return
                await message.channel.send("言語を設定しました")
                self.langs = args
                return

        if message.content.startswith(command_prefix+'help'):
            await message.channel.send('使い方:\n```'+command_prefix+'start```翻訳開始\n```'+command_prefix+'set [1番目の言語コード [2番めの言語コード] ...```中継する言語を設定\n言語コードの表→https://cloud.google.com/translate/docs/languages?hl=ja\n```'+command_prefix+'bye```翻訳を終了')
            return

        if self.isStarted:
            name = ""
            tmp = message.content
            await message.delete()
            if not message.author.nick == None:
                name = message.author.nick
            else:
                name = message.author.name

            result = trans.trans_loop(tmp, self.langs)
            await message.channel.send(name + "> " + result)
            return

intents = discord.Intents.default()
client = MyClient(intents=intents)

token = 'getenv('DISCORD_BOT_TOKEN')'

client.run(token)
