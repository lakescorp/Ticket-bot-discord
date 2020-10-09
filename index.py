import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='-')
token = ""

# Events
@bot.event
async def on_ready():    
    bot.load_extension('cogs.ticket')

bot.run(token)
