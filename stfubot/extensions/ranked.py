import disnake
import random
import asyncio
import time

from disnake.ext import commands, tasks
from datetime import datetime

# stfu model
from stfubot.models.bot.stfubot import StfuBot

# utils
from stfubot.utils.decorators import database_check

# ui
from stfubot.ui.cancelbutton import CancelButton


class Ranked(commands.Cog):
    def __init__(self, client: StfuBot):
        self.stfubot: StfuBot = client

    @commands.slash_command(
        name="ranked",
        description="make a match against people in different server",
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @database_check()
    async def ranked(self, Interaction: disnake.ApplicationCommandInteraction):
        # check if the ranked matchmaking is running
        if not self.stfubot.MatchMaking_Is_Running:
            embed = disnake.Embed(
                title="An error has occurred",
                description=f"The ranked queu is disable check out https://discord.gg/stfurequiem",
                color=disnake.Color.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
            return
        join_time = time.time()
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        # check if the user has a stand
        if user.stands == []:
            embed = disnake.Embed(
                title="An error has occurred",
                description=f"It seems you don't have any stand...",
                color=disnake.Color.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
            return
        # match macking
        embed = disnake.Embed(title="Searching for a match", color=disnake.Color.blue())
        embed.set_image(
            url="https://media1.tenor.com/images/dee343e2c5b6b795ad86f863413bca95/tenor.gif?itemid=14148346"
        )
        embed.add_field(
            name="See the leaderboard here:",
            value="the Leaderboard will be back soon !",
        )
        embed.set_footer(
            text=f"There is {await self.stfubot.database.cache.len_ranked_queu()} players in queue"
        )
        view = disnake.ui.View(timeout=None)
        view.value = None
        view.add_item(CancelButton())
        await Interaction.send(embed=embed, view=view)
        # join the queue
        await self.stfubot.ranked_queue.join(Interaction)
        dt = time.time()
        q = await self.stfubot.database.cache.len_ranked_queu()
        left = False
        reason = "leave"
        # wait for a match
        while not await self.stfubot.ranked_queue.matchIsFound(Interaction):
            await asyncio.sleep(0.1)
            # refresh the message for new players
            if (
                time.time() - dt >= 5
                and q != await self.stfubot.database.cache.len_ranked_queu()
            ):
                embed.set_footer(
                    text=f"There is {await self.stfubot.database.cache.len_ranked_queu()} players in queue"
                )
                await Interaction.edit_original_message(embed=embed)
                dt = time.time()
            # cancel our placement in the matchmaking
            if view.value == "cancel":
                await self.stfubot.ranked_queue.leave(Interaction, "leave")
                left = True
                break
            if join_time <= self.stfubot.ranked_queue.last_reset:
                await self.stfubot.ranked_queue.join(Interaction)
        else:
            if not left:
                reason = await self.stfubot.ranked_queue.get_reason(Interaction)
        # send a message according to the reason received
        if reason == "already":
            await Interaction.channel.send(
                f"Hey {Interaction.author.mention} you seems to be already in a match ? if this is an error check our server"
            )
        elif reason == "leave":
            await Interaction.channel.send(
                f"Hey {Interaction.author.mention} your left the queue !"
            )
        elif reason == "kick":
            await Interaction.channel.send(
                f"Hey {Interaction.author.mention} you have been kicked from matchmaking ,an error prevented me from creating the match :/"
            )
        elif reason == "match":
            await Interaction.channel.send(
                f"Hey {Interaction.author.mention} your match is ready !"
            )
        else:
            await Interaction.channel.send(
                f"Hey {Interaction.author.mention} you left matchmaking for some reason"
            )
        await Interaction.delete_original_message()


def setup(stfubot: StfuBot):
    stfubot.add_cog(Ranked(stfubot))