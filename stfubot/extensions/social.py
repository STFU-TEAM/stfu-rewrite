import disnake
import random
import asyncio
import datetime

from disnake.ext import commands


# utils
from stfubot.utils.decorators import database_check
from stfubot.utils.functions import is_url_image, wait_for, secondsToText

# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.globals.emojis import CustomEmoji
from stfubot.globals.variables import (
    DONOR_CR_WAIT_TIME,
    NORMAL_CR_WAIT_TIME,
    DONOR_ADV_WAIT_TIME,
    NORMAL_ADV_WAIT_TIME,
)

# ui
from stfubot.ui.social.lang_select import LangSelectDropdown


class social(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(name="profile", description="show the profile of a player")
    async def profile(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        user: disnake.User = None,
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
        embed.set_thumbnail(url=User.discord.display_avatar.url)
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

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(name="advert", description="display advert link")
    @database_check()
    async def advert(self, Interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Advert.",
            description="The easiest way to win more coins !, and to support our work !",
        )
        embed.set_image(
            url="https://i.pinimg.com/originals/a5/e8/2d/a5e82d700ff336637489b44f32d36095.gif"
        )
        embed.add_field(
            name="Link to the ads, consider disabling Adblock, for us at least..",
            value="https://stfurequiem.com/ads",
        )
        await Interaction.send(embed=embed)

    @commands.slash_command(name="cooldowns", description="Show a cooldown list")
    @database_check()
    async def cooldowns(self, Interaction: disnake.ApplicationCommandInteraction):
        user = await self.stfubot.database.get_user_info(Interaction.author.id)

        # get the times
        past_time_ad = user.last_adventure
        past_time_vote = user.last_vote
        past_time_cr = user.last_crusade
        past_time_adv = user.last_adv

        # get the current time
        now = datetime.datetime.now()

        # compute each wait time
        wait_time_vote = 12
        wait_time_cr = (
            DONOR_CR_WAIT_TIME + (not user.is_donator()) * NORMAL_CR_WAIT_TIME
        )
        wait_time_ad = (
            DONOR_ADV_WAIT_TIME + (not user.is_donator()) * NORMAL_ADV_WAIT_TIME
        )
        wait_time_adv = 6

        status_ad = "✅ ready"
        delta_ad = now - past_time_ad
        if delta_ad.total_seconds() / 3600 <= wait_time_ad:
            hours_ad = datetime.timedelta(hours=wait_time_ad)
            wait_for_ad = hours_ad - delta_ad
            status_ad = f"🕛 {secondsToText(wait_for_ad.total_seconds())} left"
        status_vote = "✅ ready"
        delta_vote = now - past_time_vote
        if delta_vote.total_seconds() / 3600 <= wait_time_vote:
            hours_vote = datetime.timedelta(hours=wait_time_vote)
            wait_for_vote = hours_vote.total_seconds() - delta_vote.total_seconds()
            status_vote = f"🕛 {secondsToText(wait_for_vote)} left"
        status_cr = "✅ ready"
        delta_cr = now - past_time_cr
        if delta_cr.total_seconds() / 3600 <= wait_time_cr:
            hours_cr = datetime.timedelta(hours=wait_time_cr)
            wait_for_cr = hours_cr - delta_cr
            status_cr = f"🕛 {secondsToText(wait_for_cr.total_seconds())} left"
        status_adv = "✅ ready"
        delta_adv = now - past_time_adv
        if delta_adv.total_seconds() / 3600 <= wait_time_adv:
            hours_adv = datetime.timedelta(hours=wait_time_adv)
            wait_for_adv = hours_adv - delta_adv
            status_adv = f"🕛 {secondsToText(wait_for_adv.total_seconds())} left"
        # create the embed
        embed = disnake.Embed(title="Your cooldowns:", color=disnake.Colour.blue())
        embed.set_thumbnail(
            url="https://cdn.iconscout.com/icon/free/png-256/clock-1605637-1360989.png"
        )
        if not user.is_donator():
            embed.add_field(
                name="Want lower cooldown ? consider donating",
                value="use donate command for more information",
            )
        embed.add_field(
            name=f"Adventure cooldown:",
            value=f"{status_ad}",
            inline=False,
        )
        embed.add_field(
            name=f"Vote cooldown",
            value=f"{status_vote}",
            inline=False,
        )
        embed.add_field(
            name=f"Crusade cooldown",
            value=f"{status_cr}",
            inline=False,
        )
        embed.add_field(
            name=f"Advert cooldown",
            value=f"{status_adv}",
            inline=False,
        )
        view = disnake.ui.View()
        if delta_adv.total_seconds() // 3600 > wait_time_adv:
            view.add_item(
                disnake.ui.Button(
                    label="Advert link",
                    style=disnake.ButtonStyle.url,
                    url="https://stfurequiem.com/ads",
                )
            )
        if delta_vote.total_seconds() // 3600 > wait_time_vote:
            view.add_item(
                disnake.ui.Button(
                    label="Vote link",
                    style=disnake.ButtonStyle.url,
                    url="https://stfurequiem.com/vote",
                )
            )
        if view.children != []:
            await Interaction.send(embed=embed, view=view)
            return
        await Interaction.send(embed=embed)

    @commands.slash_command(
        name="donate", description="show information about donation"
    )
    async def donate(self, Interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Donation",
            url="https://patreon.com/EIRBLAST",
            description="Donate to support the team and get cool loot !",
            color=disnake.Colour.blue(),
        )
        embed.set_footer(
            text="Donate only if you can, and if you really want to support us!"
        )
        embed.add_field(name="Link:", value="https://patreon.com/EIRBLAST", inline=True)
        await Interaction.send(embed=embed)


def setup(client: StfuBot):
    client.add_cog(social(client))