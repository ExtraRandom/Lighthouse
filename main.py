import discord
import os
from discord.ext import commands
from datetime import datetime
import json


def get_prefix(d_bot, message):
    prefixes = ["?"]
    return commands.when_mentioned_or(*prefixes)(d_bot, message)


class BlueBot(commands.Bot):
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.last_token_msg_time = None
        self.last_token_msg = None

        super().__init__(
            command_prefix=get_prefix,
            description="THE LIGHTHOUSE BOT\n"
                        "Developed by @Extra_Random#2564\n"
                        "Source Code: "
                        "",
                        # "https://discord.gg/EaBKarE",
            pm_help=False
            )
        # self.add_command()

    async def on_ready(self):
        login_time = datetime.now()

        file = os.path.join(self.base_dir, "settings.json")
        settings_data = self.json_read(file)
        if settings_data:
            settings_data['info']['last-login'] = str(login_time)
            self.json_write(settings_data, file)

        login_msg = "Bot Logged In at {}".format(login_time)
        # write to log
        print(login_msg)

    async def on_message(self, msg):
        """Spam Filtering is handled in the chat_filtering cog"""
        if msg.author.bot is True:
            return
        else:
            await self.process_commands(msg)

    async def on_command_error(self, ctx, error):
        channel = ctx.message.channel

        if isinstance(error, commands.MissingRequiredArgument):
            await self.show_cmd_help(ctx)
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            await channel.send("You do not have permission to use that command!")
            return
        elif isinstance(error, commands.CommandOnCooldown):
            await channel.send("This command is currently on cooldown. {}" 
                               "".format(str(error).split(". ")[1]))
            return
        else:
            """Error logging goes here"""
            """For now tho lets just say there was an error"""
            channel.send("Error:\n{}".format(error))
            return

    @staticmethod
    async def show_cmd_help(ctx):
        formatter = commands.formatter.HelpFormatter()
        f_help = await formatter.format_help_for(ctx, ctx.command)
        cmd_info = f_help[0]
        await ctx.send(cmd_info)

    @staticmethod
    def json_read(file_path):
        try:
            with open(file_path, "r") as file:
                return json.loads(file.read())
        except Exception as e:
            # log e
            return None

    @staticmethod
    def json_write(data, file_path):
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
                return True
        except Exception as e:
            # log e
            return False

    @staticmethod
    def ensure_all_fields(first_run, settings_data):
        fields = \
            {
                "keys": {
                        "discord-token": None
                    },
                "cogs": {},
                "info": {
                    "last-login": None
                }
            }
        if first_run:
            return fields
        else:
            for top_field in fields:
                if top_field in settings_data:
                    for inner_field in fields[top_field]:
                        if inner_field not in settings_data[top_field]:
                            settings_data[top_field][inner_field] = None
                            print("Settings.json - Missing field '{}' added to category '{}'".format(inner_field,
                                                                                                      top_field))
                else:
                    settings_data[top_field] = {}

                    print("Settings.json - Missing category '{}' Added".format(top_field))

                    for inner_field in fields[top_field]:
                        if inner_field not in settings_data[top_field]:
                            settings_data[top_field][inner_field] = None
                            print("Settings.json - Missing field '{}' added to category '{}'".format(inner_field,
                                                                                                   top_field))
            return settings_data

    def get_cogs_in_folder(self):
        cogs_dir = os.path.join(self.base_dir, "cogs")
        cogs_list = []

        if os.path.exists(cogs_dir) is False:
            os.mkdir(cogs_dir)
            print("Warning: The cogs folder wasn't found, a new one will be made but won't contain any cogs. "
                  "Check you didn't accidentally delete it!")
            return []  # no cogs will exist if the folder doesn't exist for some reason

        for file in os.listdir(cogs_dir):
            if file.endswith(".py"):
                cogs_list.append(file.replace(".py", ""))
        return cogs_list

    def run(self):
        first_run = False
        settings_data = {}
        settings_filepath = os.path.join(self.base_dir, "settings.json")

        """Check if this is first run"""
        if os.path.isfile(settings_filepath) is False:
            print("First Time Run")
            first_run = True
        else:
            settings_data = self.json_read(settings_filepath)
            if settings_data is None:
                print("Error Reading settings.json, Please check the file.")
                # first_run = True
                # settings_data = {}

        """Ensure all necessary fields exist"""
        settings_data = self.ensure_all_fields(first_run, settings_data)

        """Load cogs"""
        folder_cogs = self.get_cogs_in_folder()
        for f_cog in folder_cogs:
            cog_path = "cogs.{}".format(f_cog)
            if first_run:
                settings_data['cogs'][f_cog] = True
            else:
                try:
                    load_cog = settings_data['cogs'][f_cog]
                except KeyError:
                    settings_data['cogs'][f_cog] = True
                    load_cog = True

                if load_cog:
                    try:
                        self.load_extension(cog_path)
                    except Exception as exc:
                        print("Failed to load cog '{}', Reason: {}".format(
                            f_cog, type(exc).__name__))
                        settings_data['cogs'][f_cog] = False

        """Read in discord token"""
        if first_run:
            token = None
        else:
            token = settings_data['keys']['discord-token']

        if self.json_write(settings_data, settings_filepath) is False:
            # Failed to write settings.json
            print("Failed to write settings.json, that's probably not good")
            return

        if token is None:
            print("Discord Bot Token isn't set! Please go to {} and set it!".format(settings_filepath))
            return
        else:
            super().run(token)


if __name__ == '__main__':
    the_bot = BlueBot()
    the_bot.run()


