import disnake
import topgg
import os
import datetime
import asyncio

from disnake.ext import commands, tasks

# globals
from stfubot.globals.variables import ARROW_VOTE, COINS_VOTE
from stfubot.globals.emojis import CustomEmoji

# utils
from stfubot.utils.decorators import database_check
from stfubot.utils.functions import secondsToText

# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.models.gameobjects.items import item_from_dict


class TopGG(commands.Cog):
    """
    This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.
    """

    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot
        self.token = os.environ["TOPGG"]  # set this to your DBL token
        self.dblpy = topgg.DBLClient(self.stfubot, self.token)
        self.update_stats.start()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        await self.stfubot.wait_until_ready()
        try:
            server_count = len(self.stfubot.guilds)
            await self.dblpy.post_guild_count(server_count)
            print("Posted server count ({})".format(server_count))
        except Exception as e:
            print("Failed to post server count\n{}: {}".format(type(e).__name__, e))

    @commands.slash_command(name="vote", description="vote to gain rewards !")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @database_check()
    async def vote(self, Interaction: disnake.ApplicationCommandInteraction):
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        translation = await self.stfubot.database.get_interaction_lang(Interaction)

        past_time = user.last_vote
        now = datetime.datetime.now()
        Delta = now - past_time
        wait_time = 12
        if Delta.total_seconds() // 3600 <= wait_time:
            wait_for = datetime.timedelta(hours=wait_time) - Delta
            embed = disnake.Embed(
                title=translation["error_meesages"]["error"],
                description=translation["error_meesages"]["cool_down"].format(
                    "vote", secondsToText(wait_for.total_seconds())
                ),
                color=disnake.Colour.blue(),
            )
            embed.set_thumbnail(
                url="https://cdn1.iconfinder.com/data/icons/finance-banking-and-currency-part-1/400/finance_2-512.png"
            )
            await Interaction.send(embed=embed)
            return
        embed = disnake.Embed(
            title=translation["vote"]["1"], color=disnake.Colour.blue()
        )
        embed.add_field(
            name=translation["vote"]["2"].format(CustomEmoji.LOADING_ICON),
            value=translation["vote"]["3"],
        )
        embed.set_image(url=self.stfubot.avatar_url)
        await Interaction.send(embed=embed)
        time = datetime.datetime.now()
        while not await self.dblpy.get_user_vote(user.discord.id):
            delta = datetime.datetime.now() - time
            if delta.total_seconds() > 5 * 60:
                raise TimeoutError
            await asyncio.sleep(10)
        user.coins += COINS_VOTE
        user.items + [item_from_dict({"id": 2})] * ARROW_VOTE
        embed = disnake.Embed(
            title=translation["vote"]["4"], color=disnake.Colour.blue()
        )
        embed.set_image(url=self.stfubot.avatar_url)
        embed.add_field(name=f"`Arrows:`", value=f"{ARROW_VOTE}{CustomEmoji.ARROW}"),
        embed.add_field(name=f"`Coins`:", value=f"{COINS_VOTE}{CustomEmoji.COIN}")
        await user.update()
        await Interaction.delete_original_message()
        await Interaction.channel.send(embed=embed)


def setup(stfubot: StfuBot):
    stfubot.add_cog(TopGG(stfubot))