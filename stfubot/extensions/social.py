import disnake
import random
import asyncio

from disnake.ext import commands

# utils
from stfubot.utils.decorators import database_check
from stfubot.utils.functions import is_url_image, wait_for

# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.globals.emojis import CustomEmoji

# ui
from stfubot.ui.social.lang_select import LangSelectDropdown


class social(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(name="profile", description="show the profile of a player")
    async def profile(
        self, Interaction: disnake.ApplicationCommandInteraction, user=None
    ):
        # Checks
        if user == None:
            user = Interaction.author
        # get the translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        if not (await self.stfubot.database.user_in_database(user.id)):
            embed = disnake.Embed(
                title=translation["error_meesages"]["not_registered"].format(user.name),
                colour=disnake.Colour.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        User = await self.stfubot.database.get_user_info(user.id)
        User.discord = user
        embed = disnake.Embed(
            title=f"`Profile`",
            description=translation["profile"]["1"].format(User.discord.mention),
            colour=disnake.Colour.blue(),
        )
        embed.add_field(
            name=translation["profile"]["2"],
            value=f"\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            inline=False,
        )
        embed.add_field(name=translation["profile"]["3"], value=f"`{User.level}`|✨")
        embed.add_field(name="`XP`", value=f"`{User.xp}`|⬆️")
        embed.add_field(
            name=translation["profile"]["4"],
            value=f"`{User.coins}`|{CustomEmoji.COIN}\n",
        )
        embed.add_field(name=translation["profile"]["5"], value=f"`{0}`|🏅")
        embed.add_field(
            name=translation["profile"]["6"], value=f"`{User.global_elo}`|🏆"
        )
        embed.add_field(name="`Gang`:", value=f"`None`|👨‍👩‍👧‍👧")
        embed.add_field(
            name="`Stands`",
            value=f"\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            inline=False,
        )
        for stand in User.stands:
            stars = "⭐" * stand.stars + "🌟" * stand.ascension
            embed.add_field(
                name=f"`｢{stand.name}｣`|`{stars}`",
                value=f"{translation['profile']['3']}`{stand.level}`",
                inline=True,
            )
        embed.set_image(url=User.profile_image)
        embed.set_thumbnail(url=User.discord.avatar.url)
        await Interaction.send(embed=embed)

    @database_check()
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @commands.slash_command(
        name="changeprofileimage", description="Change your profile image"
    )
    async def changeprofileimage(
        self, Interaction: disnake.ApplicationCommandInteraction, url: str
    ):
        if is_url_image(url) == False:
            embed = disnake.Embed(
                title="URL Error",
                description="Please add a valid URL",
                color=disnake.Colour.red(),
            )
            await Interaction.send(embed=embed)
            return
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user.profile_image = url
        await user.update()
        embed = disnake.Embed(title=translation["changeprofileimage"]["1"])
        embed.set_image(url=url)
        await Interaction.send(embed=embed)

    @commands.slash_command(name="changedefaultlang", description="change the bot lang")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @commands.has_permissions(administrator=True)
    @database_check()
    async def changedefaultlang(
        self, Interaction: disnake.ApplicationCommandInteraction
    ):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        embed = disnake.Embed(
            title=translation["changedefaultlang"]["1"], color=disnake.Color.blue()
        )
        embed.set_image(url=self.stfubot.avatar_url)
        view = LangSelectDropdown(Interaction)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)

        lang_dict = view.value

        guild = await self.stfubot.database.get_guild_info(Interaction.guild.id)

        guild.lang = lang_dict["path"]
        await guild.update()


def setup(client: StfuBot):
    client.add_cog(social(client))