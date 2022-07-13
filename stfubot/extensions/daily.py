from cmath import tan
import disnake
import random
import datetime

from typing import List

# utils
from stfubot.utils.decorators import database_check
from stfubot.utils.functions import secondsToText

# stfu model
from stfubot.globals.emojis import CustomEmoji
from stfubot.globals.variables import DONOR_ADV_WAIT_TIME, NORMAL_ADV_WAIT_TIME
from stfubot.models.bot.stfubot import StfuBot
from stfubot.models.gameobjects.stands import get_stand_from_template
from stfubot.models.gameobjects.items import Item, item_from_dict

# specific class import
from disnake.ext import commands


class daily(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(name="begin", description="Start your daily journey")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def begin(self, Interaction: disnake.ApplicationCommandInteraction):
        # get the translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        # Check if user is registered
        if not (await self.stfubot.database.user_in_database(Interaction.author.id)):
            await self.stfubot.database.add_user(Interaction.author.id)
            User = await self.stfubot.database.get_user_info(Interaction.author.id)
            # get a 4 star as a starting stand
            starting_stands = [s for s in self.stfubot.stand_file if s["stars"] == 4]
            stand = get_stand_from_template(random.choice(starting_stands))
            # add the stand and update
            embed = disnake.Embed(
                title=translation["begin"]["1"],
                description=translation["begin"]["2"],
                color=disnake.Colour.blue(),
            )
            embed.set_image(url=f"http://storage.stfurequiem.com/Image/{stand.id}.png")
            embed.add_field(
                name="▬▬▬`STAND`▬▬▬",
                value=f"name:`{stand.name}`\n" + "stars:`⭐⭐⭐⭐`\n" + "    ▬▬▬▬▬▬▬▬▬",
            )
            embed.add_field(
                name="▬▬▬`STATS`▬▬▬",
                value=f"HP:`{stand.current_hp}❤️`\n"
                + f"DAMAGE:`{stand.current_damage}⚔️`\n"
                + f"SPEED:`{stand.current_speed}💨`\n    ▬▬▬▬▬▬▬▬▬",
            )
            turn = (
                "\n"
                if stand.special_description == "None"
                else f"\nturn:`{stand.turn_for_ability}\n`"
            )
            embed.add_field(
                name="▬▬`SPECIAL`▬▬",
                value=stand.special_description + turn + "    ▬▬▬▬▬▬▬▬▬",
            )
            embed.add_field(
                name="▬▬`Quick Start`▬▬",
                value=translation["begin"]["3"]
                + translation["begin"]["4"]
                + translation["begin"]["5"]
                + translation["begin"]["6"]
                + translation["begin"]["7"]
                + "    ▬▬▬▬▬▬▬▬▬",
            )
            User.stands.append(stand)
            # Give to arrows
            User.items.append(item_from_dict({"id": 2}))
            User.items.append(item_from_dict({"id": 2}))
            User.coins += 1
            await User.update()
            await Interaction.send(embed=embed)
        else:
            embed = disnake.Embed(title="Oops !")
            embed.add_field(
                name="▬▬▬START▬▬▬",
                value=translation["error_meesages"]["already_registered"]
                + "\n"
                + "    ▬▬▬▬▬▬▬▬▬",
            )
            await Interaction.send(embed=embed)

    @commands.slash_command(name="daily", description="daily adventure")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @database_check()
    async def daily(self, Interaction: disnake.ApplicationCommandInteraction):
        pass

    @daily.sub_command(
        name="adventure",
        description="your stands go on an adventure and get various items",
    )
    async def adventure(self, Interaction: disnake.ApplicationCommandInteraction):
        # translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        # Check the time
        past_time = user.last_adventure
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        delta = now - past_time
        wait_time = DONOR_ADV_WAIT_TIME + (not user.is_donator()) * NORMAL_ADV_WAIT_TIME

        if delta.total_seconds() // 3600 < wait_time:
            wait_for = (
                datetime.timedelta(hours=wait_time) - delta
                if datetime.timedelta(hours=wait_time) > delta
                else delta - datetime.timedelta(hours=wait_time)
            )
            embed = disnake.Embed(
                title=translation["error_meesages"]["sorry_but"],
                description=translation["error_meesages"]["cool_down"].format(
                    "adventure", secondsToText(wait_for.total_seconds())
                ),
                color=disnake.Color.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        user.last_adventure = now
        roll = random.randint(1, 100)
        embed = disnake.Embed(
            title=translation["adventure"]["1"],
            color=disnake.Colour.blue(),
        )
        if roll <= 10:
            items: List[Item] = [
                item_from_dict({"id": 2}),
                item_from_dict({"id": 1}),
                item_from_dict({"id": 4}),
            ]
            item = random.choice(items)
            user.items.append(item)
            embed.add_field(
                name=translation["adventure"]["2"],
                value=f"`{item.name}`|{item.emoji}",
                inline=True,
            )
        coins = random.randint(90, 120)
        user.coins += coins
        embed.add_field(
            name=translation["adventure"]["3"],
            value=f"`{coins}`{CustomEmoji.COIN}",
            inline=True,
        )
        embed.set_image(
            url="https://i.pinimg.com/originals/a5/e8/2d/a5e82d700ff336637489b44f32d36095.gif"
        )
        await user.update()
        await Interaction.send(embed=embed)


def setup(client: StfuBot):
    client.add_cog(daily(client))