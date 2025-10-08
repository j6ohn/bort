from datetime import datetime, timedelta
import json
import os
import firebase_admin
from firebase_admin import credentials, db
from keep_alive import keep_alive
import requests
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
gronk = ('await bot.sync_commands()')



# Specify the allowed server ID
ALLOWED_GUILD_ID = 1415672029977383097  # Change this to your server's ID

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

    await bot.change_presence(activity=discord.Game(name="Tbs!!!!"))

    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

keep_alive()
bot.run(os.getenv("TOKEN"))
