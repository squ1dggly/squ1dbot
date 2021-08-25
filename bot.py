from discord.ext import commands
from discord.colour import Color

import random
import asyncio

from cogs.fun_stuff import fun_stuff
from cogs.settings import settings
from cogs.auto_mod import auto_mod
from cogs.admin import admin
from cogs.misc import misc

from cogs.mongo import Mongo

TOKEN = "ODc4MTE2OTI1MTYxNDgwMjQy.YR8gHQ.dYxIf2_EXl2ylBp5MYlqKFI4oU0"

class bot(commands.Bot):
    def __init__(self):
        commands.Bot.__init__(self, command_prefix="s!", help_command=None)

        self.embed_colors = [Color(0x1B998B)]
        self.last_deleted_message = None

        self.guild_id = 0

        self.mongo_handler = Mongo()
        self.guild_query = {}

    async def on_ready(self):
        self.load_cogs()

        print(f"{self.user.name} has connected to discord")

    async def on_guild_join(self, guild):
        self.mongo_server_check(guild)

    async def on_message(self, msg):
        # if msg.guild.id != 878114455030992966: # Only allow it to work in the test server
        #     return

        if msg.author == self.user:
            return

        await self.process_commands(msg)

    async def on_message_delete(self, msg):
        if msg.author == self.user:
            return

        self.last_deleted_message = msg
        self.loop.create_task(self.reset_last_deleted_message())

    async def reset_last_deleted_message(self):
        await asyncio.sleep(10)
        self.last_deleted_message = None

    def pick_embed_color(self):
        return random.choice(self.embed_colors)

    def load_cogs(self):
        self.add_cog(fun_stuff(self))
        self.add_cog(settings(self))
        self.add_cog(auto_mod(self))
        self.add_cog(admin(self))
        self.add_cog(misc(self))

    def mongo_guild_setup(self, guild):
        self.guild_id = guild.id

        if self.mongo_handler.count_documents_in_server_configs({"_id": guild.id}) == 0:
            base_data = {
                "_id": guild.id,
                "prefix": self.command_prefix,
                "blacklist_toggle": False,
                "blacklisted_words": [],
                "server_rules_channel": None
            }

            self.mongo_handler.append_to_server_configs(base_data)

            query = self.mongo_handler.get_guild_user(guild.id)
            for q in query:
                self.guild_query = q
                
            print("server added to mongo")
        else:
            # Get server data and stuff
            print("loading mongo data")

            query = self.mongo_handler.get_guild_user(guild.id)
            
            for q in query:
                self.guild_query = q

            self.command_prefix = q["prefix"]

            _auto_mod = self.get_cog("auto_mod")
            _auto_mod.blacklist_check_enabled = q["blacklist_toggle"]
            _auto_mod.blacklisted_words = q["blacklisted_words"]
            _auto_mod.rules_channel = self.get_channel(q["server_rules_channel"])

            print("finished loading mongo data")

bot = bot()
bot.run(TOKEN)