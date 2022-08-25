import disnake
from disnake.ext import commands
from disnake import TextInputStyle

# Subclassing the modal.
class GangModal(disnake.ui.Modal):
    def __init__(self, translation: dict):
        self.translation = translation
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label=translation["ui"]["gang_modal"]["1"],
                placeholder=translation["ui"]["gang_modal"]["2"],
                custom_id="gang_name",
                style=TextInputStyle.short,
                max_length=25,
            ),
            disnake.ui.TextInput(
                label=translation["ui"]["gang_modal"]["3"],
                placeholder=translation["ui"]["gang_modal"]["4"],
                custom_id="gang_motd",
                style=TextInputStyle.paragraph,
            ),
            disnake.ui.TextInput(
                label=translation["ui"]["gang_modal"]["5"],
                placeholder=translation["ui"]["gang_modal"]["6"],
                custom_id="gang_motto",
                style=TextInputStyle.short,
                max_length=50,
            ),
        ]
        super().__init__(
            title=translation["ui"]["gang_modal"]["7"],
            custom_id="create_gang",
            components=components,
        )

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(
            title=self.translation["ui"]["gang_modal"]["8"], color=disnake.Color.blue()
        )
        embed.set_image(
            url="https://storage.stfurequiem.com/randomAsset/gang_default.jpg"
        )
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value,
                inline=False,
            )
        await inter.response.send_message(embed=embed)