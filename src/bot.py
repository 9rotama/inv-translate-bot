import discord
from discord.ext import commands
from os import getenv

from translate import translate_GAS
from generate import langs_order_str, create_embed, create_embed_withfooter
from ChannelConfig import ChannelConfig

command_prefix = "rt!"

intents = discord.Intents.all()
intents.message_content = True
token = getenv("DISCORD_BOT_TOKEN")
bot = commands.Bot(
    command_prefix=command_prefix,
    intents=intents
    )
# デフォルトで入っているhelpコマンドを削除
bot.remove_command('help') 

channels_list: dict[str, ChannelConfig] = {}
# チャンネルごとの設定を保持する辞書
# key...チャンネルID
# value...チャンネルごとの設定(ChannelConfigクラス)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    await bot.change_presence(activity=discord.Game(name=command_prefix+"helpでヘルプ表示"))
    # ステータスを設定

@bot.command()
async def start(ctx):
    if not ctx.channel.id in channels_list:
        channels_list[ctx.channel.id] = ChannelConfig(ctx.channel.id) #channel_listに追加

    if not channels_list[ctx.channel.id].started:
        desc = "翻訳開始！"

        embed = create_embed(
            "start", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        channels_list[ctx.channel.id].started = True
        return
    else:
        desc = "すでに翻訳開始しています"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        channels_list[ctx.channel.id].started = True
        return

@bot.command()
async def stop(ctx):
    if not ctx.channel.id in channels_list:
        desc = "先に翻訳を開始してください"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    if channels_list[ctx.channel.id].started:
        desc = "翻訳を終了します"

        embed = create_embed(
            "stopped", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        channels_list[ctx.channel.id].started = False
        return
    else:
        desc = "先に翻訳を開始してください"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

@bot.command()
async def set(ctx, *args):
    if not ctx.channel.id in channels_list:
        channels_list[ctx.channel.id] = ChannelConfig(ctx.channel.id)

    if len(args) == 0:
        desc = "設定中の言語```" + langs_order_str(channels_list[ctx.channel.id].langs, " 👉 ") + "```"

        embed = create_embed(
            "set", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    if len(args) > 10:
        desc = "中継言語に設定できるのは１０ヶ国語までです"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    else:
        res = translate_GAS("a", args)
        # 引数にGASで使えない言語が含まれているかどうかテストする

        if "無効な引数: target" in res:
            desc = "無効な言語が指定されています"
            embed = create_embed(
                "error", desc, bot.user.name, bot.user.display_avatar.url)
            await ctx.channel.send(embed=embed)
            return

        elif "特定の言語間での翻訳は、現在サポートされていません。" in res:
            desc = "同じ言語間での翻訳\nor\nサポートされていない特定の言語間の翻訳\nが含まれています"
            embed = create_embed(
                "error", desc, bot.user.name, bot.user.display_avatar.url)
            await ctx.channel.send(embed=embed)
            return

        channels_list[ctx.channel.id].langs = args

        desc = "言語を設定しました```" + langs_order_str(channels_list[ctx.channel.id].langs, " 👉 ") + "```"

        embed = create_embed(
            "set", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

@bot.command()
async def help(ctx):
    desc = "使い方:\n```" + command_prefix + "start```翻訳開始\n```" + command_prefix + "set```現在設定されている中継言語を表示\n\n```" + command_prefix + "set [1番目の言語コード] [2番めの言語コード] ...```中継する言語を設定\n※10ヶ国語まで設定できます\n\n言語コードの表→https://cloud.google.com/translate/docs/languages?hl=ja\n\n```" + command_prefix + "stop```翻訳を終了\n"

    embed = create_embed("help", desc, bot.user.name, bot.user.display_avatar.url)
    await ctx.channel.send(embed=embed)

    return

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    # bot自身のメッセージは読まずに終了


    if ctx.content.startswith(command_prefix):
        await bot.process_commands(ctx)
        return
    # コマンドプレフィックスが付く場合commandsの処理にまわして終了
    started: bool = False
    if ctx.channel.id in channels_list:
        started = channels_list[ctx.channel.id].started

    if started:
        not_translated_txt = ctx.content

        await ctx.delete()
        if not ctx.author.nick == None:
            name = ctx.author.nick
        else:
            name = ctx.author.name
        # ニックネームが設定されてなければユーザ名で表示する

        result = translate_GAS(not_translated_txt, channels_list[ctx.channel.id].langs)
        desc = result + "\n\n||原文:" + not_translated_txt + "||"
        icon_url = ctx.author.display_avatar.url
        footer_text = langs_order_str(channels_list[ctx.channel.id].langs, " -> ")

        embed = create_embed_withfooter("", desc, name, icon_url, footer_text, icon_url)
        await ctx.channel.send(embed=embed)

        return

bot.run(token)