import discord
from discord.ext import commands
from os import getenv

from translate import translate_GAS
from generate import langs_order_str, create_embed, create_embed_withfooter
from ChannelConfig import ChannelConfig

command_prefix = "^^"

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

#
# on ...　コマンドが打たれたチャンネルで自動翻訳を開始する
#

@bot.command()
async def on(ctx):
    if not ctx.channel.id in channels_list:
        channels_list[ctx.channel.id] = ChannelConfig(ctx.channel.id) #channel_listに追加

    if not channels_list[ctx.channel.id].started:
        desc = "翻訳開始！"

        embed = create_embed(
            "on", desc, bot.user.name, bot.user.display_avatar.url)
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

#
# off ...　コマンドが打たれたチャンネルで自動翻訳を終了する
#

@bot.command()
async def off(ctx):
    if not ctx.channel.id in channels_list:
        desc = "先に翻訳を開始してください"

        embed = create_embed(
            "error", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

    if channels_list[ctx.channel.id].started:
        desc = "翻訳を終了します"

        embed = create_embed(
            "off", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        channels_list[ctx.channel.id].started = False
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
    if not ctx.channel.id in channels_list:
        channels_list[ctx.channel.id] = ChannelConfig(ctx.channel.id)

    channel = channels_list[ctx.channel.id]
    show =  "表示" if channel.show_origin_text else "非表示"

    desc = "中継言語: ```" + langs_order_str(channel.langs, channel.origin_lang, " 👉 ") + "```\n"\
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
    if not ctx.channel.id in channels_list:
        channels_list[ctx.channel.id] = ChannelConfig(ctx.channel.id)

    if channels_list[ctx.channel.id].show_origin_text:
        desc = "原文を非表示にします"
        channels_list[ctx.channel.id].show_origin_text = False
    else:
        desc = "原文を表示します"
        channels_list[ctx.channel.id].show_origin_text = True

    embed = create_embed(
        "set", desc, bot.user.name, bot.user.display_avatar.url)
    await ctx.channel.send(embed=embed)
    return

#
# l ...　コマンドが打たれたチャンネルでの中継言語を設定
#

@bot.command()
async def l(ctx, *args):
    if not ctx.channel.id in channels_list:
        channels_list[ctx.channel.id] = ChannelConfig(ctx.channel.id)

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
        res = translate_GAS("a", args, channels_list[ctx.channel.id].origin_lang)
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

        desc = "言語を設定しました```" + langs_order_str(channels_list[ctx.channel.id].langs, channels_list[ctx.channel.id].origin_lang, " 👉 ") + "```"

        embed = create_embed(
            "set", desc, bot.user.name, bot.user.display_avatar.url)
        await ctx.channel.send(embed=embed)
        return

#
# lo ...　コマンドが打たれたチャンネルでの原文言語を設定
#

@bot.command()
async def ol(ctx, *args):
    if not ctx.channel.id in channels_list:
        channels_list[ctx.channel.id] = ChannelConfig(ctx.channel.id)
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
        res = translate_GAS("a", channels_list[ctx.channel.id].langs, args[0])
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

        channels_list[ctx.channel.id].origin_lang = args[0]

        desc = "言語を設定しました```" + langs_order_str(channels_list[ctx.channel.id].langs, channels_list[ctx.channel.id].origin_lang, " 👉 ") + "```"

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

        result = translate_GAS(not_translated_txt, channels_list[ctx.channel.id].langs, channels_list[ctx.channel.id].origin_lang,)
        if channels_list[ctx.channel.id].show_origin_text:
            desc = result + "\n\n||原文:" + not_translated_txt + "||"
        else:
            desc = result

        icon_url = ctx.author.display_avatar.url
        footer_text = langs_order_str(channels_list[ctx.channel.id].langs, channels_list[ctx.channel.id].origin_lang, " -> ")

        embed = create_embed_withfooter("", desc, name, icon_url, footer_text, icon_url)
        await ctx.channel.send(embed=embed)

        return

bot.run(token)