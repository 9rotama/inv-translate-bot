import discord
import trans

command_prefix = "^"

class BotClient(discord.Client):
    channels = {}
    # key...チャンネルID
    # value...設定されている言語リスト

    def create_command_msg(self, title, desc, name, icon_url):
        embed = discord.Embed(title=title, description=desc)
        embed.set_author(name=name, icon_url=icon_url)
        return embed

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

        await self.change_presence(activity=discord.Game(name=command_prefix+"helpでヘルプ表示"))
        # ステータスを設定

    async def on_message(self, message):
        channel_id = message.channel.id
        isStarted = channel_id in self.channels

        botName = self.user.name
        botIcon = self.user.avatar_url

        if message.author == self.user:
            return
        # bot自身のメッセージは読まない

        if message.content.startswith(command_prefix+"start"):

            if not isStarted:
                desc = "翻訳開始！"
                embed = self.create_command_msg("start", desc, botName, botIcon)
                await message.channel.send(embed=embed)

                self.channels[channel_id] = ["en"]
                # 新しいチャンネルの言語を初期化
                return

            else:
                return

        if message.content.startswith(command_prefix+"stop"):

            if isStarted:
                desc = "翻訳を終了します"
                embed = self.create_command_msg("stopped", desc, botName, botIcon)
                await message.channel.send(embed=embed)

                del self.channels[channel_id]
                # 辞書からチャンネルを削除
                return

            else:
                return

        if message.content.startswith(command_prefix+"set"):

            if isStarted:
                args = message.content.split(" ")[1:]

                if len(args) == 0:
                    desc = "設定中の言語```ja 👉 " + " 👉 ".join(self.channels[channel_id]) + " 👉 ja```"
                    embed = self.create_command_msg("set", desc, botName, botIcon)
                    await message.channel.send(embed=embed)

                    return

                if len(args) > 10:
                    desc = "中継言語に設定できるのは１０ヶ国語までです"
                    embed = self.create_command_msg("error", desc, botName, botIcon)
                    await message.channel.send(embed=embed)

                    return

                else:
                    res = trans.trans("a", args)
                    # 引数にGASで使えない言語が含まれているかどうかテストする

                    if "無効な引数: target" in res:
                        desc = "無効な言語が指定されています"
                        embed = self.create_command_msg("error", desc, botName, botIcon)
                        await message.channel.send(embed=embed)

                        return

                    self.channels[channel_id] = args

                    desc = "言語を設定しました```ja 👉 " + " 👉 ".join(self.channels[channel_id]) + " 👉 ja```"
                    embed = self.create_command_msg("set", desc, botName, botIcon)
                    await message.channel.send(embed=embed)

                    return

            else:
                return

        if message.content.startswith(command_prefix+"help"):
            desc = "使い方:\n```" + command_prefix + "start```翻訳開始\n```" + command_prefix + "set```現在設定されている中継言語を表示\n```" + command_prefix + "set [1番目の言語コード [2番めの言語コード] ...```中継する言語を設定\n※10ヶ国語まで設定できます\n言語コードの表→https://cloud.google.com/translate/docs/languages?hl=ja\n```" + command_prefix + "stop```翻訳を終了"
            embed = self.create_command_msg("help", desc, botName, botIcon)
            await message.channel.send(embed=embed)

            return

        if isStarted:
            original_txt = message.content

            await message.delete()
            if not message.author.nick == None:
                name = message.author.nick
            else:
                name = message.author.name
            # ニックネームが設定されてなければユーザ名で表示したい

            result = trans.trans(original_txt, self.channels[channel_id])

            desc = result + "\n\n||原文:" + original_txt + "||"
            footer_text = "ja -> " + " -> ".join(self.channels[channel_id]) + " -> ja"
            embed = discord.Embed(description=desc)
            embed.set_author(name=name, icon_url=message.author.avatar_url)
            embed.set_footer(text=footer_text, icon_url=self.user.avatar_url)
            await message.channel.send(embed=embed)

            return