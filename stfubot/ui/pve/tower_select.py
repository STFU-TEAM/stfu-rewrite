import disnake
import json

from stfubot.globals.emojis import CustomEmoji

# drop downelement class
class Dropdown(disnake.ui.Select):
    def __init__(
        self,
        lang: str = "en",
    ):
        with open("stfubot/data/static/tower.json", "r") as item:
            tower_file = json.load(item)["towers"]
        self.lang = lang
        self.emojiNumbers = [
            CustomEmoji.THREE,
            CustomEmoji.FOUR,
            CustomEmoji.FIVE,
            CustomEmoji.SIX,
            CustomEmoji.SEVEN,
            CustomEmoji.EIGHT,
        ]

        self.towers = [tower_file["1"], tower_file["2"], tower_file["3"]]

        options = [
            disnake.SelectOption(
                label=f"{tower['name']}",
                description=f"levels:{tower['levels']}",
                emoji=self.emojiNumbers[i],
                value=(i + 1),
            )
            for i, tower in enumerate(self.towers)
        ]
        super().__init__(
            placeholder="Select a tower",
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        # get the stand index
        index = int(self.values[0])
        v: TowerSelectDropdown = self.view
        # get the message initial content

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label=f"You have selected {self.towers[index - 1]['name']}",
                disabled=True,
                style=disnake.ButtonStyle.blurple,
                emoji=self.emojiNumbers[index - 1],
            )
        )
        self.interaction = interaction
        await interaction.response.edit_message(view=view)
        v.value = index
        v.stop()


class TowerSelectDropdown(disnake.ui.View):
    def __init__(
        self,
        interaction: disnake.Interaction,
        lang: str = "en",
        timeout: float = 180,
    ):
        super().__init__(timeout=timeout)
        self.value = None
        self.interaction = interaction
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(lang=lang))

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        # check if the author is the one who pressed the
        return self.interaction.author.id == interaction.author.id
