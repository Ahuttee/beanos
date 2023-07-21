import discord
from discord.ext import commands
import json
import asyncio
import os
import logging

log_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# For heroku server
if 'HEROKU' in os.environ:
    config = {
        "prefix": os.environ['PREFIX'],
        "token": os.environ['TOKEN']
    }
else:
    with open("config.json", 'r') as file:
        config = json.load(file)

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix = config['prefix'],
    intents=intents
)

@bot.event
async def on_ready():
    await bot.tree.sync()

    activity = discord.Streaming(
        name = "",
        url = "https://www.twitch.tv/quandaledingle1235"
    )
    await bot.change_presence(activity=activity)
    print("Bot is online")

async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith(".py"):
            extension = file[:-3]
            await bot.load_extension(f"cogs.{extension}")
            print("Loaded extension", extension)

asyncio.run(load_cogs())
bot.run(config['token'], log_handler=log_handler, log_level=logging.WARNING)