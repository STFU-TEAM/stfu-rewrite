import disnake


from stfubot.globals.variables import SHOPCREATIONCOST, ITEMTYPE, ITEMBYTYPE
from stfubot.globals.emojis import CustomEmoji

# utils
from stfubot.utils.decorators import database_check, shop_check
from stfubot.utils.functions import wait_for, is_url_image


# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.models.gameobjects.shop import Shop
from stfubot.models.gameobjects.items import item_from_dict

# specific class import
from disnake.ext import commands
from typing import List

# ui
from stfubot.ui.shop.shop_creation_prompt import ShopModal
from stfubot.ui.shop.item_select_shop import ShopItemSelectDropdown
from stfubot.ui.place_holder import PlaceHolder
from stfubot.ui.confirmation import Confirm
from stfubot.ui.item_select import ItemSelectDropdown


async def autocomplete_type(inter, string: str) -> List[str]:
    return [lang for lang in ITEMTYPE if string.lower() in lang.lower()]


class Shop(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(
        name="shop", description="every commands to manage and buy at shops"
    )
    @database_check()
    async def shop(self, Interaction: disnake.ApplicationCommandInteraction):
        pass

    @shop.sub_command(name="create", description="Create a public shop.")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def create(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        # Shop already exists
        if user.shop_id != None:
            embed = disnake.Embed(
                title=translation["error_meesages"]["shop_created"],
                color=disnake.Color.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return

        embed = disnake.Embed(
            title=translation["shop_create"]["1"].format(SHOPCREATIONCOST)
        )
        embed.set_image(url="https://storage.stfurequiem.com/randomAsset/shop.gif")
        view = Confirm(Interaction)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        Interaction = view.interaction

        # Refuse to pay the price
        if not view.value:
            embed = disnake.Embed(title=translation["shop_create"]["2"])
            embed.set_image(url="https://storage.stfurequiem.com/randomAsset/shop.gif")
            await Interaction.response.edit_message(embed=embed, view=PlaceHolder())
            return
        modal = ShopModal(translation)
        await Interaction.response.send_modal(modal=modal)

        modal_inter: disnake.ModalInteraction = await self.stfubot.wait_for(
            "modal_submit",
            check=lambda i: i.custom_id == "create_shop"
            and i.author.id == Interaction.author.id,
            timeout=300,
        )
        shop_name = modal_inter.text_values["shop_name"]
        shop_description = modal_inter.text_values["shop_description"]
        id = await self.stfubot.database.add_shop(shop_name, shop_description, user.id)
        user.shop_id = id
        await user.update()

    @shop.sub_command(name="sell", description="sell an item to you shop")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @shop_check()
    async def sell(
        self, Interaction: disnake.ApplicationCommandInteraction, price: int
    ):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        shop = await self.stfubot.database.get_shop_info(user.shop_id)

        if len(shop.items) >= 24:
            embed = disnake.Embed(title=translation["shop_sell"]["3"])
            embed.set_image(url=shop.image_url)
            await Interaction.send(embed=embed)
            return
        embed = disnake.Embed(title=translation["shop_sell"]["1"])
        embed.set_image(url=shop.image_url)
        view = ItemSelectDropdown(Interaction, user.items)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        index = view.value
        item = user.items.pop(index)

        shop.sell(item, price)
        await shop.update()
        await user.update()
        embed = disnake.Embed(
            title=translation["shop_sell"]["2"].format(
                item.name, f"{price}{CustomEmoji.COIN}"
            )
        )
        embed.set_image(url=shop.image_url)
        await Interaction.channel.send(embed=embed)

    @shop.sub_command(name="remove", description="remove an item from your shop")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @shop_check()
    async def remove(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        # Shop does no exists
        if user.shop_id == None:
            embed = disnake.Embed(
                title=translation["error_meesages"]["shop_not_created"],
                color=disnake.Color.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return

        shop = await self.stfubot.database.get_shop_info(user.shop_id)

        if len(shop.items) == 0:
            embed = disnake.Embed(
                title=translation["shop_remove"]["3"], color=disnake.Color.blue()
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return

        view = ShopItemSelectDropdown(Interaction, shop.items, shop.prices)
        embed = disnake.Embed(
            title=translation["shop_remove"]["1"],
            color=disnake.Color.blue(),
        )
        embed.set_image(url=shop.image_url)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)

        item = shop.items.pop(view.value)
        price = shop.prices.pop(view.value)
        user.items.append(item)

        await shop.update()
        await user.update()

        embed = disnake.Embed(
            title=translation["shop_remove"]["2"].format(
                f"{item.name}|{price}{CustomEmoji.COIN}"
            ),
            color=disnake.Color.blue(),
        )
        await Interaction.channel.send(embed=embed)

    @shop.sub_command(name="show", description="show your own shop")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @shop_check()
    async def show(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        # Shop does no exists
        if user.shop_id == None:
            embed = disnake.Embed(
                title=translation["error_meesages"]["shop_not_created"],
                color=disnake.Color.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return

        shop = await self.stfubot.database.get_shop_info(user.shop_id)
        embed = disnake.Embed(
            title=translation["shop_show"]["1"].format(user.discord.name),
            color=disnake.Color.blue(),
        )
        embed.add_field(
            name=shop.name,
            value=shop.description,
            inline=False,
        )
        embed.add_field(
            name=translation["shop_show"]["2"],
            value="\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            inline=False,
        )
        for i, item in enumerate(shop.items):
            embed.add_field(
                name=f"{item.name}{item.emoji}",
                value=translation["shop_show"]["3"].format(shop.prices[i]),
                inline=True,
            )

        embed.set_image(url=shop.image_url)
        await Interaction.send(embed=embed)

    @shop.sub_command(name="changeimage", description="change the shop image")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @shop_check()
    async def changeimage(
        self, Interaction: disnake.ApplicationCommandInteraction, url: str
    ):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        # Shop does no exists
        if user.shop_id == None:
            embed = disnake.Embed(
                title=translation["error_meesages"]["shop_not_created"],
                color=disnake.Color.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return

        if not is_url_image(url):
            embed = disnake.Embed(
                title=translation["error_meesages"]["not_an_image"],
                color=disnake.Color.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return

        shop = await self.stfubot.database.get_shop_info(user.shop_id)

        shop.image_url = url
        await shop.update()
        embed = disnake.Embed(
            title=translation["shop_changeimage"]["1"], color=disnake.Color.blue()
        )
        embed.set_image(url=shop.image_url)
        await Interaction.send(embed=embed)

    @shop.sub_command(
        name="buy", description="buy the cheapest items from other player"
    )
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    async def buy(
        self,
        Interaction: disnake.ApplicationCommandInteraction,
        itemtype: str = commands.Param(autocomplete=autocomplete_type),
    ):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        item_list = [item_from_dict(item) for item in ITEMBYTYPE[itemtype]]

        view = ItemSelectDropdown(Interaction, item_list)
        embed = disnake.Embed(
            title=translation["shop_buy"]["1"], color=disnake.Color.blue()
        )
        embed.set_image(url="https://storage.stfurequiem.com/randomAsset/shop.gif")
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)

        item = item_list[view.value]

        shop, index = await self.stfubot.database.find_suitable_shop(item, user.shop_id)

        if shop == None:
            embed = disnake.Embed(
                title=translation["error_meesages"]["no_shop_found"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url="https://storage.stfurequiem.com/randomAsset/shop.gif")
            await Interaction.channel.send(embed=embed)
            return

        shop_item = shop.items[index]
        shop_price = shop.prices[index]

        if user.coins < shop_price:
            embed = disnake.Embed(
                title=translation["error_meesages"]["not_enough_money"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url="https://storage.stfurequiem.com/randomAsset/shop.gif")
            await Interaction.channel.send(embed=embed)
            return

        embed = disnake.Embed(title=shop.name, description=shop.description)
        embed.set_image(url=shop.image_url)
        embed.add_field(
            name=translation["shop_buy"]["2"],
            value=translation["shop_buy"]["3"].format(
                shop_item.name, f"{shop_price}{CustomEmoji.COIN}"
            ),
        )
        view = Confirm(Interaction)
        await Interaction.channel.send(embed=embed, view=view)
        await wait_for(view)
        Interaction = view.interaction
        if not view.value:
            embed = disnake.Embed(title=shop.name, description=shop.description)
            embed.set_image(url=shop.image_url)
            embed.add_field(
                name=translation["shop_buy"]["4"], value=translation["shop_buy"]["5"]
            )
            await Interaction.send(embed=embed)
            return
        await shop.buy(index, user)
        embed = disnake.Embed(title=shop.name, description=shop.description)
        embed.set_image(url=shop.image_url)
        embed.add_field(
            name=translation["shop_buy"]["6"],
            value=translation["shop_buy"]["7"].format(shop_item.name),
        )
        await Interaction.send(embed=embed)


def setup(stfubot: StfuBot):
    stfubot.add_cog(Shop(stfubot))