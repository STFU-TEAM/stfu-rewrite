import disnake
import asyncio
import traceback
import topgg
from datetime import datetime
from logging import warning

# utils
from stfubot.utils.functions import view_timeout

# stfu model
from stfubot.models.bot.stfubot import StfuBot


from disnake.ext import commands
from disnake.ext.commands import errors


class ErrorHandle(commands.Cog):
    """ Handle error for the bot """

    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.Cog.listener()
    async def on_command_error(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        error: commands.errors.CommandError,
    ) -> None:
        await self.handle_error(Interaction, error)

    @commands.Cog.listener()
    async def on_message_command_error(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        error: commands.errors.CommandError,
    ) -> None:
        await self.handle_error(Interaction, error)

    @commands.Cog.listener()
    async def on_user_command_error(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        error: commands.errors.CommandError,
    ) -> None:
        await self.handle_error(Interaction, error)

    @commands.Cog.listener()
    async def on_slash_command_error(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        error: commands.errors.CommandError,
    ) -> None:
        await self.handle_error(Interaction, error)

    async def handle_error(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        error: errors.CommandError,
    ):
        """
        this listen for error and handle them in this order

        Beforhand save data if any

        1-Know if the error need to be ignored.
        2-Else Notify the user that an error occurred
        3-Log the error
        4-Warn in the console
        """
        # ignore ctx commands
        if isinstance(Interaction, commands.Context):
            return
        # call update to prevent cache hickups
        if await self.stfubot.database.guild_in_database(
            Interaction.guild.id
        ) and await self.stfubot.database.user_in_database(Interaction.author.id):
            user = await self.stfubot.database.get_user_info(Interaction.author.id)
            await user.update()
        translation = await self.stfubot.database.get_interaction_lang(Interaction)

        # get the command where the error occurred
        command = Interaction.application_command
        # ignore these Exception
        ignore = [
            errors.CommandNotFound,
            errors.CheckFailure,
            errors.CommandNotFound,
            # RuntimeError,
        ]
        # if it's an invokeError we get what caused it
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original

        # check if the error should be ignored
        if any([isinstance(error, exception) for exception in ignore]):
            return  # avoid logging
        # case handlling

        # Timeout error with view :)
        if isinstance(
            error,
            (
                TimeoutError,
                asyncio.exceptions.TimeoutError,
            ),
        ):
            # add a little button that show a command expired
            await view_timeout(Interaction)
            return  # avoid logging
        # We mostly ignore command on CommandOnCooldown
        if isinstance(error, errors.CommandOnCooldown):
            embed = disnake.Embed(
                title=f"This command has a cooldown, try in {int(error.retry_after)}s"
            )
            await self.try_sending_message(Interaction, embed)
            return  # avoid logging
        # Missing Permission error from bot
        if isinstance(error, disnake.errors.Forbidden):
            embed = disnake.Embed(
                title=translation["error_messages"]["error"],
                description=translation["error_messages"]["not_enough_permission"],
                color=disnake.Color.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            embed.add_field(
                name=translation["errors"]["1"],
                value="https://stfurequiem.com/invite/",
            )
            embed.add_field(
                name=translation["errors"]["2"],
                value=translation["errors"]["3"],
            )
            embed.set_footer(text=translation["errors"]["4"])
            await self.try_sending_message(Interaction, embed)
            return  # avoid logging
        # Missing Permission error from user
        if isinstance(error, errors.MissingPermissions):
            embed = disnake.Embed(
                title=translation["error_messages"]["error"],
                description=translation["error_messages"]["no_permission"],
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            embed.set_footer(text=translation["errors"]["1"])
            await self.try_sending_message(Interaction, embed)
            return  # avoid logging
        # if someone doesn't give all the command argument
        if isinstance(error, errors.MissingRequiredArgument):
            embed = disnake.Embed(
                title=translation["error_messages"]["error"],
                description=translation["error_messages"]["missing_arguments"],
                color=disnake.Color.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            embed.set_footer(text=translation["errors"]["4"])
            await self.try_sending_message(Interaction, embed)
            return  # avoid logging
        # if the arrow command was user more than one time
        if isinstance(error, errors.MaxConcurrencyReached):
            embed = disnake.Embed(
                title=translation["error_messages"]["error"],
                description=translation["error_messages"]["max_concurrency"].format(
                    command.qualified_name
                ),
                color=disnake.Color.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            embed.set_footer(text=translation["errors"]["4"])
            await self.try_sending_message(Interaction, embed)
            return  # avoid logging
        # if the top.gg server are dead.
        if isinstance(error, (topgg.errors.ServerError, topgg.errors.HTTPException)):
            embed = disnake.Embed(
                title=translation["error_messages"]["error"],
                description=translation["error_messages"]["TOPGG"],
                color=disnake.Color.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            embed.set_footer(text=translation["errors"]["4"])
            await self.try_sending_message(Interaction, embed)
        # bad embed form
        if isinstance(error, disnake.errors.HTTPException):
            embed = disnake.Embed(
                title=translation["error_messages"]["error"],
                description=translation["error_messages"]["http_error"],
                color=disnake.Color.red(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            embed.set_footer(text=translation["errors"]["4"])
            await self.try_sending_message(Interaction, embed)
        # log the error and warn
        warning(f'In the "{command}" command got the Exception: {str(type(error))}')
        await self.logger(command, error)

    # try sending a message without an error
    async def try_sending_message(
        self, Interaction: disnake.ApplicationCommandInteraction, embed: disnake.Embed
    ) -> None:
        try:
            await Interaction.response.send_message(embed=embed)
        except Exception as e:
            if isinstance(e, disnake.errors.InteractionResponded):
                try:
                    await Interaction.followup.send(embed=embed)
                except:
                    await Interaction.send(embed=embed)
                return
            await Interaction.send(embed=embed)

    # log a given error
    async def logger(
        self,
        Interaction_command: commands.InvokableApplicationCommand,
        error: Exception,
    ) -> None:
        try:
            # from stack overflow : https://stackoverflow.com/questions/4564559/get-exception-description-and-stack-trace-which-caused-an-exception-all-as-a-st
            error_traceback = "".join(
                traceback.format_exception(
                    etype=type(error), value=error, tb=error.__traceback__
                )
            )
            # log the error
            await self.stfubot.database.add_log(
                datetime.now(),
                str(Interaction_command.qualified_name),
                str(type(error)),
                error_traceback,
            )
        except:
            warning(f"failed Logging! is the database compromised ?")


def setup(client):
    client.add_cog(ErrorHandle(client))
