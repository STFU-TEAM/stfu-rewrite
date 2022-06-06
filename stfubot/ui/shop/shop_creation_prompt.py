# At the top of the file.
import disnake
from disnake.ext import commands
from disnake import TextInputStyle

# Subclassing the modal.
class ShopModal(disnake.ui.Modal):
    def __init__(self, translation: dict):
        self.name:str = "None",
        self.description:str = "None"
        self.translation = translation
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label=translation["ui"]["shop_modal"]["1"],
                placeholder=translation["ui"]["shop_modal"]["2"],
                custom_id="shop_name",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label=translation["ui"]["shop_modal"]["3"],
                placeholder=translation["ui"]["shop_modal"]["4"],
                custom_id="shop_description",
                style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(
            title=translation["ui"]["shop_modal"]["5"],
            custom_id="create_shop",
            components=components,
        )

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title=self.translation["ui"]["shop_modal"]["6"])
        embed.set_image(url="https://storage.stfurequiem.com/randomAsset/shop.gif")
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value,
                inline=False,
            )
        await inter.response.send_message(embed=embed)