import re
import discord
from discord.ext import commands

# CHANGE THIS if you ever want to use a different channel
TARGET_CHANNEL_ID = 1427648895839895634

class TBSChannelRenamer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # compile once
        self._regex = re.compile(r'\bTBS\s*(\d+)\b', re.IGNORECASE)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ignore bots and DMs
        if message.author.bot or message.guild is None:
            return

        # only respond for the configured channel
        if message.channel.id != TARGET_CHANNEL_ID:
            return

        match = self._regex.search(message.content)
        if not match:
            return

        number = match.group(1)  # as string
        # build a safe channel name: lowercase, no spaces, keep - and _
        new_name = f"tbs-{number}".lower()
        new_name = re.sub(r'[^a-z0-9-_]', '', new_name)

        # don't rename if it's already the same
        try:
            current_name = message.channel.name
        except Exception:
            current_name = None

        if current_name == new_name:
            # already named correctly — just react to confirm detection
            try:
                await message.add_reaction("✅")
            except Exception:
                pass
            return

        # Attempt to rename the channel
        try:
            await message.channel.edit(name=new_name)
            # react to the user's message as confirmation
            try:
                await message.add_reaction("✅")
            except Exception:
                pass
        except discord.Forbidden:
            # bot lacks Manage Channels permission
            try:
                await message.channel.send(
                    "I can't rename this channel — I need the **Manage Channels** permission."
                )
            except Exception:
                pass
        except discord.HTTPException as e:
            # general HTTP error (rate limit, invalid name, etc.)
            try:
                await message.channel.send(f"Failed to rename channel: {e}")
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(TBSChannelRenamer(bot))
