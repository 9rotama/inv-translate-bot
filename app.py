# This example requires the 'message_content' intent.

import discord
from os import getenv
import trans

command_prefix = "^^"

class BotClient(discord.Client):
    channels = {}

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        await self.change_presence(activity=discord.Game(name="^helpでヘルプ表示"))

    async def on_message(self, message):
        channel_id = message.channel.id
        isStarted = channel_id in self.channels

        if message.author == self.user:
            return

        if message.content.startswith(command_prefix+'start'):
            if not isStarted:
                embed = discord.Embed(title='start', description='翻訳開始！')
                embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
                await message.channel.send(embed=embed)
                self.channels[channel_id] = ["en"]
                return
            else:
                return

        if message.content.startswith(command_prefix+'stop'):
            if isStarted:
                embed = discord.Embed(title='stop', description='翻訳を終了します')
                embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
                await message.channel.send(embed=embed)
                del self.channels[channel_id]
                return
            else:
                return

        if message.content.startswith(command_prefix+'set'):
            if isStarted:
                args = message.content.split(' ')[1:]

                if len(args) == 0:
                    embed = discord.Embed(title='set', description="設定中の言語```ja 👉 " + ' 👉 '.join(self.channels[channel_id]) + " 👉 ja```")
                    embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
                    await message.channel.send(embed=embed)
                    return
                else:
                    for arg in args:
                        if not arg in trans.LANGUAGES:
                            embed = discord.Embed(title='set', description='無効な言語が指定されています```' + arg + '```')
                            embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
                            await message.channel.send(embed=embed)
                            self.channels[channel_id] = ["en"]
                            return
                    self.channels[channel_id] = args
                    embed = discord.Embed(title='set', description="言語を設定しました```ja 👉 " + ' 👉 '.join(self.channels[channel_id]) + " 👉 ja```")
                    embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
                    await message.channel.send(embed=embed)
                    return
            else:
                return

        if message.content.startswith(command_prefix+'help'):
            desc = '使い方:\n```'+command_prefix+'start```翻訳開始\n```'+command_prefix+'set```現在設定されている中継言語を表示\n```'+command_prefix+'set [1番目の言語コード [2番めの言語コード] ...```中継する言語を設定\n言語コードの表→https://cloud.google.com/translate/docs/languages?hl=ja\n```'+command_prefix+'stop```翻訳を終了'

            embed = discord.Embed(title='help', description=desc)
            embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
            await message.channel.send(embed=embed)
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
            embed = discord.Embed(description=result)
            embed.set_author(name=name, icon_url=message.author.avatar_url)
            embed.set_footer(text="translated by " + self.user.name, icon_url=self.user.avatar_url)
            await message.channel.send(embed=embed)
            return


intents = discord.Intents.default()
client = BotClient(intents=intents)

token = getenv('DISCORD_BOT_TOKEN')
client.run(token)
