#different commands go here lol

import discord
from discord.ext import commands
import asyncio
import os
from aiohttp import ClientSession
from utils.custom import TimeConverter
from utils.custom import GetMessage


class Misc(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"{self.__class__.__name__} Cog has been loaded\n----------------------------------------------------------")

    @commands.command(name="ping", description="Displays current latency.")
    async def _ping(self, ctx):
        await ctx.reply(f'Pong \nLatency: {round(bot.latency * 1000)}ms')

    @commands.command(name="hello", aliases=["hi"], description="Says hello.")
    async def _hello(self, ctx):
        responses = ['Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi']
        await ctx.reply(random.choice(responses))
    
    @commands.command(name="sum", aliases=["add"], description="Adds two numbers together.")
    async def _sum(self, ctx, numOne: int, numTwo: int):   
        await ctx.reply(numOne + numTwo)

    @commands.command(name="serverinfo", aliases=["guildinfo", "guild", "server"], description="Displays server information")
    async def _serverinfo(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", description="the info of the server", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        embed.set_thumbnail(url=f"{ctx.guild.icon}")
        embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

        await ctx.reply(embed=embed)

    @commands.command(name="count", description="Counts from 1 to 10.")
    async def _count(self, ctx):
        number = 0
        while number < 11:
            await ctx.send(number)
            number += 1
            asyncio.sleep(2)

    

def setup(bot):
    bot.add_cog(Misc(bot))
