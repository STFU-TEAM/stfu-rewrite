import disnake
import asyncio

from typing import List, Union
from discord.ext import commands
from stfubot.models.database.maindatabase import Database
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
        if not await database.server_InDatabase(Interaction.guild.id):
            embed = disnake.Embed(
                title="An error has occurred",
                description="It seems you are not in the database, consider using /begin first !",
                color=0xFF0000,
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
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