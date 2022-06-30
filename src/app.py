import discord
from discord.ext import commands
from os import getenv

import translate
import ChannelConfig

command_prefix = "^^"

intents = discord.Intents.all()
intents.message_content = True
token = getenv("DISCORD_BOT_TOKEN")
bot = commands.Bot(
    command_prefix=command_prefix,
    intents=intents
    )
bot.remove_command('help')

channels_list: dict[str, ChannelConfig.ChannelConfig] = {}
# key...チャンネルID
# value...チャンネルごとの設定(ChannelConfigクラス)

def langs_order_str(langs, separator):
        str = "ja" + separator + separator.join(langs) + separator + "ja"
        return str

def create_embed(title, desc, name, icon_url):
    embed = discord.Embed(title=title, description=desc)
    embed.set_author(name=name, icon_url=icon_url)
    return embed

def create_embed_withfooter(title, desc, name, icon_url, footer_text, footer_icon_url):
    embed = discord.Embed(title=title, description=desc)
    embed.set_author(name=name, icon_url=icon_url)
    embed.set_footer(text=footer_text, icon_url=footer_icon_url)
    return embed

@bot.event
async def on_command_error(ctx, e):
  cmd=ctx.invoked_with
  if isinstance(e,discord.ext.commands.CommandNotFound):
    await ctx.send("コマンドが見つかりませんでした")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    await bot.change_presence(activity=discord.Game(name=command_prefix+"helpでヘルプ表示"))
    # ステータスを設定

@bot.event
async def on_message(ctx):
    if not ctx.channel.id in channels_list:
        channels_list[ctx.channel.id] = ChannelConfig.ChannelConfig

    started = channels_list[ctx.channel.id].started
    if ctx.author == bot.user:
        return
    # bot自身のメッセージは読まずに終了

    if started:
        not_translated_txt = ctx.content

        await ctx.delete()
        if not ctx.author.nick == None:
            name = ctx.author.nick
        else:
            name = ctx.author.name
        # ニックネームが設定されてなければユーザ名で表示する

        result = translate.translate_GAS(not_translated_txt, channels_list[ctx.channel.id].langs)
        desc = result + "\n\n||原文:" + not_translated_txt + "||"
        icon_url = ctx.author.avatar_url
        footer_text = bot.langs_order_str(channels_list[ctx.channel.id].langs, " -> ")

        embed = bot.create_embed_withfooter("", desc, name, icon_url, footer_text, icon_url)
        await ctx.channel.send(embed=embed)

        return

@bot.command()
async def start(self, ctx):
    print("aiueo")
    if not channels_list[ctx.channel.id].started:
        desc = "翻訳開始！"

        embed = self.create_embed(
            "start", desc, self.user.name, self.user.avatar_url)
        await ctx.channel.send(embed=embed)
        channels_list[ctx.channel.id].started = True
        return
    else:
        return

@bot.command()
async def stop(self, ctx):
    if channels_list[ctx.channel.id].started:
        desc = "翻訳を終了します"

        embed = self.create_embed(
            "stopped", desc, self.user.name, self.user.avatar_url)
        await ctx.channel.send(embed=embed)
        channels_list[ctx.channel.id].started = False
        return
    else:
        return

@bot.command()
async def set(self, ctx, arg):

    if len(arg) == 0:
        desc = "設定中の言語```" + self.langs_order_str(channels_list[ctx.channel.id].langs, " 👉 ") + "```"

        embed = self.create_embed(
            "set", desc, self.user.name, self.user.avatar_url)
        await ctx.channel.send(embed=embed)
        return

    if len(arg) > 10:
        desc = "中継言語に設定できるのは１０ヶ国語までです"

        embed = self.create_embed(
            "error", desc, self.user.name, self.user.avatar_url)
        await ctx.channel.send(embed=embed)
        return

    else:
        res = translate.translate_GAS("a", arg)
        # 引数にGASで使えない言語が含まれているかどうかテストする

        if "無効な引数: target" in res:
            desc = "無効な言語が指定されています"
            embed = self.create_embed(
                "error", desc, self.user.name, self.user.avatar_url)
            await ctx.channel.send(embed=embed)
            return

        elif "特定の言語間での翻訳は、現在サポートされていません。" in res:
            desc = "同じ言語間での翻訳\nor\nサポートされていない特定の言語間の翻訳\nが含まれています"
            embed = self.create_embed(
                "error", desc, self.user.name, self.user.avatar_url)
            await ctx.channel.send(embed=embed)
            return

        channels_list[ctx.channel.id].langs = arg

        desc = "言語を設定しました```" + self.langs_order_str(channels_list[ctx.channel.id].langs, " 👉 ") + "```"

        embed = self.create_embed(
            "set", desc, self.user.name, self.user.avatar_url)
        await ctx.channel.send(embed=embed)
        return

@bot.command()
async def help(self, ctx):
    desc = "使い方:\n```" + command_prefix + "start```翻訳開始\n```" + command_prefix + "set```現在設定されている中継言語を表示\n```" + command_prefix + "set [1番目の言語コード [2番めの言語コード] ...```中継する言語を設定\n※10ヶ国語まで設定できます\n言語コードの表→https://cloud.google.com/translate/docs/languages?hl=ja\n```" + command_prefix + "stop```翻訳を終了"

    embed = self.create_embed("help", desc, self.user.name, self.user.avatar_url)
    await ctx.channel.send(embed=embed)

    return



bot.run(token)