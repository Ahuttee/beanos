import disnake
from disnake.ext import commands
import json

with open("config.json", 'r') as file:
	config = json.load(file)

bot = commands(
	command_prefix = config['prefix']
)

@bot.slash_command(name='hello')
async def hello(ctx):
	await ctx.send("world!")


bot.run(config['token'])