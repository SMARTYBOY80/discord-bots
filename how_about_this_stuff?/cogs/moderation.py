import discord
from discord.ext import commands
import asyncio
import os
from aiohttp import ClientSession
from utils.custom import TimeConverter
from utils.custom import GetMessage


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----------------------------------------------------------")

    @commands.command(name="ban", description="Bans a member from the server.")
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(member)
        if reason:
            await ctx.send(f'User {member.mention} has been banned for{reason}.')
        else:
            await ctx.send(f'User {member.mention} has been banned.')

    @commands.command(name="kick", description="kicks a member from the server")
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(member)
        if reason:
            await ctx.send(f'User {member.mention} has been kicked for {reason}.')
        else:
            await ctx.send(f'User {member.mention} has been kicked.')

    @commands.command(name="mute", description="mutes a specified user.")
    @commands.has_permissions(administrator=True)
    async def _mute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(mutedRole)

        embed = discord.Embed(title="mute", description=f" muted-{member.mention}",colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)

    @commands.command(name="unmute", description="Unmutes a specified user.")
    @commands.has_permissions(administrator=True)
    async def _unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, limit: int):
        limit = limit + 1
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Moderation(bot))