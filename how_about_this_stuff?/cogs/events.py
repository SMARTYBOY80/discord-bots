import discord
from discord.ext import commands
import asyncio
import os
from aiohttp import ClientSession
from utils.custom import TimeConverter
from utils.custom import GetMessage

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------------------------------------------")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return
        
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.reply(f"You must wait {int(s)} seconds to use this command!")
            elif int(h) == 0 and int(m) != 0:
                await ctx.reply(f"You must wait {int(m)} minutes and {int(s)} seconds to use this command!")
            else:
                await ctx.reply(f"You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!")
            return

        elif isinstance(error, commands.CheckFailure):
            await ctx.reply("You can't do this :/")
            return
        raise error

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("member joined")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print("member left")

def setup(bot):
    bot.add_cog(Events(bot))
