# This example requires the 'message_content' intent.

import discord
from os import getenv
import trans

command_prefix = "^"


class BotClient(discord.Client):
    channels = {}

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        channel_id = message.channel.id
        isStarted = channel_id in self.channels

        if message.author == self.user:
            return

        if message.content.startswith(command_prefix+'start'):
            if not isStarted:
                await message.channel.send('翻訳開始!')
                self.channels[channel_id] = ["en"]
                return
            else:
                return

        if message.content.startswith(command_prefix+'stop'):
            if isStarted:
                await message.channel.send('翻訳を終了します')
                del self.channels[channel_id]
                return
            else:
                return

        if message.content.startswith(command_prefix+'set'):
            if isStarted:
                args = message.content.split(' ')[1:]

                if len(args) == 0:
                    await message.channel.send("設定中の言語```ja 👉 " + ' 👉 '.join(self.channels[channel_id]) + " 👉 ja```")
                    return
                else:
                    for arg in args:
                        if not arg in trans.LANGUAGES:
                            await message.channel.send("無効な言語が指定されています")
                            return
                    await message.channel.send("言語を設定しました")
                    self.channels[channel_id] = args
                    return
            else:
                return

        if message.content.startswith(command_prefix+'help'):
            await message.channel.send('使い方:\n```'+command_prefix+'start```翻訳開始\n```'+command_prefix+'set```現在設定されている中継言語を表示\n```'+command_prefix+'set [1番目の言語コード [2番めの言語コード] ...```中継する言語を設定\n言語コードの表→https://cloud.google.com/translate/docs/languages?hl=ja\n```'+command_prefix+'stop```翻訳を終了')
            return

        if isStarted:
            name = ""
            tmp = message.content
            await message.delete()
            if not message.author.nick == None:
                name = message.author.nick
            else:
                name = message.author.name

            result = trans.trans_loop(tmp, self.channels[channel_id])
            await message.channel.send(name + "> " + result)
            return


intents = discord.Intents.default()
client = BotClient(intents=intents)

token = getenv('DISCORD_BOT_TOKEN')
client.run(token)
