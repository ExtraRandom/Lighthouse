import discord
from discord.ext import commands
from datetime import datetime
from cogs.utils import perms
import os


class PermTest:
    """"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['boop'])
    @perms.is_bot_owner()
    async def bot_owner_perm(self, ctx):
        await ctx.send("Yeah you got bot owner perms {}".format(ctx.author.mention))

    @commands.command(hidden=True, aliases=['sop', 'soup'])
    @perms.is_server_owner()
    async def server_owner_perm(self, ctx):
        await ctx.send("Yeah you got server owner perms {}".format(ctx.author.mention))

    @commands.command(hidden=True)
    @perms.is_bot_owner()
    async def repeat(self, ctx, *, term: str):
        await ctx.send(term)

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

def setup(bot):
    n = PermTest(bot)
    bot.add_cog(n)

