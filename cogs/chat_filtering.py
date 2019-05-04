import discord
from discord.ext import commands
from datetime import datetime
from cogs.utils import perms


class ChatFilter:
    def __init__(self, bot):
        self.bot = bot
        self.last_token_msg = None
        self.last_token_msg_time = None

    async def token_spam_stopper(self, msg):
        if msg.author.id == 328310056754085888:  # 92562410493202432:   # id for testing
            if self.last_token_msg is None and msg.clean_content is not None:
                self.last_token_msg = msg.clean_content
            elif msg.clean_content == self.last_token_msg and msg.clean_content is not None:
                time_since_last = datetime.now() - self.last_token_msg_time  # print(time_since_last.seconds)
                if time_since_last.seconds >= 20:
                    # after 20 seconds ignore repeats as its unlikely to be real spam
                    pass
                else:
                    await msg.delete()
                    print("Deleted token spam")
            self.last_token_msg = msg.clean_content
            self.last_token_msg_time = datetime.now()

    async def invite_blocker(self, msg):
        """https://discord.gg/"""
        return

def setup(bot):
    n = ChatFilter(bot)
    bot.add_listener(n.token_spam_stopper, "on_message")
    bot.add_cog(n)

