import disnake

from typing import List

from stfubot.models.gameobjects.gang import Gang

# drop downelement class
class Dropdown(disnake.ui.Select):
    def __init__(
        self,
        gangs: List[Gang],
        lang: str = "en",
    ):
        self.gangs = gangs
        self.lang = lang
        options = [
            disnake.SelectOption(
                label=f"{gang.name}",
                emoji="🏡",
                value=i,
            )
            for i, gang in enumerate(gangs)
        ]
        super().__init__(
            placeholder="Select a gang",
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        # get the stand index
        index = int(self.values[0])
        v: GangSelectDropdown = self.view
        # get the message initial content

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label=f"You have selected {self.gangs[index].name}",
                disabled=True,
                style=disnake.ButtonStyle.blurple,
                emoji="✅",
            )
        )
        self.interaction = interaction
        await interaction.response.edit_message(view=view)
        v.value = index
        v.stop()


class GangSelectDropdown(disnake.ui.View):
    def __init__(
        self,
        interaction: disnake.Interaction,
        gangs: List[Gang],
        lang: str = "en",
        timeout: float = 180,
    ):
        super().__init__(timeout=timeout)
        self.value: int = None
        self.interaction = interaction
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(gangs, lang=lang))

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return self.interaction.author.id == interaction.author.id