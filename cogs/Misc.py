import discord
from discord.ext import commands
from discord import app_commands
import random
import aiohttp

with open("dictionary.txt", 'r') as f:
	dictionary = f.read().split('\n')

class CatView(discord.ui.View):
	def __init__(self, embed):
		super().__init__()
		self.embed = embed
	
	@discord.ui.button(label="NEW", style=discord.ButtonStyle.green)
	async def new(self, inter: discord.Interaction, button: discord.ui.Button):
		async with aiohttp.ClientSession() as session:
			async with session.get("https://api.thecatapi.com/v1/images/search") as response:
				if response.status == 200:
					data = await response.json()
					self.url = data[0]["url"]
					self.embed.set_image(url=self.url)
					await inter.response.edit_message(embed=self.embed, view=self)
				else:
					inter.response.send_message("Unable to get a new picture", ephemeral=True)

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


	@commands.hybrid_command(name="cat", aliases=['neko'])
	async def cat(self, ctx):
		async with aiohttp.ClientSession() as session:
			async with session.get("https://api.thecatapi.com/v1/images/search") as response:
				if response.status == 200:
					data = await response.json()
					url = data[0]["url"]
				else:
					ctx.send("Unable to get an image, try again later", ephemeral=True)
					return

		
		embed = discord.Embed(
			title = "c a t",
			color = discord.Colour.random()
		)
		embed.set_footer(text = "thecatapi.com")
		embed.set_image(url=url)
		
		view = CatView(embed)
		msg = await ctx.send(embed=embed, view=view)

		await view.wait()
		await msg.edit(embed=embed, view=None)
			


		

async def setup(bot):
	await bot.add_cog(Misc(bot))

	
