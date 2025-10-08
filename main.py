from datetime import datetime, timedelta
import json
import os
import firebase_admin
from firebase_admin import credentials, db
from keep_alive import keep_alive
import requests
import discord
from discord.ext import commands, tasks
from discord import Option

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
ROLE_ID = 976330092693311548  

result_channel_id = 1270428610448068649
AUTHORIZED_USERS = [383004753459806217, 1214104505243930645, 166304067579019265, 259429005499957249]
CHANNEL_IDS = [977563049001115738, 977563149307887637, 976305065923076106]
penismen = [259429005499957249, 1214104505243930645, 242440226931212300, 267399123089489920, 166304067579019265, 383004753459806217]

# Specify the allowed server ID
ALLOWED_GUILD_ID = 970757427169484890  # Change this to your server's ID

cred_data = json.loads(os.getenv('cred'))
cred = credentials.Certificate(cred_data)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://manifest-pride-395502-default-rtdb.firebaseio.com/'
})

# Load extensions (cogs)
extensions = [
    'cogs.RoleCog',
    'cogs.mod1Commands',
    'cogs.slowmode',
    'cogs.MemberCountUpdater',
    'cogs.Tf2UpdateRelay',
    'cogs.LevelingSystem',
    'cogs.EmojiAdder',
    'cogs.Giveaway',
    'cogs.TF2AI',    
    'cogs.strike',
    'cogs.MentionAble',
    'cogs.ReactionTrigger',
    'cogs.ReactionHandler',
    'cogs.Punishments',
    'cogs.TF2ServerStatus',    
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f'Successfully loaded {extension}')
        except Exception as e:
            print(f'Failed to load {extension}: {e}')

# Global check for authorized users AND server restriction
@bot.check
async def globally_check(ctx):
    if ctx.guild and ctx.guild.id == ALLOWED_GUILD_ID:  # Allow commands only in the specified server
        return True  # Anyone in the server can use commands
    return False  # Ignore commands outside the server# Ignore commands outside the allowed server

@bot.event
async def on_ready():
    guild = discord.Object(id=ALLOWED_GUILD_ID)
    await bot.sync_commands()

    await bot.change_presence(activity=discord.Game(name="Team Fortress 2"))

    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

keep_alive()
bot.run(os.getenv("TOKEN"))
