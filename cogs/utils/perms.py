from discord.ext import commands
import discord


def is_bot_owner():
    def predicate(ctx):
        return ctx.message.author.id == 92562410493202432
    return commands.check(predicate)


def is_server_owner():
    def predicate(ctx):
        return ctx.message.author.id in [
            92562410493202432, 328310056754085888, 414585192896921600]
    return commands.check(predicate)




