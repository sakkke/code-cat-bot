import discord
import os
from dotenv import load_dotenv

import aiohttp
import tempfile

ext_to_lang = {
    '.py': 'py',
}

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for attachment in message.attachments:
        supported_exts = [
            '.py'
        ]

        ext: str
        for supported_ext in supported_exts:
            if attachment.filename.endswith(supported_ext):
                ext = supported_ext
                break

        if not ext:
            continue

        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as response:
                if response.status != 200:
                    print('Response status is not 200')
                    continue

                data = await response.read()
                text = data.decode()

                lang = ext_to_lang[ext]

                await message.channel.send(f'```{lang}\n{text}\n```', silent=True)

bot.run(os.getenv('TOKEN'))
