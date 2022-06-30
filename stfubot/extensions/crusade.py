import disnake
import random
import datetime

from typing import List
from numpy.random import choice
from disnake.ext import commands

# ui
from stfubot.ui.paginator import Menu

# utils
from stfubot.utils.decorators import database_check
from stfubot.utils.fight_logic import fight_instance
from stfubot.utils.functions import secondsToText, format_combat_log

# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.models.gameobjects.stands import Stand, get_stand_from_template
from stfubot.models.gameobjects.ia import Ia
from stfubot.models.gameobjects.items import item_from_dict, get_item_from_template
from stfubot.globals.variables import (
    COINSGAINS,
    PLAYER_XPGAINS,
    STAND_XPGAINS,
    CRUSADEURL,
    CHANCEITEM,
    DONOR_CR_WAIT_TIME,
    NORMAL_CR_WAIT_TIME,
)
from stfubot.globals.emojis import CustomEmoji


class Crusade(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(
        name="crusade", description="fight random generated stand based on your level"
    )
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @database_check()
    async def crusade(self, Interaction: disnake.ApplicationCommandInteraction):

        # translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        # Check the time
        past_time = user.last_crusade
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        delta = now - past_time
        wait_time = DONOR_CR_WAIT_TIME + (not user.is_donator()) * NORMAL_CR_WAIT_TIME

        if delta.total_seconds() // 3600 < wait_time:
            wait_for = datetime.timedelta(hours=wait_time) - delta
            embed = disnake.Embed(
                title=translation["error_meesages"]["sorry_but"],
                description=translation["error_meesages"]["cool_down"].format(
                    "crusade", secondsToText(wait_for.total_seconds())
                ),
                color=disnake.Color.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        embed = disnake.Embed(
            title=translation["crusade"]["1"], color=disnake.Color.blue()
        )
        await Interaction.send(embed=embed)

        user.last_crusade = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        if user.level < 5:
            star = 3
            n = random.randint(1, 2)
        elif 5 <= user.level < 25:
            star = 4
            n = random.randint(1, 1)
        elif 25 <= user.level < 50:
            star = 5
            n = random.randint(2, 3)
        elif 50 <= user.level < 75:
            star = 5
            n = 3
        elif user.level >= 75:
            star = 6
            n = 3
        names = ["Megalo", "Mr Davelo", "Vince", "Icarus", "Arkkos", "Yoshikage Ramsay"]
        ennemy_data = {
            "name": f"{random.choice(names)}'s Soul",
            "avatar": None,
            "stands": [
                stand.to_dict() for stand in get_stands(self.stfubot, star=star, n=n)
            ],
        }
        ennemy = Ia(ennemy_data)
        players = [user, ennemy]
        channels = [Interaction.channel] * 2

        winner, combat_log = await fight_instance(
            players, channels, translation, ranked=False
        )
        embeds = format_combat_log(translation, combat_log)
        final_view = Menu(embeds)
        await Interaction.channel.send(embed=embeds[0], view=final_view)
        # Loose
        if not winner.is_human:
            embed = disnake.Embed(
                title=translation["crusade"]["2"], color=disnake.Color.blue()
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.channel.send(embed=embed)
            await user.update()
            return
        # Win
        # Guarented drops and stuff
        winner.xp += PLAYER_XPGAINS
        winner.coins += COINSGAINS
        for stand in winner.stands:
            stand.xp += STAND_XPGAINS
        embed = disnake.Embed(
            title=translation["crusade"]["3"], color=disnake.Color.blue()
        )
        embed.set_image(url=CRUSADEURL)
        embed.add_field(
            name=translation["crusade"]["4"],
            value=f"`{COINSGAINS}`{CustomEmoji.COIN}",
        )
        item_roll = random.randint(1, 100)
        if item_roll <= CHANCEITEM:
            id = random.choice([1, 2, 4])
            item = item_from_dict(get_item_from_template({"id": id}))
            embed.add_field(
                name=translation["crusade"]["5"], value=f"`{item.name}|`{item.emoji}"
            )
            user.items.append(item)
        await user.update()
        await Interaction.channel.send(embed=embed)


def get_stands(stfubot: StfuBot, star=4, n: int = 1) -> List[Stand]:
    leveled = [stand for stand in stfubot.stand_file if stand["stars"] == star]
    random_stand = [get_stand_from_template(stand) for stand in choice(leveled, size=n)]
    return random_stand


def setup(stfubot: StfuBot):
    stfubot.add_cog(Crusade(stfubot))
