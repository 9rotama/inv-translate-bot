# This example requires the "message_content" intent.

import discord
from os import getenv
from BotClient import BotClient

intents = discord.Intents.default()
client = BotClient(intents=intents)

token = getenv("DISCORD_BOT_TOKEN")
client.run(token)
