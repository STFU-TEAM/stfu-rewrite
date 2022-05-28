import disnake

from disnake import emoji

from stfubot.globals.emojis import CustomEmoji


# Define a simple View that gives us a confirmation menu
class Stand_Select(disnake.ui.View):
    def __init__(self, interaction: disnake.Interaction):
        super().__init__()
        self.value = None
        self.interaction = interaction

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return self.interaction.author.id == interaction.author.id

    # return value is the emoji
    @disnake.ui.button(emoji=CustomEmoji.ONE, style=disnake.ButtonStyle.grey)
    async def ONE(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = CustomEmoji.ONE
        self.interaction = interaction
        self.stop()

    # return value is the emoji
    @disnake.ui.button(emoji=CustomEmoji.TWO, style=disnake.ButtonStyle.grey)
    async def TWO(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = CustomEmoji.TWO
        self.interaction = interaction
        self.stop()

    # return value is the emoji
    @disnake.ui.button(emoji=CustomEmoji.THREE, style=disnake.ButtonStyle.grey)
    async def THREE(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = CustomEmoji.THREE
        self.interaction = interaction
        self.stop()

    # return value is the emoji
    @disnake.ui.button(emoji="🎒", style=disnake.ButtonStyle.grey, custom_id="store")
    async def store(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = "🎒"
        self.interaction = interaction
        self.stop()

    # return value is the emoji
    @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.grey)
    async def cancel(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = "❌"
        self.interaction = interaction
        self.stop()

    async def on_timeout(self) -> None:
        """|coro|

        A callback that is called when a view's timeout elapses without being explicitly stopped.
        """
        raise TimeoutError