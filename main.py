import discord
from discord.ext import commands
import datetime
import random
import os

my_secret = os.environ['Token']


bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")

intents = discord.Intents.default()
intents.members=True

@bot.command()
async def ping(ctx):
  await ctx.send('pong')
  await ctx.send(f'Latency: {round(bot.latency * 1000)}ms')


@bot.command()
async def hello(ctx):
  responses = ['Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi']
  await ctx.send(random.choice(responses))


@bot.command()
async def credits(ctx):
    await ctx.send('Made by `SMARTYBOY80` and `samjamramman`')

@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="the info of the server", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)

# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Tutorials", url="https://youtu.be/dQw4w9WgXcQ"))
    print('My Ready is Body')

@bot.command()
async def count(ctx):
  number = 0
  while number <= 10:
    await ctx.send(number)
    number = number + 1

#@bot.event
#async def on_member_join(member):
  #await member.channel.send(f"welcome {member.mention}!")

@bot.event
async def on_member_leave(member):
  await member.channel.send("fuck you", {member.mention})

@bot.event
async def on_message_join(member):
    channel = bot.get_channel(957709508447203430)
    embed=discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!") # F-Strings!
    embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
    await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.ban(member)
    await ctx.send(f'User {member.mention} has been banned for{reason}')

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

  

@bot.command(description="mutes a specified user.")
@commands.has_permissions(manage_messages=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
  await member.add_roles(mutedRole)

  embed = discord.Embed(title="mute", description=f" muted-{member.mention}",colour=discord.Colour.light_gray())
  await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, question, option1=None, option2=None):
  if option1==None and option2==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = No**")
    await message.add_reaction('✅')
    await message.add_reaction('❎')
  elif option1==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = No**")
    await message.add_reaction('✅')
    await message.add_reaction('❎')
  elif option2==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = {option2}**")
    await message.add_reaction('✅')
    await message.add_reaction('❎')
  else:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = {option2}**")
    await message.add_reaction('✅')
    await message.add_reaction('❎')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
        limit = limit + 1
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
                          
bot.run(my_secret)

