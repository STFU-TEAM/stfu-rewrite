import disnake
import random
import asyncio

from disnake.ext import commands, tasks

# stfu model
from stfubot.models.bot.stfubot import StfuBot

from typing import List


class Routines(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot
        self.change_presence.start()

    @tasks.loop(seconds=15 * 60)
    async def change_presence(self):
        quotes = [
            "Stfurequiem but better",
            "The start of a new era",
            "what the fuck is oatmeal",
            "your adventure has just begun",
            "the jojo reference singularity will one day be reached",
            "STAN Kelian",
            "STAN Vince",
            "being keyshiwophobic >>>>",
        ]
        quote = random.choice(quotes)
        await self.stfubot.change_presence(activity=disnake.Game(quote))


def setup(stfubot: StfuBot):
    stfubot.add_cog(Routines(stfubot))