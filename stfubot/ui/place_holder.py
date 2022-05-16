import disnake


# Define a simple View that gives us a confirmation menu
class PlaceHolder(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None