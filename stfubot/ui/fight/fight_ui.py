import disnake
import time
import asyncio

from models.gameobjects.stands import Stand
from globals.emojis import CustomEmoji

from typing import List, Union

EmojiList = [
    CustomEmoji.ONE,
    CustomEmoji.TWO,
    CustomEmoji.THREE,
    CustomEmoji.FF,
]
# [ONE, TWO, THREE, FF]


class FightButton(disnake.ui.Button):
    def __init__(self, postion: int):
        super().__init__(
            style=disnake.ButtonStyle.blurple,
            emoji=EmojiList[postion],
            custom_id=str(postion),
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        view: FightUi = self.view
        view.value = int(self.custom_id)
        view.interaction = interaction
        view.stop()


class FightButtonFF(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            style=disnake.ButtonStyle.red, emoji=EmojiList[3], custom_id="ff"
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        view: FightUi = self.view
        view.value = self.custom_id
        view.interaction = interaction
        view.stop()


# Define a simple View that gives us a confirmation menu
class FightUi(disnake.ui.View):
    def __init__(
        self,
        interaction: Union[disnake.MessageInteraction, disnake.Message],
        user: disnake.User,
        watcher_stands: List[Stand],
        player_stands: List[Stand],
    ):
        super().__init__(timeout=60.0)  # 1 min timeout
        self.value = None
        self.interaction = interaction
        self.user = user
        # add the coresponding button to the view
        for i in range(len(watcher_stands)):
            # check if a button should be added
            if watcher_stands[i].is_alive():
                self.add_item(FightButton(i))
        # add the forfeit button
        self.add_item(FightButtonFF())

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return self.user.id == interaction.author.id
