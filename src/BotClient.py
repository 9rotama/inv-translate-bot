import discord
import translate
import ChannelConfig


class BotClient(discord.Client):
    # key...チャンネルID
    # value...チャンネルごとの設定

    async def on_message(self, message):
        channel_id = message.channel.id

        if not channel_id in self.channels_list:
            self.channels_list[channel_id] = ChannelConfig.ChannelConfig

        started = self.channels_list[channel_id].started

        bot_name = self.user.name
        bot_icon_url = self.user.avatar_url

        if message.author == self.user:
            return
        # bot自身のメッセージは読まずに終了

        if started:
            not_translated_txt = message.content

            await message.delete()
            if not message.author.nick == None:
                name = message.author.nick
            else:
                name = message.author.name
            # ニックネームが設定されてなければユーザ名で表示する

            result = translate.translate_GAS(not_translated_txt, self.channels_list[channel_id].langs)
            desc = result + "\n\n||原文:" + not_translated_txt + "||"
            icon_url = message.author.avatar_url
            footer_text = self.langs_order_str(self.channels_list[channel_id].langs, " -> ")

            embed = self.create_embed_withfooter("", desc, name, icon_url, footer_text, icon_url)
            await message.channel.send(embed=embed)

            return
