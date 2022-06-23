from typing import List, Union
import disnake


# Define a simple View that gives us a confirmation menu
class Confirm(disnake.ui.View):
    def __init__(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user: Union[disnake.User, None] = None,
        timeout: float = 180,
    ):
        super().__init__(timeout=timeout)
        self.value = None
        self.interaction = interaction
        self.user = user
        self.author = None

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return (
            self.interaction.author.id == interaction.author.id and self.user == None
        ) or (self.user.id == interaction.author.id)

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @disnake.ui.button(emoji="✔️", style=disnake.ButtonStyle.blurple)
    async def confirm(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = True

        self.interaction = interaction
        self.author = interaction.author
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.blurple)
    async def cancel(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = False

        self.interaction = interaction
        self.author = interaction.author
        self.stop()
