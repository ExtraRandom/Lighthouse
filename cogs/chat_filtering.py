import discord
from discord.ext import commands
from datetime import datetime
from cogs.utils import perms


class ChatFilter:
    def __init__(self, bot):
        self.bot = bot

        self.last_token_msg = None
        self.last_token_msg_time = None

        self.token_stfu = False
        self.last_token_stfu_warning = None
        self.bad_words = ["kill", "murder", "blood", "cull", "culling", "gas", "chambers", "genocide", "eliminate",
                          "destroy", "overthrow"]

        # self.image_lockdown_list = []
        # self.image_lockdown_start_time = None

    @commands.command(aliases=['stfutoken', "tstfu"], hidden=True, name="tokenstfu")
    @perms.is_token_stfu_controller()
    async def token_stfu(self, ctx):
        """Toggles Auto-Deletion of all Token's new messages"""
        self.token_stfu = not self.token_stfu
        await ctx.send("Token STFU is now {}".format(self.token_stfu))

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

    async def token_stfu_enforcer(self, msg):
        if msg.author.id == 328310056754085888:  # 92562410493202432:   # id for testing
            if msg.channel.id in [575848857926107136]:  # TODO add other channels to block
                if self.token_stfu is True:
                    if self.bad_words in str(msg.clean_content).lower():
                        await msg.delete()

                        last_warn_time = datetime.now() - self.last_token_msg_time
                        if last_warn_time.seconds >= 20:
                            await msg.channel.send("{} STFU!".format(msg.author.mention))


    async def invite_blocker(self, msg):
        """https://discord.gg/"""
        return


def setup(bot):
    n = ChatFilter(bot)
    bot.add_cog(n)
    bot.add_listener(n.token_spam_stopper, "on_message")
    bot.add_listener(n.token_stfu_enforcer, "on_message")
    # bot.add_listener(n.image_lockdown, "on_message")


