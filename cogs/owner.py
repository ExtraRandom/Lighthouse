import discord
from discord.ext import commands
from datetime import datetime, timedelta
from cogs.utils import perms
import os


class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @perms.is_bot_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot"""
        print("Shutting Down")
        await ctx.send("Shutting down...")
        await self.bot.logout()

    @commands.command(hidden=True)
    @perms.is_bot_owner()
    async def avatar(self, ctx, image: str):
        """"Change the bot's avatar"""
        try:
            with open(os.path.join(self.bot.base_dir, image), "rb") as avatar:
                f = avatar.read()
                image_bytes = bytearray(f)
                await self.bot.user.edit(avatar=image_bytes)
        except Exception as e:
            await ctx.send("Failed to change avatar")
            print(e)

    @commands.command()
    async def uptime(self, ctx):
        """Shows the bots current uptime"""
        try:
            data = self.bot.json_read(self.bot.settings_file)

            login_time = datetime.strptime(data['info']['last-login'], "%Y-%m-%d %H:%M:%S.%f")
            now = datetime.now()
            difference = int(round(now.timestamp() - login_time.timestamp()))
            uptime = str(timedelta(seconds=difference))

            await ctx.send("Bot Uptime: {}".format(uptime))

        except Exception as e:
            await ctx.send("Error getting bot uptime. Reason: {}".format(type(e).__name__))

def setup(bot):
    n = Owner(bot)
    bot.add_cog(n)

