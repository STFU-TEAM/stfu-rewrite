import disnake
import random
import asyncio

# utils
from stfubot.utils.decorators import database_check
from stfubot.utils.functions import (
    play_files,
    sign,
    wait_for,
    add_to_available_storage,
)


# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.models.gameobjects.stands import Stand

# specific class import
from disnake.ext import commands

# ui
from ui.place_holder import PlaceHolder
from ui.confirmation import Confirm
from ui.StandSelect import StandSelectDropdown
from ui.storage.ChooseDonor import ChooseStorage


class management(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(name="stand", description="stand management")
    @database_check()
    async def stand(self, Interaction: disnake.ApplicationCommandInteraction):
        pass

    @stand.sub_command(name="show", description="show one of your main stand stats.")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def show(self, Interaction: disnake.ApplicationCommandInteraction):
        User = await self.stfubot.database.get_user_info(Interaction.author.id)
        if User.stands == []:
            embed = disnake.Embed(
                title="Error",
                description="You don't have any stand in your main stand.",
                color=disnake.Colour.blue(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
        else:
            # make an embed
            embed = disnake.Embed(
                title="Which stand would you like to select ?",
                color=disnake.Colour.blue(),
            )
            embed.set_image(url="https://storage.stfurequiem.com/Image/arrow.gif")

            view = StandSelectDropdown(Interaction, User.stands)
            await Interaction.send(embed=embed, view=view)
            await wait_for(view)
            index = view.value
            # get the stand

            stand: Stand = User.stands[index]
            items = stand.items
            stars = "⭐" * stand.stars + "🌟" * stand.ascension
            # shinies
            if stand.ascension + stand.stars > 7 and stand.id != 110:
                stars = "🌟" * stand.stars + "🌠" * stand.ascension
                # per case embed and name
                if stand.id == 109:
                    stand.name = "ボームヴンレクイエム"
                    rand = 1
                elif stand.id == 84:
                    stand.name = "Alternate Universe Gold Experience Requiem"
                    rand = 5
                elif stand.id == 54:
                    stand.name = "Super Duper Cute and Angy Stray Cat"
                    rand = 2
                elif stand.id == 86:
                    stand.name = "受け継がれた魂 Stone Free"
                    rand = 1
                rand = random.randint(1, rand)
                url = f"https://storage.stfurequiem.com/Shiny/{stand.id}_{rand}.gif"
                play = f"data/sound/{stand.id}_1.mp3"
            # evolved 4 star
            elif stand.ascension > 1 and stand.stars == 4 and stand.id <= 85:
                url = f"https://storage.stfurequiem.com/Image/{stand.id}.gif"
                play = ""
            # 5+ star
            elif stand.stars >= 5:
                url = f"https://storage.stfurequiem.com/Image/{stand.id}.gif"
                play = f"data/sound/{stand.id}.mp3"
            else:
                url = f"https://storage.stfurequiem.com/Image/{stand.id}.png"
                play = ""
            embed = disnake.Embed(
                title=f"`{stand.name}`",
                description=f"`{stars}`",
                color=disnake.Colour.blue(),
            )
            bonus_hp = stand.current_hp - stand.base_hp
            bonus_damage = stand.current_damage - stand.base_damage
            bonus_speed = stand.current_speed - stand.base_speed
            bonus_critical = stand.current_critical - stand.base_critical
            embed.set_image(url=url)
            embed.add_field(
                name="▬▬▬`STATS`▬▬▬",
                value=f"HP:`{int(stand.base_hp)}{sign(bonus_hp)}❤️`\n"
                + f"DAMAGE:`{int(stand.base_damage)}{sign(bonus_damage)}⚔️`\n"
                + f"SPEED:`{int(stand.base_speed)}{sign(bonus_speed)}💨`\n"
                + f"CRITICAL RATE:`{int(stand.base_critical)}{sign(bonus_critical)}✨`\n"
                + f"LEVEL:`{stand.level}`\n"
                + f"XP:`{stand.xp}`\n    ▬▬▬▬▬▬▬▬▬",
            )
            if len(items) != 0:
                item = ""
                for i in items:
                    item += f"{i.emoji}:{i.name}\n"
                item += "    ▬▬▬▬▬▬▬▬▬\n"
                embed.add_field(name="▬▬▬`ITEMS`▬▬▬", value=item)
            turn = (
                "\n"
                if stand.special_description == "None"
                else f"\nturn:`{stand.turn_for_ability}`"
            )
            embed.add_field(
                name="▬▬`SPECIAL`▬▬",
                value=stand.special_description + turn + "\n    ▬▬▬▬▬▬▬▬▬",
            )

            await Interaction.channel.send(embed=embed)
            if play:
                await play_files(Interaction, [play])

    @stand.sub_command(name="remove", description="Remove a stand from your storage")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def remove(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        storage = user.stand_storage
        premium = False
        if user.is_donator():
            embed = disnake.Embed(
                title=translation["ui"]["1"], color=disnake.Color.blue()
            )
            view = ChooseStorage(Interaction)
            await Interaction.send(embed=embed, view=view)
            await wait_for(view)
            Interaction = view.interaction
            premium = True
            if not view.value:
                storage = user.pstand_storage

        if storage == []:
            embed = disnake.Embed(
                title=translation["error_meesages"]["empty_storages"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        embed = disnake.Embed(
            title=translation["remove"]["1"], color=disnake.Color.blue()
        )
        for stand in storage:
            etoile = stand.stars * "⭐" + "🌟" * stand.ascension
            embed.add_field(
                name=f"`『{stand.name}』`level:{stand.level}\n",
                value=f"`{etoile}`\n    ▬▬▬▬▬▬▬▬▬",
                inline=True,
            )
        view = StandSelectDropdown(Interaction, storage)
        if Interaction.response.is_done():
            await Interaction.send(embed=embed, view=view)
        else:
            await Interaction.channel.send(embed=embed, view=view)
        await wait_for(view)
        stand = storage.pop(view.value)
        embed = disnake.Embed(
            title=translation["remove"]["2"].format(stand.name),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=f"https://storage.stfurequiem.com/Image/{stand.id}.png")
        view = Confirm(Interaction)
        await Interaction.channel.send(embed=embed, view=view)
        await wait_for(view)
        Interaction = view.interaction
        if view.value:
            embed = disnake.Embed(
                title=translation["remove"]["3"].format(stand.name),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=f"https://storage.stfurequiem.com/Image/{stand.id}.png")
            if premium:
                user.pstand_storage = storage
            else:
                user.stand_storage = storage
            await user.update()
            await Interaction.response.edit_message(embed=embed, view=PlaceHolder())
            return
        embed = disnake.Embed(
            title=translation["remove"]["4"].format(stand.name),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=f"https://storage.stfurequiem.com/Image/{stand.id}.png")
        await Interaction.response.edit_message(embed=embed, view=PlaceHolder())

    @stand.sub_command(name="storage", description="show your storage")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def storage(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        storage = user.stand_storage
        if user.is_donator():
            embed = disnake.Embed(
                title=translation["ui"]["1"], color=disnake.Color.blue()
            )
            view = ChooseStorage(Interaction)
            await Interaction.send(embed=embed, view=view)
            await wait_for(view)
            Interaction = view.interaction
            if not view.value:
                storage = user.pstand_storage

        if storage == []:
            embed = disnake.Embed(
                title=translation["error_meesages"]["empty_storages"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        embed = disnake.Embed(
            title=translation["storage"]["1"].format(user.discord.name),
            color=disnake.Color.blue(),
        )
        for stand in storage:
            etoile = stand.stars * "⭐" + "🌟" * stand.ascension
            embed.add_field(
                name=f"`『{stand.name}』`level:{stand.level}\n",
                value=f"`{etoile}`\n    ▬▬▬▬▬▬▬▬▬",
                inline=True,
            )
        if Interaction.response.is_done():
            await Interaction.send(embed=embed)
        else:
            await Interaction.channel.send(embed=embed)

    @stand.sub_command(
        name="main", description="move a stand from storage to your main stands"
    )
    async def mainstand(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        storage = user.stand_storage
        premium = False
        if user.is_donator():
            embed = disnake.Embed(
                title=translation["ui"]["1"], color=disnake.Color.blue()
            )
            view = ChooseStorage(Interaction)
            await Interaction.send(embed=embed, view=view)
            await wait_for(view)
            Interaction = view.interaction
            if not view.value:
                premium = True
                storage = user.pstand_storage

        if storage == []:
            embed = disnake.Embed(
                title=translation["error_meesages"]["empty_storages"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        embed = disnake.Embed(
            title=translation["mainstand"]["1"], color=disnake.Color.blue()
        )
        for stand in storage:
            etoile = stand.stars * "⭐" + "🌟" * stand.ascension
            embed.add_field(
                name=f"`『{stand.name}』`level:{stand.level}\n",
                value=f"`{etoile}`\n    ▬▬▬▬▬▬▬▬▬",
                inline=True,
            )
        view = StandSelectDropdown(Interaction, storage)
        if Interaction.response.is_done():
            await Interaction.send(embed=embed, view=view)
        else:
            await Interaction.channel.send(embed=embed, view=view)
        await wait_for(view)
        stand = storage.pop(view.value)
        embed = disnake.Embed(
            title=translation["mainstand"]["2"].format(stand.name),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=f"https://storage.stfurequiem.com/Image/{stand.id}.png")
        view = Confirm(Interaction)
        await Interaction.channel.send(embed=embed, view=view)
        await wait_for(view)
        Interaction = view.interaction
        if not view.value:
            embed = disnake.Embed(
                title=translation["mainstand"]["3"].format(stand.name),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=f"https://storage.stfurequiem.com/Image/{stand.id}.png")
            await Interaction.response.edit_message(embed=embed, view=PlaceHolder())
            return
        if len(user.stands) < 3:
            embed = disnake.Embed(
                title=translation["mainstand"]["4"].format(stand.name),
                color=disnake.Color.blue(),
            )
            if premium:
                user.pstand_storage = storage
            else:
                user.stand_storage = storage
            user.stands.append(stand)
            await user.update()
            await Interaction.response.edit_message(embed=embed, view=PlaceHolder())
            return
        view = StandSelectDropdown(Interaction, user.stands)
        embed = disnake.Embed(
            title=translation["mainstand"]["5"], color=disnake.Color.blue()
        )
        await Interaction.response.edit_message(embed=embed, view=view)
        await wait_for(view)
        stand2 = user.stands.pop(view.value)
        storage.append(stand2)
        if premium:
            user.pstand_storage = storage
        else:
            user.stand_storage = storage
        user.stands.append(stand)
        embed = disnake.Embed(
            title=translation["mainstand"]["6"].format(stand.name, stand2.name),
            color=disnake.Color.blue(),
        )
        await user.update()
        await Interaction.channel.send(embed=embed)

    @stand.sub_command(name="store", description="store a main stand into storage")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def store(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        embed = disnake.Embed(
            title=translation["store"]["1"], color=disnake.Color.blue()
        )
        for stand in user.stands:
            etoile = stand.stars * "⭐" + "🌟" * stand.ascension
            embed.add_field(
                name=f"`『{stand.name}』`level:{stand.level}\n",
                value=f"`{etoile}`\n    ▬▬▬▬▬▬▬▬▬",
                inline=True,
            )
        view = StandSelectDropdown(Interaction, user.stands)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        stand = user.stands.pop(view.value)
        msg = add_to_available_storage(user, stand, skip_main=True)
        if msg:
            embed = disnake.Embed(
                title=translation["use"]["3"].format(msg),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=f"https://storage.stfurequiem.com/Image/{stand.id}.png")
            await user.update()
            await Interaction.channel.send(embed=embed)
            return
        embed = disnake.Embed(title=translation["use"]["4"], color=disnake.Color.blue())
        embed.set_image(url=f"https://storage.stfurequiem.com/Image/{stand.id}.png")
        await Interaction.channel.send(embed=embed)

    @stand.sub_command(
        name="ascend", description="ascend a main stand to a higher plain of existence"
    )
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def ascend(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        embed = disnake.Embed(
            title=translation["ascend"]["1"], color=disnake.Color.blue()
        )
        view = StandSelectDropdown(Interaction, user.stands)

        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        stand: Stand = user.stands[view.value]
        if stand.level == 100 and (stand.stars + stand.ascension) < 7:
            embed = disnake.Embed(
                title=translation["ascend"]["2"].format(
                    stand.name, stand.ascension + 1
                ),
                color=disnake.Color.blue(),
            )
            embed.set_image(url="https://storage.stfurequiem.com/item_special/6.gif")
            stand.ascension += 1
            stand.xp = 0
            await user.update()
            await Interaction.channel.send(embed=embed)
            return
        embed = disnake.Embed(
            title=translation["ascend"]["3"], color=disnake.Color.blue()
        )
        await Interaction.channel.send(embed=embed)


def setup(client: StfuBot):
    client.add_cog(management(client))