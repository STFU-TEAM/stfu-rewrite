import disnake
import asyncio


from disnake.ext import commands


# ui
from stfubot.ui.confirmation import Confirm
from stfubot.ui.paginator import Menu

# utils
from stfubot.utils.functions import format_combat_log
from stfubot.utils.fight_logic import fight_instance
from stfubot.utils.image_generators import get_fight_image, get_win_image

# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.globals.variables import PLAYER_XPGAINS, STAND_XPGAINS


class fight(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(name="fight", description="fight someone in your server")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def fight(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        ennemy: disnake.Member,
    ):
        await Interaction.response.defer()
        # get the translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        # Check if both user are already registered
        if not await self.stfubot.database.user_in_database(Interaction.author.id):
            embed = disnake.Embed(
                title=translation["error_meesages"]["not_registered"].format(
                    Interaction.author.name
                ),
                colour=disnake.Colour.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        if not await self.stfubot.database.user_in_database(ennemy.id):
            embed = disnake.Embed(
                title=translation["error_meesages"]["not_registered"].format(
                    ennemy.name
                ),
                colour=disnake.Colour.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        if ennemy.id == Interaction.author.id:
            embed = disnake.Embed(
                title="Don't fight yourself, get therapy",
                color=disnake.Colour.blue(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return

        # Get the users
        user_1 = await self.stfubot.database.get_user_info(ennemy.id)
        user_2 = await self.stfubot.database.get_user_info(Interaction.author.id)
        user_1.discord = ennemy
        user_2.discord = Interaction.author
        image = await get_fight_image(user_1.discord, user_2.discord)
        embed = disnake.Embed(
            title=translation["fight"]["1"].format(
                user_1.discord.name, user_2.discord.name
            ),
            colour=disnake.Colour.blue(),
        )
        embed.set_image(file=image)
        view = Confirm(Interaction, user=ennemy)
        await Interaction.send(embed=embed, view=view)
        if await view.wait():
            raise asyncio.TimeoutError
        await Interaction.delete_original_message()
        if not view.value:
            embed = disnake.Embed(
                title=translation["fight"]["2"].format(user_1.discord.name),
                colour=disnake.Colour.blue(),
            )
            await Interaction.channel.send(embed=embed)
            return
        # Everyone should have at least one stand in their main soooo.
        channels = [Interaction.channel] * 2
        players = [user_1, user_2]
        winner, combat_log = await fight_instance(
            players, channels, translation, ranked=False
        )
        # This is nessesary because we actually affect the stand "itself"
        # This will obviously never cause any problem in the future 🙃
        for stand in players[0].stands + players[1].stands:
            stand.reset()

        # combat log formating
        embeds = format_combat_log(translation, combat_log)
        final_view = Menu(embeds)

        # Reward the winner
        winner.xp += PLAYER_XPGAINS // 2  # Divided by 2 because local fight
        for stand in winner.stands:
            stand.xp += STAND_XPGAINS // 2  # same as above
        winner.coins += 0  # Prevent local abuse
        players.remove(winner)
        # "Reward" the looser
        looser = players[0]
        looser.xp += PLAYER_XPGAINS // 2  # Divided by 2 because local fight
        for stand in looser.stands:
            stand.xp += STAND_XPGAINS // 2  # same as above
        looser.coins += 0  # Prevent local abuse
        # Embeds and stuff
        final_embed = disnake.Embed(
            title=translation["fight"]["10"].format(winner.discord.name),
            color=disnake.Color.blue(),
        )
        image = await get_win_image(winner.discord)
        final_embed.set_image(file=image)
        # Update
        await winner.update()
        await looser.update()
        # Final Send

        await Interaction.channel.send(embed=final_embed)
        await Interaction.channel.send(embed=embeds[0], view=final_view)


def setup(client: StfuBot):
    client.add_cog(fight(client))