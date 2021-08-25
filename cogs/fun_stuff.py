import discord
from discord.ext import commands

import random

class fun_stuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *args):
        await ctx.message.delete()
        
        if len(args) == 0:
            await ctx.channel.send("I can't send an empty message, bruh.", delete_after=4)
            return

        response = ""
        for arg in args:
            response += arg + " "
        response = response[0:len(response)-1]

        await ctx.channel.send(response)

    @commands.command()
    async def nou(self, ctx):
        no_u_cards = [
            'https://cdn.discordapp.com/emojis/748177980626567189.gif', # Anime
            'https://cdn.discordapp.com/emojis/701465549145767999.gif', # Rainbow
            'https://cdn.discordapp.com/emojis/528389554676432906.png', # Red
            'https://cdn.discordapp.com/emojis/528389554445484033.png', # Blue
            'https://cdn.discordapp.com/emojis/528389554739347466.png', # Yellow
            'https://cdn.discordapp.com/emojis/528389554554667028.png' # Green
        ]

        embed = discord.Embed(title="no u", color=self.bot.pick_embed_color())

        embed.set_image(url=random.choice(no_u_cards))
        embed.set_footer(text="hah got em")

        await ctx.channel.send(embed=embed)

    @commands.command()
    async def sus(self, ctx):
        await ctx.channel.send("That's kinda sus ngl.")