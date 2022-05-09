from stfubot.models.gameobjects.items import Item, item_from_dict
from stfubot.models.gameobjects.effects import Effect
from typing import List, TypeVar

XPRATE = 0.1
HPSCALING = 50
SPEEDSCALING = 1
DAMAGESCALING = 10
CRITICALSCALING = 0.1

stand = TypeVar("stand", "Stand")


class Stand:
    def __init__(self, data: dict):
        # define the constant
        self.data: dict = data
        self.id: int = data["id"]
        self.position: int = data["position"]
        self.name: str = data["name"]
        self.stars: int = data["stars"]
        self.xp: int = data["xp"]
        self.ascension: int = data["ascension"]
        self.base_critical: int = data["base_critical"]
        self.base_hp: int = data["base_hp"]
        self.base_damage: int = data["base_damage"]
        self.base_speed: int = data["base_speed"]
        self.items: List[Item] = [item_from_dict(s) for s in data["items"]]

        # Compute the starting Items and XP scaling.
        bonus_hp = 0
        bonus_damage = 0
        bonus_speed = 0
        bonus_critical = 0
        for item in self.items:
            bonus_hp += item.bonus_hp
            bonus_damage += item.bonus_damage
            bonus_speed += item.bonus_speed
            bonus_critical += item.bonus_critical
        # LEVEL SCALING
        bonus_hp += XPRATE * self.xp * (7 - self.stars) * HPSCALING
        bonus_damage += XPRATE * self.xp * (7 - self.stars) * DAMAGESCALING
        bonus_speed += XPRATE * self.xp * (7 - self.stars) * SPEEDSCALING
        bonus_critical += XPRATE * self.xp * (7 - self.stars) * CRITICALSCALING
        # Define the starting STATS and variables
        self.current_hp = self.base_hp + bonus_hp
        self.current_damage = self.base_damage + bonus_damage
        self.current_speed = self.base_speed + bonus_speed
        self.current_critical = self.base_critical + bonus_critical
        self.effects: List[Effect] = []
        self.special: int = 0

    def attack(self, ennemy_stand: stand) -> dict:
        pass

    def as_effects(self):
        return self.effects

    def end_turn(self):
        pass

    def to_dict(self) -> dict:
        self.data["position"] = self.position
        self.data["xp"] = self.xp
        self.data["ascension"] = self.ascension
        self.ascension["items"] = [s.to_dict() for s in self.items]
        return self.data


def stand_from_dict(data: dict) -> Stand:
    return Stand(data)