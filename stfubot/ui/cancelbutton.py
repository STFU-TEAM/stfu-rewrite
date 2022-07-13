import disnake


class CancelButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(label="Cancel", emoji="❌", style=disnake.ButtonStyle.grey)

    async def callback(self, interaction: disnake.MessageInteraction):
        self.view.value = "cancel"
        self.view.interaction = interaction
        self.view.stop()
