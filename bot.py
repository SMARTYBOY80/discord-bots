import discord
from discord.ext import commands, tasks
import json
from pathlib import Path
import datetime
import os
import asyncio
import pymongo
import motor.motor_asyncio
import socket
import requests

#makes json ussage easier
import utils.json
#makes db usage easier
from utils.mongo import Document

#gets current ip for config purposes
ip = requests.get('https://api.ipify.org').text
print(f"-----------------------------------------------------------------------------------------------------------------------------\
    \nCurrent IP: {ip}\n----------------------------------------------------------")


#defines and prints the cwd
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"CWD: {cwd}\n----------------------------------------------------------")

#gets the prefix from the database entry for the respective server
async def get_prefix(bot, message):
    #if DM
    if not message.guild:
        return commands.when_mentioned_or("xina ", "Xina ")(bot, message)

    #tries to find a db entry
    try:
        data = await bot.config.find(message.guild.id)

        if not data or "prefixes" not in data:
            return commands.when_mentioned_or('xina ', "Xina ")(bot, message)
        return commands.when_mentioned_or(*data["prefixes"])(bot, message)

    #returns default if no entry is found
    except:
        return commands.when_mentioned_or("xina ", "Xina ")(bot, message)

#allows the bot to read message content
intents = discord.Intents.default()
intents.members = True

#Defines the bot object
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents, help_command=None)

#gets the config file and respective information (the file should be /bot_config/secrets.json)
replit_file = json.load(open(cwd+"/bot_config/replit.json"))
if replit_file["onReplit"] == "no":  
    secret_file = json.load(open(cwd+"/bot_config/secrets.json"))
    bot.config_token = secret_file["token"]
    bot.config_token = secret_file["mongo"]
    bot.dad_joke_key = secret_file["DadjokeKey"]
else:
    bot.config_token = os.environ["token"]
    bot.config_token = os.environ["mongo"]
    bot.dad_joke_key = os.environ["DadjokeKey"]

#defines some variables
bot.version = "2.3.0"
bot.cwd = cwd

#defines hex values as colours
bot.colours = {
    "white":0xFFFFFF,
    "aqua":0x1ABC9C,
    "green":0x2ECC71,
    "blue":0x0061ff,
    "light_blue":0x3498DB,
    "purple":0x9B59B6,
    "pink":0xE91E63,
    "gold":0xF1C40F,
    "orange":0xE67E22,
    "red":0xE74C3C,
    "navy":0x34495E,
    "dark_aqua":0x11806A,
    "dark_green":0x1F8B4C,
    "dark_blue":0x206694,
    "dark_purple":0x71368A,
    "dark_pink":0xAD1457,
    "dark_gold":0xC27C0E,
    "dark_orange":0xA84300,
    "dark_red":0x992D22,
    "dark_navy":0x2C3E50,
    "black":0x020000
}
#allows random.choice to be used
bot.colour_list = [colour for colour in bot.colours.values()]

#when bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name} : {bot.user.id} \n----------------------------------------------------------")
    await bot.change_presence(activity=discord.Streaming(name="Tutorials", url="https://youtu.be/dQw4w9WgXcQ"))

    #attempts to connect to the database
    try:
        bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
        bot.db = bot.mongo["Xina_bot"]

        bot.config = Document(bot.db, "config")
        bot.blacklist = Document(bot.db, "blackist")
        bot.roles = Document(bot.db, "roles")

        blacklisted_users = await bot.blacklist.get_all()
        bot.blacklisted_users = {}
        for guild in blacklisted_users:
            users = guild["users"]
            server = guild["_id"]
            bot.blacklisted_users[server]=users
        
        DBroles = await bot.roles.get_all()
        bot.rolescache = {}
        for guild in DBroles:
            server = guild["_id"]
            roles = guild["roles"]
            bot.rolescache[server] = roles

    #cannot connect to database
    except Exception as error:
        print(f"!--------------------------------------------Database connection failed. :/--------------------------------------------!\
         \nTry checking whether the ip adress is allowed and that your connection code is accurate. {error}\
         \n!----------------------------------------------------------------------------------------------------------------------!")
        exit()
    else:     
        print(f"Initialized Database\n----------------------------------------------------------")
        
#checks every message to see if the bot has been mentioned
@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    try:
        if message.author.id in bot.blacklisted_users[message.guild.id]:
            return
    except:
        pass

    if message.content.startswith(f"<@!{bot.user.id}>"):
        try:
            data = await bot.config.find(message.guild.id)
            prefixes = data["prefixes"]
            await message.channel.send(f"The current prefixes for this server are: {prefixes}")
        except:
            await message.channel.send(f"The current prefixes for this server are 'xina ' and 'Xina '")
        
    await bot.process_commands(message)

#runs through /cogs/ and loads those as extentions (keeps the commands organised in seperate files)
if __name__ == "__main__":
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    #runs the bot
    bot.run(bot.config_token)