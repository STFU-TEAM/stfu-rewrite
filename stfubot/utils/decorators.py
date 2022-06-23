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
        await Interaction.response.defer()
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
        await Interaction.response.defer()
        user = await database.get_user_info(Interaction.author.id)
        translation = await database.get_interaction_lang(Interaction)
        await database.close()
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
        await Interaction.response.defer()
        user = await database.get_user_info(Interaction.author.id)
        translation = await database.get_interaction_lang(Interaction)
        await database.close()
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
        await Interaction.response.defer()
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
            await database.close()
            return False

        gang = await database.get_gang_info(user.gang_id)
        await database.close()
        rank = gang.ranks[user.id]
        return rank <= minimum_rank

    return commands.check(check)