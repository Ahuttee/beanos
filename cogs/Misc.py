import discord
from discord.ext import commands
from discord import app_commands
import random

with open("dictionary.txt", 'r') as f:
	dictionary = f.read()

class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.view_avatar_ctx_menu = app_commands.ContextMenu(
			name = "View avatar",
			callback=self.view_avatar
		)

		self.bot.tree.add_command(self.view_avatar_ctx_menu)


	async def view_avatar(self, inter: discord.Interaction, user: discord.User):
		embed = discord.Embed(
			title = "Avatar",
			color = discord.Colour.from_rgb(40, 1, 92)
		)
		embed.set_image(url=user.avatar.url)
		embed.set_footer(text = user.name + "#" + user.discriminator, icon_url = user.avatar.url)

		await inter.response.send_message(embed=embed)

	@commands.hybrid_command(name="godspeak")
	async def godspeak(self, ctx, number: int):
		if number < 150:
			await ctx.send(' '.join([random.choice(dictionary) for _ in range(number)]))
		else:
			await ctx.send("Too large, use a value of less than 150", ephemeral=True)

async def setup(bot):
	await bot.add_cog(Misc(bot))

	
