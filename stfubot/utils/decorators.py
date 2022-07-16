import disnake
import asyncio

from typing import List, Union
from discord.ext import commands

from stfubot.models.database.maindatabase import Database
from stfubot.models.gameobjects.gang import GangRank
from stfubot.globals.variables import LOOP


def database_check():
    """check for the existence of data about the context author
        display an error message otherwise

        if this decorator is above a command database.get_userInfo can be
        used without fear of returning None
    Args:
        slash_command:wether it's a slash command check or not

    Returns:
        [type]: [return a check decorator]
    """
    database = Database(LOOP)

    async def check(Interaction: disnake.ApplicationCommandInteraction) -> bool:
        """
            inner check
        Args:
            ctx (commands.Context): disnake Context

        Returns:
            bool: the anwser
        """
        """
        if await database.isBanned(Interaction.author.id):
            embed = disnake.Embed(
                title="It seems like you've been permanently banned from the bot.",
                description="Contact us via our website if you would like to get more infos.",
                color=0xFF0000,
            )
            await Interaction.send(embed=embed)
            return False
        """
        await Interaction.response.defer()
        if not await database.user_in_database(Interaction.author.id):
            translation = await database.get_interaction_lang(Interaction)
            embed = disnake.Embed(
                title=translation["error_meesages"]["error"],
                description=translation["error_meesages"]["not_registered"],
                color=disnake.Color.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
            return False
        return True

    return commands.check(check)


def shop_check():
    database = Database(LOOP)

    async def check(Interaction: disnake.ApplicationCommandInteraction) -> bool:
        user = await database.get_user_info(Interaction.author.id)
        translation = await database.get_interaction_lang(Interaction)
        # Shop does no exists
        if user.shop_id == None:
            embed = disnake.Embed(
                title=translation["error_meesages"]["shop_not_created"],
                color=disnake.Color.red(),
            )
            embed.set_image(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
            return False
        return True

    return commands.check(check)


def gang_check():
    database = Database(LOOP)

    async def check(Interaction: disnake.ApplicationCommandInteraction) -> bool:
        user = await database.get_user_info(Interaction.author.id)
        translation = await database.get_interaction_lang(Interaction)
        # gang does no exists
        if user.gang_id == None:
            embed = disnake.Embed(
                title=translation["error_meesages"]["gang_not_created"],
                color=disnake.Color.red(),
            )
            embed.set_image(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
            return False
        return True

    return commands.check(check)


def gang_rank_check(minimum_rank: GangRank = GangRank.SOLDIER):
    """Checks whether the user as a sufficient rank in their gang to use the command
    can be used to replace `gang_check`

    Args:
        minimum_rank (GangRank, optional): rank to use the command Defaults to GangRank.SOLDIER.
    """
    database = Database(LOOP)

    async def check(Interaction: disnake.ApplicationCommandInteraction) -> bool:
        user = await database.get_user_info(Interaction.author.id)
        translation = await database.get_interaction_lang(Interaction)

        # gang does no exists
        if user.gang_id == None:
            embed = disnake.Embed(
                title=translation["error_meesages"]["gang_not_created"],
                color=disnake.Color.red(),
            )
            embed.set_image(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)

            return False

        gang = await database.get_gang_info(user.gang_id)
        rank = gang.ranks[user.id]
        return rank <= minimum_rank

    return commands.check(check)


def inner_permissions(type: str = "give_stand"):
    """Allow to check if a user is allowed to use a command based on our own perssion levels
    Args:
        type (str, optional): can be `developer`, `give_stand` or `tester`. Defaults to `tester`.

    Returns:
        [type]: [description]
    """
    developers = [
        242367586233352193,  # EIRBLAST
        112866272106012672,  # Arkkos
        289413979644755970,  # Kelian
    ]
    testers = developers + [
        248492672979959809,  # EIRBOT
        435082104381112340,  # Allways
    ]
    give_stand = developers + [
        704961055662538833,  # Keyshiwo
        348342650853785602,  # Greg
        476057912532533273,  # Pickle
        435082104381112340,  # Allways
    ]

    async def check(Interaction: disnake.ApplicationCommandInteraction) -> bool:
        if type == "developer" and not Interaction.author.id in developers:
            embed = disnake.Embed(
                title="An error has occurred",
                description="This command is developer only",
                color=disnake.Colour.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
            return False
        if type == "tester" and not Interaction.author.id in testers:
            embed = disnake.Embed(
                title="An error has occurred",
                description="This command is testers only",
                color=disnake.Colour.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
            return False
        if type == "give_stand" and not Interaction.author.id in give_stand:
            embed = disnake.Embed(
                title="An error has occurred",
                description="This command is at least moderator only",
                color=disnake.Colour.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
            return False
        return True

    return commands.check(check)