import discord
from discord.ext import commands, tasks
import json
import asyncio
import os
import logging
from itertools import cycle


status_msg = cycle( ["with Shaq", "with Kai Cenat", "with Quandale Dingle", "with you"] )

log_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

with open("config.json", 'r') as file:
        config = json.load(file)

bot = commands.Bot(
	command_prefix = config['prefix'],
	intents=intents
)


@tasks.loop(minutes=5)
async def update_status():
    activity = discord.Streaming(
		name = next(status_msg),
		url = "https://www.twitch.tv/quandaledingle1235"
	)
    await bot.change_presence(activity=activity)
    


@bot.event
async def on_ready():
	await bot.tree.sync()
	print("Bot is online")
	await update_status.start()

async def load_cogs():
	for file in os.listdir('./cogs'):
		if file.endswith(".py"):
			extension = file[:-3]
			await bot.load_extension(f"cogs.{extension}")
			print("Loaded extension", extension)

asyncio.run(load_cogs())


# For hosting on Replit
if "REPLIT" in os.environ:
  import keep_alive
  keep_alive.main()
  config["token"] = os.environ["TOKEN"]
  
bot.run(config["token"], log_handler=log_handler, log_level=logging.WARNING)