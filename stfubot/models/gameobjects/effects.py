import disnake

Emoji = {
    "STUN": "<:stunned:952619012544684122>",
    "POISON": "<:poison:952619038746501170>",
    "WEAKEN": "<:weakened:952620861762985994>",
}


class Effect:
    def __init__(self, data: dict):
        self.type: str = data["type"]
        self.duration: int = data["duration"]
        self.value: int = data["value"]
        self.emoji = Emoji[self.type]
