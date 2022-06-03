from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix='^')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


token = 'OTgyMDg0MDQ2OTI0NDM5NjIy.Gy_m2U.K9hK2zE2iR5tWoBtNGdJFAuTFdKyE1iFl6mWWs'
bot.run(token)
