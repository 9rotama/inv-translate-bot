# This example requires the 'message_content' intent.

import discord



class MyClient(discord.Client):
    isStarted = False;

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('^bye'):
            if self.isStarted:
                await message.channel.send('翻訳を終了します')
                self.isStarted = False;
            else:
                return

        if self.isStarted:
            await message.channel.send(message.content)

        if message.content.startswith('^start'):
            if not self.isStarted:
                await message.channel.send('翻訳開始!')
                self.isStarted = True;
            else:
                return

intents = discord.Intents.default()
client = MyClient(intents=intents)

# token = 'getenv('DISCORD_BOT_TOKEN')'
token = 'OTgyMDg0MDQ2OTI0NDM5NjIy.Gy_m2U.K9hK2zE2iR5tWoBtNGdJFAuTFdKyE1iFl6mWWs'
client.run(token)
