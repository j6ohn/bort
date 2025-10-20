import re
import discord
from discord.ext import commands

class TBSDetector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages sent by bots
        if message.author.bot:
            return

        # Look for TBS followed by digits (e.g. TBS10)
        match = re.search(r'TBS(\d+)', message.content, re.IGNORECASE)
        if match:
            number = int(match.group(1))
            await message.channel.send(f"Detected TBS number: **{number}**")

async def setup(bot):
    await bot.add_cog(TBSDetector(bot))
