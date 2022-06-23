import disnake
import json
import random
import asyncio

from disnake.ext import commands
from typing import List

# ui
from stfubot.ui.StandSelect import StandSelectDropdown
from stfubot.ui.item_select import ItemSelectDropdown

# utils
from stfubot.utils.decorators import database_check
from stfubot.utils.functions import (
    wait_for,
    get_drop_from_list,
    stand_fields,
    add_to_available_storage,
)

# stfu model
from stfubot.models.gameobjects.items import Item
from stfubot.models.bot.stfubot import StfuBot
from stfubot.models.gameobjects.stands import Stand, get_stand_from_template


class Items(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(name="item", description="manage item")
    @database_check()
    async def item(self, Interaction: disnake.ApplicationCommandInteraction):
        pass

    @item.sub_command(
        name="inventory", description="show all your items in your inventory"
    )
    async def inventory(self, Interaction: disnake.ApplicationCommandInteraction):
        # translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        unique: List[Item] = []
        for item in user.items:
            if not item.id in [i.id for i in unique]:
                unique.append(item)

        embed = disnake.Embed(
            title=translation["inventory"]["1"].format(user.discord.name),
            color=disnake.Color.blue(),
        )
        for item in unique:
            num = f" x{[i.id for i in user.items].count(item.id)}"
            embed.add_field(name=item.name + num, value=item.emoji, inline=False)
        await Interaction.send(embed=embed)

    @item.sub_command(name="equip", description="equip an item on a stand")
    async def equip(self, Interaction: disnake.ApplicationCommandInteraction):
        # translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        if len(user.items) == 0:
            embed = disnake.Embed(
                title=translation["equip"]["1"], color=disnake.Color.blue()
            )
            await Interaction.send(embed=embed)

        embed = disnake.Embed(
            title=translation["equip"]["2"], color=disnake.Color.blue()
        )
        view = StandSelectDropdown(Interaction, user.stands)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        stand_index = view.value
        stand: Stand = user.stands[view.value]

        if len(stand.items) == 3:
            embed = disnake.Embed(
                title=translation["equip"]["3"], color=disnake.Color.blue()
            )
            await Interaction.channel.send(embed=embed)
            return

        embed = disnake.Embed(
            title=translation["equip"]["4"], color=disnake.Color.blue()
        )
        equipable = [i for i in user.items if i.is_equipable]
        view = ItemSelectDropdown(Interaction, equipable)
        await Interaction.channel.send(embed=embed, view=view)
        await wait_for(view)
        item = equipable.pop(view.value)
        user.items.remove(item)
        user.stands[stand_index].items.append(item)

        embed = disnake.Embed(
            title=translation["equip"]["5"].format(item.name, stand.name),
            color=disnake.Color.blue(),
        )
        await user.update()
        await Interaction.channel.send(embed=embed)

    @item.sub_command(name="unequip", description="unequip an item")
    async def unequip(self, Interaction: disnake.ApplicationCommandInteraction):
        # translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        embed = disnake.Embed(
            title=translation["unequip"]["1"], color=disnake.Color.blue()
        )
        view = StandSelectDropdown(Interaction, user.stands)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        stand_index = view.value
        stand: Stand = user.stands[view.value]

        if len(stand.items) == 0:
            embed = disnake.Embed(
                title=translation["unequip"]["2"], color=disnake.Color.blue()
            )
            await Interaction.channel.send(embed=embed)
            return

        view = ItemSelectDropdown(Interaction, stand.items)
        await Interaction.channel.send(embed=embed, view=view)
        await wait_for(view)
        item = stand.items.pop(view.value)
        user.stands[stand_index] = stand
        user.items.append(item)
        embed = disnake.Embed(
            title=translation["unequip"]["3"].format(item.name, stand.name),
            color=disnake.Color.blue(),
        )
        await user.update()
        await Interaction.channel.send(embed=embed)

    @item.sub_command(name="unequipall", description="unequip all items from a stand")
    async def unequip_all(self, Interaction: disnake.ApplicationCommandInteraction):
        # translation
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        embed = disnake.Embed(
            title=translation["unequip"]["1"], color=disnake.Color.blue()
        )
        view = StandSelectDropdown(Interaction, user.stands)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        stand_index = view.value
        stand: Stand = user.stands[view.value]

        if len(stand.items) == 0:
            embed = disnake.Embed(
                title=translation["unequip"]["2"], color=disnake.Color.blue()
            )
            await Interaction.channel.send(embed=embed)
            return

        for item in stand.items:
            user.items.append(item)
        stand.items = []
        user.stands[stand_index] = stand
        embed = disnake.Embed(
            title=translation["unequipall"]["1"].format(stand.name),
            color=disnake.Color.blue(),
        )
        await user.update()
        await Interaction.channel.send(embed=embed)

    @item.sub_command(name="use", description="use one of your non equipable items.")
    async def use(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        usable_items = [item for item in user.items if not item.is_equipable]
        if len(usable_items) == 0:
            embed = disnake.Embed(
                title=translation["use"]["1"], color=disnake.Color.blue()
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        embed = disnake.Embed(title=translation["use"]["2"], color=disnake.Color.blue())
        view = ItemSelectDropdown(Interaction, usable_items)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        index = view.value
        item = usable_items[index]
        index = [i.id for i in user.items].index(item.id)
        item = user.items.pop(index)

        # Gacha items
        gacha_item = [2, 12]
        # Stand chip
        chip_ids = [8, 9, 10, 11, 14]
        actual_id = [9, 0, 5, 29, 162]
        # Requiem IDs
        requiemable = [49, 6, 59]
        requiem_stand = [57, 82, 83]
        # action based on which item was used
        if item.id in gacha_item:  # Stand arrows classic gacha
            if item.id == 2:
                stand_list = [
                    get_stand_from_template(stand) for stand in self.stfubot.stand_file
                ]
            if item.id == 12:
                stand_list = [
                    get_stand_from_template(stand)
                    for stand in self.stfubot.stand_file
                    if stand["id"] < 31
                ]
            drop: Stand = get_drop_from_list(stand_list)[0]
            msg = add_to_available_storage(user, drop)
            if msg:
                embed = disnake.Embed(
                    title=translation["use"]["3"].format(msg),
                    color=disnake.Color.blue(),
                )
                embed.set_thumbnail(
                    url="https://vignette.wikia.nocookie.net/jjba/images/9/9f/Arrow_anime.png/revision/latest?cb=20190614222010"
                )
                embed = stand_fields(drop, embed)
                await user.update()
                await Interaction.channel.send(embed=embed)
                return
            embed = disnake.Embed(
                title=translation["use"]["4"], color=disnake.Color.blue()
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.channel.send(embed=embed)
            return
        if item.id == 3:  # Requiem stand
            view = StandSelectDropdown(Interaction, user.stands)
            embed = disnake.Embed(
                title=translation["use"]["5"], color=disnake.Color.blue()
            )
            await Interaction.channel.send(embed=embed, view=view)
            await wait_for(view)
            stand: Stand = user.stands[view.value]
            if stand.ascension + stand.stars >= 7:
                embed = disnake.Embed(
                    title=translation["use"]["6"], color=disnake.Color.blue()
                )
                embed.set_image(url=self.stfubot.avatar_url)
                await Interaction.channel.send(embed=embed)
                return
            if stand.id in requiemable:
                index = requiemable.index(stand.id)
                new_stand_template = self.stfubot.stand_file[requiem_stand[index]]
                new_stand = get_stand_from_template(new_stand_template)
                new_stand.items = stand.items
                new_stand.reset()
                user.stands[view.value] = new_stand
                await user.update()
                embed = disnake.Embed(
                    title=translation["use"]["7"], color=disnake.Color.blue()
                )
                embed = stand_fields(new_stand, embed)
                await Interaction.channel.send(embed=embed)
                return
            stand.ascension += 1
            user.stands[view.value] = stand
            embed = disnake.Embed(
                title=translation["use"]["8"].format(stand.name, stand.ascension),
                color=disnake.Color.blue(),
            )
            embed.set_image(url="https://storage.stfurequiem.com/item_special/6.gif")
            await user.update()
            await Interaction.channel.send(embed=embed)
        if item.id in chip_ids:  # Stand Chips
            index = chip_ids.index(item.id)
            new_stand_template = self.stfubot.stand_file[actual_id[index]]
            new_stand = get_stand_from_template(new_stand_template)
            msg = add_to_available_storage(user, new_stand)
            if msg:
                embed = disnake.Embed(
                    title=translation["use"]["3"].format(msg),
                    color=disnake.Color.blue(),
                )
                embed = stand_fields(new_stand, embed)
                await user.update()
                await Interaction.channel.send(embed=embed)
                return
            embed = disnake.Embed(
                title=translation["use"]["4"], color=disnake.Color.blue()
            )
            await Interaction.channel.send(embed=embed)
            user.items.append(item)
            return
        if item.id == 13:  # bag of coins
            amount = random.randint(75, 125)
            user.coins += amount
            embed = disnake.Embed(
                title=translation["use"]["9"].format(amount), color=disnake.Color.blue()
            )
            embed.set_image(
                url="https://i.pinimg.com/originals/a5/e8/2d/a5e82d700ff336637489b44f32d36095.gif"
            )
            await user.update()
            await Interaction.channel.send(embed=embed)
            return


def setup(stfubot: StfuBot):
    stfubot.add_cog(Items(stfubot))