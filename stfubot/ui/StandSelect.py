import disnake
import json

from stfubot.globals.emojis import CustomEmoji
from stfubot.models.gameobjects.stands import Stand
from typing import List, Union

# drop downelement class
class Dropdown(disnake.ui.Select):
    def __init__(
        self,
        stand_list: List[Stand],
        disabled: List[bool],
        lang: str = "en",
        max_value: int = 1,
        min_value: int = 1,
    ):
        self.stand_list = stand_list
        self.lang = lang
        self.stop = False
        self.max_value = max_value
        self.emojiNumbers = [
            CustomEmoji.ONE,
            CustomEmoji.TWO,
            CustomEmoji.THREE,
            CustomEmoji.FOUR,
            CustomEmoji.FIVE,
            CustomEmoji.SIX,
            CustomEmoji.SEVEN,
            CustomEmoji.EIGHT,
            CustomEmoji.NINE,
            CustomEmoji.TEN,
        ]
        if len(disabled) == 0:
            disabled = [False] * len(stand_list)
        options = [
            disnake.SelectOption(
                label=f"『{stand.name}』",
                description=f'{stand.stars*"⭐"+stand.ascension*"🌟"}',
                emoji=self.emojiNumbers[index],
                value=str(index),
            )
            for index, stand in enumerate(stand_list)
            if not disabled[index]
        ]
        super().__init__(
            placeholder="Select the stand",
            min_values=min_value,
            max_values=max_value,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        # get the stand index
        index = int(self.values[0])
        v: StandSelectDropdown = self.view
        # get the message initial content

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label=f"You have selected 『{self.stand_list[index].name}』",
                disabled=True,
                style=disnake.ButtonStyle.blurple,
                emoji=self.emojiNumbers[index],
            )
        )
        self.interaction = interaction
        await interaction.response.edit_message(view=view)
        if self.max_value == 1:
            v.value = int(self.values[0])
        else:
            v.value = [int(i) for i in self.values]
        v.stop()


class StandSelectDropdown(disnake.ui.View):
    def __init__(
        self,
        interaction: disnake.Interaction,
        stand_list: List[Stand],
        disabled: List[bool] = [],
        lang: str = "en",
        timeout: float = 180,
        max_value: int = 1,
        min_value: int = 1,
        custom_user: disnake.User = None,
    ):
        super().__init__()
        self.value: Union[List[int], int] = None
        self.timeout = timeout
        self.interaction = interaction
        self.custom_user = custom_user
        # Adds the dropdown to our view object.
        self.add_item(
            Dropdown(
                stand_list,
                disabled,
                lang=lang,
                max_value=max_value,
                min_value=min_value,
            )
        )

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return (
            self.interaction.author.id == interaction.author.id
            and self.custom_user == None
        ) or self.custom_user.id == interaction.author.id