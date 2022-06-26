import disnake
import json
from datetime import datetime, timedelta

from stfubot.models.bot.stfubot import StfuBot
from stfubot.models.gameobjects.stands import get_stand_from_template
from stfubot.models.gameobjects.items import item_from_dict

from stfubot.utils.functions import add_to_available_storage, stand_fields
from stfubot.utils.decorators import inner_permissions

from stfubot.globals.emojis import CustomEmoji

from disnake.ext import commands
from typing import List
from enum import Enum


class awards(int, Enum):
    donor = 1
    FirstEggChampion = 2
    SecondEggChampion = 3
    ThirdEggChampion = 4
    ModTeam = 5
    StfuTeam = 6


"""
# For future discord permissions system
DEVELOPERS_PERMS = {}
for devs in DEVELOPER:
    DEVELOPERS_PERMS[f"{devs}"] = True
GIVESTAND_PERMS = {}
for gv in GIVESTAND:
    DEVELOPERS_PERMS[f"{gv}"] = True
TESTERS_PERMS = {}
for test in TESTERS:
    DEVELOPERS_PERMS[f"{test}"] = True
"""


class admincommands(commands.Cog):
    """all admin commands
    Args:
        commands ([type]): [description]
    """

    def __init__(self, bot: StfuBot):
        self.stfubot = bot

    @inner_permissions()
    @commands.slash_command(
        name="admincommands",
        description="reserved to admins",
        guild_ids=[
            432561641306193921,
            717088658305450057,
            742654613282619473,
            908304253309841409,
        ],
    )
    async def admin(self, Interaction: disnake.ApplicationCommandInteraction):
        pass

    @admin.sub_command(
        name="givedonor", description="give donor status to someone for 1 month"
    )
    @commands.is_owner()
    async def giveDonor(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        someone: disnake.Member,
    ):
        time = datetime.now() + timedelta(weeks=4)
        user = await self.stfubot.database.get_user_info(someone.id)
        user.discord = someone
        user.donor_status = time
        await user.update()
        embed = disnake.Embed(title=f"Gave donor status to {someone.display_name} ")
        embed.set_image(
            url="https://vignette.wikia.nocookie.net/jjba/images/d/d2/JoJos-Bizarre-Adventure-Speedwagon.jpg/revision/latest/scale-to-width-down/340?cb=20140406083728&path-prefix=fr"
        )
        await Interaction.send(embed=embed)

    @admin.sub_command(name="give_stand", description="Give a stand to someone")
    @inner_permissions(type="give_stand")
    async def giveStand(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        standid: int,
        star: int,
    ):
        stand = self.stfubot.stand_file[standid - 1]
        stand = get_stand_from_template(stand)
        user = await self.stfubot.database.get_user_info(member.id)
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        msg = add_to_available_storage(user, stand)

        if msg:
            embed = disnake.Embed(
                title=translation["use"]["3"].format(msg),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=f"https://storage.stfurequiem.com/Image/{stand.id}.png")
            embed = stand_fields(stand, embed)
            await user.update()
            await Interaction.channel.send(embed=embed)
            return
        embed = disnake.Embed(title=translation["use"]["4"], color=disnake.Color.blue())
        embed.set_image(url=self.stfubot.avatar_url)
        await Interaction.channel.send(embed=embed)
        return

    @admin.sub_command(name="givearrow", description="Give arrows to someone")
    @inner_permissions(type="give_stand")
    async def giveArrow(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        ammount: int,
    ):
        user = await self.stfubot.database.get_user_info(member.id)
        user.discord = member
        translation = await self.stfubot.database.get_interaction_lang(Interaction)

        user.items = user.items + [item_from_dict({"id": 2})] * ammount
        await user.update()
        embed = disnake.Embed(
            title=f"added {ammount}{CustomEmoji.ARROW} to {user.discord.display_name}"
        )
        await Interaction.send(embed=embed)

    @admin.sub_command(name="givecoin", description="give coin to someone")
    @inner_permissions(type="give_stand")
    async def giveCoin(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        amount: int,
    ):
        user = await self.stfubot.database.get_user_info(member.id)
        user.discord = member
        user.coins += amount
        await user.update()
        embed = disnake.Embed(
            title=f"added {amount}{CustomEmoji.COIN} to {user.discord.display_name}"
        )
        await Interaction.send(embed=embed)

    @admin.sub_command(name="giveoh", description="give OH status to someone")
    @commands.is_owner()
    async def giveOH(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        someone: disnake.Member,
    ):
        user = await self.stfubot.database.get_user_info(someone.id)
        user.discord = someone
        user.over_heaven_supporter = True
        embed = disnake.Embed(
            title=f"Gave OVER HEAVEN donor status to {someone.display_name}  THANKS for everything"
        )
        embed.set_image(
            url="https://c.tenor.com/5sahUGLcwbkAAAAd/dio-heaven-ascension-jjba.gif"
        )
        await Interaction.send(embed=embed)


def setup(client: StfuBot):
    client.add_cog(admincommands(client))
