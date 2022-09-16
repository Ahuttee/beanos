import discord
from discord.ext import commands
import json
import random
import asyncio
import os

with open("config.json", 'r') as file:
	config = json.load(file)

with open("dictionary.txt", 'r') as file:
	dictionary = file.read().split("\n")

intents = discord.Intents.default()

bot = commands.Bot(
	command_prefix = config['prefix'],
	intents=intents
)

@bot.event
async def on_ready():
	await bot.tree.sync()

	activity = discord.Streaming(
		name = "with Quandale Dingle",
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
bot.run(config['token'])