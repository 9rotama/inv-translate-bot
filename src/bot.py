import discord
from discord.ext import commands
from os import environ
import sys

from translate import translate_GAS
from generate import langs_order_str, create_embed, create_embed_withfooter
from db import *

command_prefix = "^^"

intents = discord.Intents.all()

token = environ["DISCORD_BOT_TOKEN"]

bot = commands.Bot(
    command_prefix=command_prefix,
    intents=intents
    )
# デフォルトで入っているhelpコマンドを削除
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    await bot.change_presence(activity=discord.Game(name=command_prefix+"helpでヘルプ表示"))
    # ステータスを設定

def validate_exist_langs(langs, origin_langs):
    # 引数にGASで使えない言語が含まれているかどうかテストする
    # エラーがなければFalseを返す
    res = translate_GAS("a", langs, origin_langs)

    if "無効な引数" in res:
        desc = "無効な言語が指定されています"
        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        return embed

    elif "特定の言語間での翻訳は、現在サポートされていません。" in res:
        desc = "同じ言語間での翻訳\nor\nサポートされていない特定の言語間の翻訳\nが含まれています"
        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        return embed
    else:
        return False

#
# on ...　コマンドが打たれたチャンネルで自動翻訳を開始する
#

@bot.command()
async def on(ctx):
    config = await get_channel(ctx.channel.id)

    # チャンネルがDBに無い場合追加する
    if config is False:
        await add_channel(ctx.channel.id)
        config = await get_channel(ctx.channel.id)

    if config["started"] is False:
        # チャンネルがDBにあり場合開始していない場合
        desc = "翻訳開始！"

        embed = create_embed(
            "on", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        await set_channel(ctx.channel.id, True, config["langs"], config["show_origin_text"], config["origin_lang"])
        return
    else:
        desc = "すでに翻訳開始しています"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

#
# off ...　コマンドが打たれたチャンネルで自動翻訳を終了する
#

@bot.command()
async def off(ctx):
    config = await get_channel(ctx.channel.id)

    # チャンネルがDBに無い場合エラーを出す
    if config is False:
        desc = "先に翻訳を開始してください"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    if config["started"]:
        # チャンネルがDBにあり開始している場合
        desc = "翻訳を終了します"

        embed = create_embed(
            "off", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        await set_channel(ctx.channel.id, False, config["langs"], config["show_origin_text"], config["origin_lang"])
        return
    else:
        desc = "先に翻訳を開始してください"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

#
# show ...　コマンドが打たれたチャンネルの設定を表示
#

@bot.command()
async def config(ctx, *args):
    config = await get_channel(ctx.channel.id)

    # チャンネルがDBに無い場合追加する
    if config is False:
        await add_channel(ctx.channel.id)
        config = await get_channel(ctx.channel.id)

    show = "表示" if config["show_origin_text"] else "非表示"
    desc = "中継言語: ```" + langs_order_str(config["langs"], config["origin_lang"], " 👉 ") + "```\n"\
        "原文: ```" + show + "```\n"

    embed = create_embed(
        "設定", desc, bot.user.name, bot.user.display_avatar.url)
    await ctx.channel.send(embed=embed)
    return

#
# spoil ...　コマンドが打たれたチャンネルの原文表示の切り替え
#

@bot.command()
async def spoil(ctx):
    config = await get_channel(ctx.channel.id)

    # チャンネルがDBに無い場合追加する
    if config is False:
        await add_channel(ctx.channel.id)
        config = await get_channel(ctx.channel.id)

    if config["show_origin_text"]:
        desc = "原文を非表示にします"
        await set_channel(ctx.channel.id, config["started"], config["langs"], False, config["origin_lang"])
    else:
        desc = "原文を表示します"
        await set_channel(ctx.channel.id, config["started"], config["langs"], True, config["origin_lang"])

    embed = create_embed(
        "set", desc, bot.user.name, bot.user.display_avatar.url)
    await ctx.channel.send(embed=embed)
    return

#
# l ...　コマンドが打たれたチャンネルでの中継言語を設定
#

@bot.command()
async def l(ctx, *args):
    config = await get_channel(ctx.channel.id)

    # チャンネルがDBに無い場合追加する
    if config is False:
        await add_channel(ctx.channel.id)
        config = await get_channel(ctx.channel.id)

    if len(args) == 0:
        desc = "言語コードを入力してください"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    elif len(args) > 10:
        desc = "中継言語に設定できるのは１０ヶ国語までです"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    else:
        res = validate_exist_langs(args, config["origin_lang"])
        if res:
            await ctx.channel.send(embed=res)
            return

        await set_channel(ctx.channel.id, config["started"], args, config["show_origin_text"], config["origin_lang"])

        config = await get_channel(ctx.channel.id) # 設定が更新されたされたので再度取得
        desc = "言語を設定しました```" + langs_order_str(config["langs"], config["origin_lang"], " 👉 ") + "```"

        embed = create_embed(
            "set", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

#
# lo ...　コマンドが打たれたチャンネルでの原文言語を設定
#

@bot.command()
async def ol(ctx, *args):
    config = await get_channel(ctx.channel.id)

    # チャンネルがDBに無い場合追加する
    if config is False:
        await add_channel(ctx.channel.id)
        config = await get_channel(ctx.channel.id)

    if len(args) == 0:
        desc = "言語コードを入力してください"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    elif len(args) > 1:
        desc = "1ヶ国語のみ入力してください"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    else:
        res = validate_exist_langs(config["langs"], args[0])
        if res:
            await ctx.channel.send(embed=res)
            return

        await set_channel(ctx.channel.id, config["started"], config["langs"], config["show_origin_text"], args[0])

        config = await get_channel(ctx.channel.id) # 設定が更新されたされたので再度取得
        desc = "言語を設定しました```" + langs_order_str(config["langs"], config["origin_lang"], " 👉 ") + "```"

        embed = create_embed(
            "set", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

#
# help ...　ヘルプ表示
#

@bot.command()
async def help(ctx):
    desc = "```" + command_prefix + "on```翻訳開始\n" \
        + "```"+ command_prefix + "off```翻訳を終了\n" \
        + "```" + command_prefix + "config```現在の設定を表示\n" \
        + "```"+ command_prefix + "l [1番目の言語コード] [2番めの言語コード] ...```中継する言語を設定\n※10ヶ国語まで設定できます" \
        + "```"+ command_prefix + "ol [言語コード]```原文で使用する言語を設定\n言語コードの表 → https://cloud.google.com/translate/docs/languages?hl=ja\n" \
        + "```" + command_prefix + "spoil```原文の表示/非表示切り替え\n"

    embed = create_embed("使い方", desc, bot.user.name, bot.user.display_avatar.url)
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

    started = False
    config = await get_channel(ctx.channel.id)

    if config is not False:
        started = config["started"]

    if started:
        not_translated_txt = ctx.content

        await ctx.delete()
        if not ctx.author.nick == None:
            name = ctx.author.nick
        else:
            name = ctx.author.name
        # ニックネームが設定されてなければユーザ名で表示する

        result = translate_GAS(not_translated_txt, config["langs"], config["origin_lang"])
        if config["show_origin_text"]:
            desc = result + "\n\n||原文:" + not_translated_txt + "||"
        else:
            desc = result

        icon_url = ctx.author.display_avatar.url
        footer_text = langs_order_str(config["langs"], config["origin_lang"], " -> ")

        embed = create_embed_withfooter("", desc, name, icon_url, footer_text, icon_url)
        await ctx.channel.send(embed=embed)

        return

bot.run(token)