import discord
from discord.ext import commands

prefix = '-'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

token = ""

# Events
@bot.event
async def on_ready():    
    bot.load_extension('cogs.ticket')

bot.run(token)
