import disnake

from enum import Enum

from typing import TYPE_CHECKING, Optional

# It's for typehint
if TYPE_CHECKING:
    from stfubot.models.gameobjects.stands import Stand


Emoji = {
    "STUN": "<:stunned:952619012544684122>",
    "POISON": "<:poison:952619038746501170>",
    "WEAKEN": "<:weakened:952620861762985994>",
    "REGENERATION": "<:regeneration:974407195426947143>",
    "SLOW": "<:slowed:993988645520412702>",
}


class EffectType(Enum):
    STUN = "STUN"
    POISON = "POISON"
    WEAKEN = "WEAKEN"
    REGENERATION = "REGENERATION"
    SLOW = "SLOW"


class Effect:
    def __init__(
        self,
        type: EffectType,
        duration: int,
        value: int,
        sender: Optional["Stand"] = None,
    ):
        self.type: EffectType = type
        self.duration: int = duration
        self.value: int = value
        self.emoji: disnake.PartialEmoji = Emoji[self.type.name]
        self.sender: Optional["Stand"] = sender
