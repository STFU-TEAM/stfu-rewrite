import disnake
import json
import random
import asyncio

from disnake.ext import commands

# ui
from stfubot.ui.pve.tower_select import TowerSelectDropdown
from stfubot.ui.confirmation import Confirm
from stfubot.ui.place_holder import PlaceHolder

# utils
from stfubot.utils.decorators import database_check
from stfubot.utils.fight_logic import fight_instance
from stfubot.utils.functions import wait_for
from stfubot.utils.image_generators import tower_images

# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.models.gameobjects.ia import Ia
from stfubot.models.gameobjects.items import item_from_dict, get_item_from_template
from stfubot.globals.variables import (
    PLAYER_XPGAINS,
    STAND_XPGAINS,
    ENTRYCOST,
    TOWERURL,
)
from stfubot.globals.emojis import CustomEmoji


class Tower(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot
        with open("stfubot/data/static/tower.json", "r") as item:
            self.tower_file = json.load(item)["towers"]

    @commands.slash_command(
        name="tower", description="Enter towers to farm items and stands !"
    )
    @database_check()
    async def tower(self, Interaction: disnake.ApplicationCommandInteraction):
        # translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        # Check entry cost

        entry = f"{ENTRYCOST}{CustomEmoji.COIN}"
        balance = f"{user.coins}{CustomEmoji.COIN}"
        embed = disnake.Embed(
            title=translation["tower"]["1"].format(entry, balance),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=TOWERURL)
        view = Confirm(Interaction)

        await Interaction.send(embed=embed, view=view)
        await wait_for(view)

        Interaction = view.interaction

        if not view.value:
            embed = disnake.Embed(
                title=translation["tower"]["2"], color=disnake.Color.blue()
            )
            embed.set_image(url=TOWERURL)
            await Interaction.response.edit_message(embed=embed, view=PlaceHolder())
            return
        if user.coins < ENTRYCOST:
            amount = f"{ENTRYCOST-user.coins}{CustomEmoji.COIN}"
            embed = disnake.Embed(
                title=translation["tower"]["3"].format(amount),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=TOWERURL)
            await Interaction.response.edit_message(embed=embed, view=PlaceHolder())
            return

        # Level selection

        user.coins -= ENTRYCOST
        await user.update()
        view = TowerSelectDropdown(Interaction)
        await Interaction.response.edit_message(embed=embed, view=view)
        await wait_for(view)
        tower_id = view.value
        tower = self.tower_file[f"{tower_id}"]

        # fights
        for i, stands in enumerate(tower["fighters"]):
            file = await tower_images[f"{tower_id}"](user.discord, i + 1)
            embed = disnake.Embed(color=disnake.Color.blue())
            embed.set_image(file=file)

            Stage = await Interaction.channel.send(embed=embed)

            await asyncio.sleep(2)

            await Stage.delete()

            ennemy_data = {
                "name": f"{tower['names'][i]}",
                "avatar": None,
                "stands": stands,
            }

            ennemy = Ia(ennemy_data)
            players = [user, ennemy]
            channels = [Interaction.channel] * 2
            winner, combat_log = await fight_instance(
                players, channels, translation, ranked=False
            )
            if not winner.is_human:
                # The Person has lost
                break
        for stand in user.stands:
            stand.xp += int(STAND_XPGAINS * (tower["levels"] + 1 / (i + 1)))
        user.xp += int(PLAYER_XPGAINS * (tower["levels"] + 1 / (i + 1)))
        tower["rewards"].sort(key=lambda x: x["p"], reverse=True)
        # What happens when you gain no items
        if tower["unlocks"][i] == 0:
            embed = disnake.Embed(
                title=translation["tower"]["4"], color=disnake.Color.blue()
            )
            embed.set_image(url=TOWERURL)
            await user.update()
            await Interaction.channel.send(embed=embed)
            return
        reward_items = [
            {"id": i["id"]} for i in tower["rewards"][0 : tower["unlocks"][i]]
        ]
        probabilities = [i["p"] for i in tower["rewards"][0 : tower["unlocks"][i]]]
        sum_level = (i * (i + 1)) / 2
        probabilities_ndrop = [(7 - n) / sum_level for n in range(1, i + 1)]
        number_of_drops = random.choices(
            list(range(1, i + 1)), probabilities_ndrop, k=1
        )[0]
        items = random.choices(reward_items, probabilities, k=number_of_drops)

        items = [item_from_dict(get_item_from_template(item)) for item in items]
        title = "Tower"

        if i + 1 == tower["levels"] and winner.is_human:
            # the tower is completed
            title = translation["tower"]["5"]
            embed = disnake.Embed(title=title, color=disnake.Color.blue())
            embed.add_field(
                name=translation["tower"]["8"],
                value="    ▬▬▬▬▬▬▬▬▬\n",
                inline=False,
            )
            if user.tower_level <= tower_id:
                user.tower_level = tower_id + 1
                first_item = item_from_dict(tower["first_completion_reward"])
                embed.add_field(
                    name=translation["tower"]["7"],
                    value=f"{first_item.name}|{first_item.emoji}",
                    inline=False,
                )
                items.append(first_item)
        else:
            title = translation["tower"]["6"]
            embed = disnake.Embed(title=title, color=disnake.Color.blue())
            embed.add_field(
                name=translation["tower"]["8"],
                value="    ▬▬▬▬▬▬▬▬▬\n",
                inline=False,
            )

        for item in items:
            embed.add_field(name=f"{item.name}", value=f"{item.emoji}", inline=False)
            user.items.append(item)
        await user.update()
        embed.set_image(url=TOWERURL)
        await Interaction.channel.send(embed=embed)

    """
    @commands.slash_command(
        name="test", description="Enter towers to farm items and stands !"
    )
    @database_check()
    async def test(self, Interaction: disnake.ApplicationCommandInteraction):
        for i in range(1, 6):
            file = await tower_images["3"](Interaction.author, i)
            embed = disnake.Embed(color=disnake.Color.blue())
            embed.set_image(file=file)
            await Interaction.send(embed=embed)
    """


def setup(stfubot: StfuBot):
    stfubot.add_cog(Tower(stfubot))