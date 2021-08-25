import discord
from discord.ext import commands

# Settings and other useful commands that have nothing to do with the actual use of this bot
class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo_handler = self.bot.mongo_handler

    # Sets our bot's prefix
    @commands.command()
    async def prefix(self, ctx, new_prefix):
        if new_prefix != "":
            self.mongo_handler.update_server_configs({"_id": ctx.guild.id}, {"$set":{"prefix": new_prefix}})

            old_prefix = self.bot.command_prefix
            self.bot.command_prefix = new_prefix

            await ctx.channel.send(f"Prefix changed from `{old_prefix}` to `{new_prefix}`")
        else:
            await ctx.channel.send(f"My prefix is `{self.bot.command_prefix}`")

    @commands.command()
    async def help(self, ctx):
        pfx = self.bot.command_prefix

        embed = discord.Embed(title="Help has arrived!", color=self.bot.pick_embed_color())

        embed.add_field(
            name="Settings",
            value=f"`{pfx}help` - woah, a paradox!",
            inline=False
        )

        embed.add_field(
            name="Fun Stuff",
            value=f"`{pfx}say` | `{pfx}nou` | `{pfx}sus`",
            inline=False
        )

        embed.add_field(
            name="Misc",
            value=f"`{pfx}snipe` | `{pfx}ping`",
            inline=False
        )

        embed.add_field(
            name="Auto Moderator",
            value=f"`{pfx}setruleschannel` | `{pfx}toggleblacklist` | `{pfx}blacklistadd`",
            inline=False
        )

        embed.add_field(
            name="Admin",
            value=f"`{pfx}purge`",
            inline=False
        )

        embed.set_footer(text="Page 1/1")

        await ctx.reply(embed=embed, mention_author=False)