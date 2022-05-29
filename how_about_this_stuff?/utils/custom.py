#useful things

import discord
from discord.ext import commands
import re
import asyncio

#not used but is an example check
def check_if_it_it_me():
  async def lol(ctx):
    return ctx.author.id == 763810207310544906
  return commands.check(lol)

#converts h|s|m|d into seconds
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}
class TimeConverter(commands.Converter):
  async def convert(self, ctx, argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
      try:
        time += time_dict[value] * float(key)
      except KeyError:
        raise commands.BadArgument(f"{value} is an invalid time key! h|m|s|d are valid arguments")
      except ValueError:
        raise commands.BadArgument(f"{key} is not a number!")
    return time

#sends an embed with 2 options and waits for a message reply
async def GetMessage(bot, ctx, contentOne="Default Message", contentTwo="\uFEFF", timeout=100):
    embed = discord.Embed(title=f"{contentOne}", description=f"{contentTwo}",)
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for("message", timeout=timeout, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        if msg:
          return sent, msg
    except asyncio.TimeoutError:
        return False