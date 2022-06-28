import discord
import translate

command_prefix = "^^"


class BotClient(discord.Client):
    started_channels_list = {}
    # key...チャンネルID
    # value...チャンネルごとの設定

    def langs_order_str(self, langs, separator):
        str = "ja" + separator + separator.join(langs) + separator + "ja"
        return str

    def create_embed(self, title, desc, name, icon_url):
        embed = discord.Embed(title=title, description=desc)
        embed.set_author(name=name, icon_url=icon_url)
        return embed

    def create_embed_withfooter(self, title, desc, name, icon_url, footer_text, footer_icon_url):
        embed = discord.Embed(title=title, description=desc)
        embed.set_author(name=name, icon_url=icon_url)
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        return embed

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

        await self.change_presence(activity=discord.Game(name=command_prefix+"helpでヘルプ表示"))
        # ステータスを設定

    async def on_message(self, message):
        channel_id = message.channel.id
        is_started = channel_id in self.started_channels_list

        bot_name = self.user.name
        bot_icon_url = self.user.avatar_url

        if message.author == self.user:
            return
        # bot自身のメッセージは読まずに終了

        if message.content.startswith(command_prefix+"start"):
            if not is_started:
                desc = "翻訳開始！"
                embed = self.create_embed(
                    "start", desc, bot_name, bot_icon_url)
                await message.channel.send(embed=embed)

                self.started_channels_list[channel_id] = ["en"]
                # 新しいチャンネルの言語を英語のみで初期化
                return

            else:
                return

        if message.content.startswith(command_prefix+"stop"):
            if is_started:
                desc = "翻訳を終了します"
                embed = self.create_embed(
                    "stopped", desc, bot_name, bot_icon_url)
                await message.channel.send(embed=embed)

                del self.started_channels_list[channel_id]
                # 辞書からチャンネルを削除
                return

            else:
                return

        if message.content.startswith(command_prefix+"set"):
            if is_started:
                args = message.content.split(" ")[1:]

                if len(args) == 0:
                    desc = "設定中の言語```" + self.langs_order_str(self.started_channels_list[channel_id], " 👉 ") + "```"

                    embed = self.create_embed(
                        "set", desc, bot_name, bot_icon_url)
                    await message.channel.send(embed=embed)

                    return

                if len(args) > 10:
                    desc = "中継言語に設定できるのは１０ヶ国語までです"

                    embed = self.create_embed(
                        "error", desc, bot_name, bot_icon_url)
                    await message.channel.send(embed=embed)

                    return

                else:
                    res = translate.translate_GAS("a", args)
                    # 引数にGASで使えない言語が含まれているかどうかテストする

                    if "無効な引数: target" in res:
                        desc = "無効な言語が指定されています"
                        embed = self.create_embed(
                            "error", desc, bot_name, bot_icon_url)
                        await message.channel.send(embed=embed)

                        return
 
                    elif "特定の言語間での翻訳は、現在サポートされていません。" in res:
                        desc = "同じ言語間での翻訳\nor\nサポートされていない特定の言語間の翻訳\nが含まれています"
                        embed = self.create_embed(
                            "error", desc, bot_name, bot_icon_url)
                        await message.channel.send(embed=embed)

                        return

                    self.started_channels_list[channel_id] = args

                    desc = "言語を設定しました```" + self.langs_order_str(self.started_channels_list[channel_id], " 👉 ") + "```"

                    embed = self.create_embed(
                        "set", desc, bot_name, bot_icon_url)
                    await message.channel.send(embed=embed)

                    return

            else:
                return

        if message.content.startswith(command_prefix+"help"):
            desc = "使い方:\n```" + command_prefix + "start```翻訳開始\n```" + command_prefix + "set```現在設定されている中継言語を表示\n```" + command_prefix + "set [1番目の言語コード [2番めの言語コード] ...```中継する言語を設定\n※10ヶ国語まで設定できます\n言語コードの表→https://cloud.google.com/translate/docs/languages?hl=ja\n```" + command_prefix + "stop```翻訳を終了"

            embed = self.create_embed("help", desc, bot_name, bot_icon_url)
            await message.channel.send(embed=embed)

            return

        if is_started:
            not_translated_txt = message.content

            await message.delete()
            if not message.author.nick == None:
                name = message.author.nick
            else:
                name = message.author.name
            # ニックネームが設定されてなければユーザ名で表示する

            result = translate.translate_GAS(not_translated_txt, self.started_channels_list[channel_id])
            desc = result + "\n\n||原文:" + not_translated_txt + "||"
            icon_url = message.author.avatar_url
            footer_text = self.langs_order_str(self.started_channels_list[channel_id], " -> ")

            embed = self.create_embed_withfooter("", desc, name, icon_url, footer_text, icon_url)
            await message.channel.send(embed=embed)

            return
