import disnake


# Define a simple View that gives us a confirmation menu
class ChooseStorage(disnake.ui.View):
    def __init__(self, interaction: disnake.ApplicationCommandInteraction):
        super().__init__()
        self.value = None
        self.interaction = interaction

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return self.interaction.author.id == interaction.author.id

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @disnake.ui.button(
        emoji="💿", label="Classic Storage", style=disnake.ButtonStyle.grey
    )
    async def Classic(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = False
        self.stop()
        self.interaction = interaction
        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label=f"You have selected Classic Storage",
                disabled=True,
                style=disnake.ButtonStyle.blurple,
                emoji="💿",
            )
        )
        await interaction.response.edit_message(view=view)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @disnake.ui.button(
        emoji="📀", label="Premium storage", style=disnake.ButtonStyle.grey
    )
    async def Premium(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.value = True
        self.stop()
        self.interaction = interaction
        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label=f"You have selected Premium Storage",
                disabled=True,
                style=disnake.ButtonStyle.blurple,
                emoji="📀",
            )
        )
        await interaction.response.edit_message(view=view)
