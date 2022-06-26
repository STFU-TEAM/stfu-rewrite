import disnake
import json

from typing import Optional

with open("stfubot/lang/lang.json", "r", encoding="utf8") as file:
    lang_file = json.load(file)["supported_lang"]

# drop downelement class
class Dropdown(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label=lang["name"],
                emoji=lang["emoji"],
                value=str(index),
            )
            for index, lang in enumerate(lang_file)
        ]
        super().__init__(
            placeholder="Select a language",
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        index = int(self.values[0])
        v: LangSelectDropdown = self.view
        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label=f"You have selected {lang_file[index]['name']}",
                disabled=True,
                style=disnake.ButtonStyle.blurple,
                emoji=lang_file[index]["emoji"],
            )
        )
        self.interaction = interaction
        await interaction.response.edit_message(view=view)
        v.value = lang_file[index]
        v.stop()


class LangSelectDropdown(disnake.ui.View):
    def __init__(
        self,
        interaction: disnake.Interaction,
    ):
        super().__init__()
        self.value: Optional[dict] = None
        self.interaction = interaction
        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return self.interaction.author.id == interaction.author.id
