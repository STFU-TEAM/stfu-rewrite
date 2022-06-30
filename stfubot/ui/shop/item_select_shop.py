import disnake
import json

from typing import List

from stfubot.models.gameobjects.items import Item
from stfubot.globals.emojis import CustomEmoji

# drop downelement class
class Dropdown(disnake.ui.Select):
    def __init__(
        self,
        items: List[Item],
        prices: List[int],
        lang: str = "en",
    ):
        self.lang = lang
        self.items: List[Item] = items
        self.prices: List[int] = prices
        options = [
            disnake.SelectOption(
                label=f"{item.name}|{prices[i]}💰",
                emoji=item.emoji,
                value=i,
            )
            for i, item in enumerate(items)
        ]
        super().__init__(
            placeholder="Select an item",
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        # get the stand index
        index = int(self.values[0])
        v: ShopItemSelectDropdown = self.view
        # get the message initial content

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label=f"You have selected {self.items[index].name}|{self.prices[index]} coins",
                disabled=True,
                style=disnake.ButtonStyle.blurple,
                emoji=self.items[index].emoji,
            )
        )
        self.interaction = interaction
        await interaction.response.edit_message(view=view)
        v.value = index
        v.stop()


class ShopItemSelectDropdown(disnake.ui.View):
    def __init__(
        self,
        interaction: disnake.Interaction,
        items: List[Item],
        prices: List[int],
        lang: str = "en",
        timeout: float = 180,
    ):
        super().__init__(timeout=timeout)
        self.value: int = None
        self.interaction = interaction
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(items, prices, lang=lang))

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return self.interaction.author.id == interaction.author.id