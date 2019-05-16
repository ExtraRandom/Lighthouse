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
        self.bad_words = ["kill", "murder", "blood", "cull", "culling", "gas", "chambers", "genocide", "eliminate",
                          "destroy", "overthrow"]
        self.bad_words_temp = []
        self.token_stfu_warn_time = None

    @commands.command(aliases=['stfutoken', "tstfu"], hidden=True, name="tokenstfu")
    @perms.is_token_stfu_controller()
    async def token_stfu_toggle_command(self, ctx):
        """Toggles Auto-Deletion of Token messages with bad words"""
        self.token_stfu = not self.token_stfu
        await ctx.send("Token STFU is now {}".format(self.token_stfu))

    @commands.command(hidden=True, name="tokenadd", aliases=['tokenstfuadd', 'stfuadd', 'badword'])
    @perms.is_token_stfu_controller()
    async def token_stfu_add_temp_word(self, ctx, *, word: str):
        """Add temporary word to Token bads word list

        I'll add a better solution than this in the future, if still needed"""
        if word in self.bad_words_temp or word in self.bad_words:
            await ctx.send("'{}' is already a blocked word".format(word))
            return
        else:
            self.bad_words_temp.append(word)
            await ctx.send("'{}' added to temporary bad word list".format(word))
            return

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
            if msg.channel.id in [575848857926107136, 223132558609612810]:  # TODO add other channels to block
                if self.token_stfu is True:
                    msg_fmt = str(msg.clean_content).lower()
                    if msg_fmt in self.bad_words or msg_fmt in self.bad_words_temp:
                        await msg.delete()

                        if self.token_stfu_warn_time is not None:
                            last_warn_time = datetime.now() - self.token_stfu_warn_time
                            if last_warn_time.seconds >= 20:
                                await msg.channel.send("{} STFU!".format(msg.author.mention))
                                self.token_stfu_warn_time = datetime.now()

                        elif self.last_token_msg_time is None:
                            await msg.channel.send("{} STFU!".format(msg.author.mention))
                            self.token_stfu_warn_time = datetime.now()

    async def invite_blocker(self, msg):
        """https://discord.gg/"""
        return


def setup(bot):
    n = ChatFilter(bot)
    bot.add_cog(n)
    bot.add_listener(n.token_spam_stopper, "on_message")
    bot.add_listener(n.token_stfu_enforcer, "on_message")


