import os
import disnake

from disnake.ext import commands
from statcord import StatcordClient

from stfubot.models.bot.stfubot import StfuBot


class MyStatcordCog(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot
        self.key = os.environ["STATCORD"]
        self.statcord_client = StatcordClient(stfubot, self.key)


def setup(bot: StfuBot):
    bot.add_cog(MyStatcordCog(bot))