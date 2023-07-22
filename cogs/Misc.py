import discord
from discord.ext import commands
from discord import app_commands
import random
import aiohttp

with open("dictionary.txt", 'r') as f:
    dictionary = f.read().split('\n')


class ImageView(discord.ui.View):
    def __init__(self, embed, site_url):
        super().__init__()
        self.embed = embed
        self.site_url = site_url
        self.timeout = 120.0
    
    @discord.ui.button(label="NEW", style=discord.ButtonStyle.green)
    async def new(self, inter: discord.Interaction, button: discord.ui.Button):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.site_url) as response:
                if response.status == 200:
                    data = await response.json()
                    await self.new_image(inter, data)
                else:
                    await inter.response.send_message("Unable to get a new picture", ephemeral=True)
                    
    async def new_image(self, inter, data):
        pass
        
    async def on_timeout(self):
        self.clear_items()
        await self.message.edit(view=self)
            
            

class CatView(ImageView):
    def __init__(self, embed, site_url):
        super().__init__(embed, site_url)
        
    async def new_image(self, inter, data):
        url = data[0]["url"]
        self.embed.set_image(url=url)
        await inter.response.edit_message(embed=self.embed, view=self)
        

class DogView(ImageView):
    def __init__(self, embed, site_url):
        super().__init__(embed, site_url)
        
    async def new_image(self, inter, data):
        url = data["message"]
        self.embed.set_image(url=url)
        await inter.response.edit_message(embed=self.embed, view=self)
    
                    
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
        site_url = "https://api.thecatapi.com/v1/images/search"
        async with aiohttp.ClientSession() as session:
            async with session.get(site_url) as response:
                if response.status == 200:
                    data = await response.json()
                    url = data[0]["url"]
                else:
                    await ctx.send("Unable to get an image, try again later", ephemeral=True)
                    return

        embed = discord.Embed(
            title = "c a t",
            color = discord.Colour.random()
        )
        embed.set_footer(text = "www.thecatapi.com")
        embed.set_image(url=url)
        
        view = CatView(embed, site_url)
        view.message = await ctx.send(embed=embed, view=view)

        #await view.wait()
        #await msg.edit(embed=embed, view=None)
        
        
    @commands.hybrid_command(name="dog", aliases=['doge'])
    async def dog(self, ctx):
        site_url = "https://dog.ceo/api/breeds/image/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(site_url) as response:
                if response.status == 200:
                    data = await response.json()
                    url = data["message"]
                else:
                    await ctx.send("Unable to get an image, try again later", ephemeral=True)
                    return

        embed = discord.Embed(
            title = "doge",
            color = discord.Colour.random()
        )
        embed.set_footer(text = "www.dog.ceo")
        embed.set_image(url=url)
        
        view = DogView(embed, site_url)
        view.message = await ctx.send(embed=embed, view=view)

    #   await view.wait()
    #   await msg.edit(embed=embed, view=None)
            
    @app_commands.command(name="ping", description="Send the bots latency in milliseconds")
    async def ping(self, inter: discord.Interaction):
         await inter.response.send_message(f"Pong! {int(self.bot.latency * 1000)}ms")
            


        

async def setup(bot):
    await bot.add_cog(Misc(bot))

    
