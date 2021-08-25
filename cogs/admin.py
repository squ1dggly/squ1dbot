from discord.ext import commands
from discord.ext.commands.core import command

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup(self, ctx):
        if ctx.message.author.id != 227851838572068875:
            return

        await ctx.channel.send("Reving up our engines...")

        self.bot.mongo_guild_setup(ctx.guild)

        await ctx.channel.send("Bot setup complete.")

    @commands.command()
    async def purge(self, ctx, amt=0):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.channel.send("You need admin perms to use this command you fool!", delete_after=4)
            return

        if amt == 0:
            await ctx.channel.send("Please specify how many messages you would like to clear.", delete_after=4)
            return
            
        await ctx.channel.purge(limit=amt+1)
        await ctx.channel.send(f"{amt} messages deleted.", delete_after=2)