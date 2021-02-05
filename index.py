import discord
from discord.ext import commands

prefix = '-'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

token = "NjkwMjI2ODY0MjcwMjEzMzUw.XnOV3A.9sgaOII8FZFzgbOz_9t_tiScj-Q"

# Events
@bot.event
async def on_ready():    
    bot.load_extension('cogs.ticket')

bot.run(token)
