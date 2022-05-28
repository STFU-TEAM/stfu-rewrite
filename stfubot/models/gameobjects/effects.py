from enum import Enum


Emoji = {
    "STUN": "<:stunned:952619012544684122>",
    "POISON": "<:poison:952619038746501170>",
    "WEAKEN": "<:weakened:952620861762985994>",
    "REGENERATION": "<:regeneration:974407195426947143>",
}


class EffectType(Enum, str):
    STUN = "STUN"
    POISON = "POISON"
    WEAKEN = "WEAKEN"
    REGENERATION = "REGENERATION"


class Effect:
    def __init__(self, type: EffectType, duration: int, value: int):
        self.type: EffectType = type
        self.duration: int = duration
        self.value: int = value
        self.emoji = Emoji[self.type.name]
