import discord
from discord.ext import commands
from discord.ext.commands.core import command

def check_for_blacklisted_words(msg, blacklist):
    _msg = msg.content.lower()
    for word in blacklist:
        if word in _msg:
            return True
    return False

class auto_mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo_handler = self.bot.mongo_handler

        self.blacklist_check_enabled = False
        self.blacklisted_words = []
        self.rules_channel = None

    # TODO: FIX
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.guild.id != 878114455030992966: # Only allow it to work in the test server
            return

        if msg.author == self.bot.user:
            return

        if msg.content.replace(" ", "") == "":
            return
    
        if self.blacklist_check_enabled:
            if check_for_blacklisted_words(msg, self.blacklisted_words):
                await msg.delete()

                if self.rules_channel == None:
                    await msg.channel.send(f"{msg.author.mention} your message had one or more blacklisted words in it.\nPlease read the rules.", delete_after=4)
                else:
                    await msg.channel.send(f"{msg.author.mention} your message had one or more blacklisted words in it.\nPlease read the rules in {self.rules_channel.mention}", delete_after=4)

    @commands.command()
    async def setruleschannel(self, ctx):
        if len(ctx.message.channel_mentions) == 0:
            await ctx.reply("Please mention a channel to set as the server rules channel.", delete_after=4)
            return

        if ctx.message.content.lower() == "reset":
            self.rules_channel = None
            await ctx.reply("Server rules channel reset to none.")
            self.mongo_handler.update_server_configs({"_id": self.bot.guild_id}, {"$set":{"server_rules_channel": None}})
            return

        self.rules_channel = ctx.message.channel_mentions[0]
        self.mongo_handler.update_server_configs({"_id": self.bot.guild_id}, {"$set":{"server_rules_channel": ctx.message.channel_mentions[0].id}})
        await ctx.reply(f"Server rules channel set to {self.rules_channel.mention}.")

    @commands.command()
    async def toggleblacklist(self, ctx):
        self.blacklist_check_enabled = not self.blacklist_check_enabled
        self.mongo_handler.update_server_configs({"_id": self.bot.guild_id}, {"$set":{"blacklist_toggle": self.blacklist_check_enabled}})
        await ctx.reply(f"Blacklist check set to {self.blacklist_check_enabled}.")

    @commands.command()
    async def blacklistadd(self, ctx, *args):
        _msg = ""
        for arg in args:
            _msg += arg + " "
        _msg = _msg[0:len(_msg)-1]

        if _msg.replace(" ", "") == "":
            await ctx.reply("There's nothing to add! Use `,` to seperate your blacklisted words.", delete_after=4)
            return

        new_words = _msg.split(",")

        for word in new_words:
            self.blacklisted_words.append(word)

        self.mongo_handler.update_server_configs({"_id": self.bot.guild_id}, {"$set":{"blacklisted_words": self.blacklisted_words}})

        await ctx.reply("Blacklist updated.")