import discord
from discord.ext import commands

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def snipe(self, ctx):
        last_msg = self.bot.last_deleted_message

        if not last_msg:
            await ctx.channel.send("No message found! They're a tricky one, that's for sure.", delete_after=4)
            return

        embed = discord.Embed(color=self.bot.pick_embed_color())
        
        embed.add_field(
            name=f"{last_msg.author.display_name} said:",
            value=last_msg.content
        )

        embed.set_footer(text="pew pew!")

        await ctx.reply(embed=embed, mention_author=False)

    # Tells us the bot's current latency with discord
    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f"Pong! {round(self.bot.latency, 1)}ms")