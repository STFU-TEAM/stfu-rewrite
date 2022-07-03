import random
import math
import json

from stfubot.models.gameobjects.items import Item, item_from_dict
from stfubot.models.gameobjects.effects import Effect, EffectType
from stfubot.models.gameobjects.standabilities import specials
from typing import List, TypeVar

from stfubot.globals.variables import (
    HPSCALING,
    DAMAGESCALING,
    SPEEDSCALING,
    CRITICALSCALING,
    CRITMULTIPLIER,
    DODGENERF,
    STXPTOLEVEL,
    MAX_LEVEL,
    LEVEL_TO_STAT_INCREASE,
)

stand = TypeVar("stand", bound="Stand")


class Stand:
    def __init__(self, data: dict):
        with open("stfubot/data/static/stand_template.json", "r") as item:
            stand_file = json.load(item)["stand"]
        # define the constant
        self.data: dict = data
        self.id: int = data["id"]
        self.name: str = stand_file[self.id - 1]["name"]
        self.stars: int = stand_file[self.id - 1]["stars"]
        self.xp: int = data["xp"]
        self.ascension: int = data["ascension"]
        self.base_critical: float = stand_file[self.id - 1]["base_critical"]
        self.base_hp: int = stand_file[self.id - 1]["base_hp"]
        self.base_damage: int = stand_file[self.id - 1]["base_damage"]
        self.base_speed: int = stand_file[self.id - 1]["base_speed"]
        self.turn_for_ability: int = stand_file[self.id - 1]["turn_for_ability"]
        self.special_description: str = stand_file[self.id - 1]["special_description"]
        self.items: List[Item] = [item_from_dict(s) for s in data["items"]]
        self.level: int = min(MAX_LEVEL, self.xp // STXPTOLEVEL)

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
        bonus_hp += (
            (self.level // LEVEL_TO_STAT_INCREASE)
            * self.base_damage
            * (HPSCALING / 100)
        )
        bonus_damage += (
            (self.level // LEVEL_TO_STAT_INCREASE)
            * self.base_hp
            * (DAMAGESCALING / 100)
        )
        bonus_speed += (
            (self.level // LEVEL_TO_STAT_INCREASE)
            * self.base_speed
            * (SPEEDSCALING / 100)
        )
        bonus_critical += (
            (self.level // LEVEL_TO_STAT_INCREASE)
            * self.base_critical
            * (CRITICALSCALING / 100)
        )

        # Define the starting STATS and variables
        self.current_hp = int(self.base_hp + bonus_hp * (1 + self.ascension / 3))
        self.current_damage = int(
            self.base_damage + bonus_damage * (1 + self.ascension / 3)
        )
        self.current_speed = int(
            self.base_speed + bonus_speed * (1 + self.ascension / 3)
        )
        self.current_critical = self.base_critical + bonus_critical * (
            1 + self.ascension / 3
        )

        self.start_hp = self.current_hp
        self.start_damage = self.current_damage
        self.start_speed = self.current_speed
        self.start_critical = self.current_critical
        self.effects: List[Effect] = []
        self.special_meter: int = 0
        self.turn: int = 0
        self.ressistance: int = 1

    def is_alive(self) -> bool:
        """Check if a stand is alive

        Returns:
            bool: The  answer
        """
        if self.current_hp <= 0:
            self.current_hp = 0
        return self.current_hp > 0

    def attack(self, ennemy_stand: stand, multiplier: int = 1) -> dict:
        """Attack a stand

        Args:
            ennemy_stand (stand): the stand to attack

        Returns:
            dict: Default {"damage": 0, "critical": False, "Dodged": False}
        """
        # create a return dict this time :)
        atck = {"damage": 0, "critical": False, "Dodged": False}
        crit = random.randint(0, 100)
        # classic attack have no modifiers so x1
        multi = multiplier
        if self.current_critical >= crit:
            multi *= CRITMULTIPLIER
            atck["critical"] = True
        dodge_roll = False
        # If the ennemy is faster check if he dodged
        if ennemy_stand.current_speed > self.current_speed:
            dodge_roll = (
                random.randint(0, 100)
                < (ennemy_stand.current_speed - self.current_speed) // DODGENERF
            )
            atck["Dodged"] = dodge_roll
        # if it is dodged the we do not compute damage
        if dodge_roll:
            return atck
        damage = (self.current_damage // ennemy_stand.ressistance) * multi
        ennemy_stand.current_hp -= damage
        atck["damage"] = damage
        return atck

    def is_stunned(self) -> bool:
        """Check if the stand is stunned

        Returns:
            bool: whether the stand is stunned
        """
        return EffectType.STUN in [c.type for c in self.effects]

    def end_turn(self) -> None:
        """Make the relevant action at the end of the turn"""
        # apply effects
        for effect in self.effects:
            if effect.duration <= 0:
                continue
            if effect.type == EffectType.POISON:
                self.current_hp -= effect.value
            elif effect.type == EffectType.WEAKEN:
                self.ressistance *= effect.value
            elif (
                effect.type == EffectType.REGENERATION
                and self.current_hp < self.base_hp
            ):
                self.current_hp += effect.value
            effect.duration -= 1
        # cleanup effect that have ended
        self.effects = [e for e in self.effects if e.duration > 0]
        # add to the special
        self.special_meter += 1
        self.turn += 1
        # add to items special meter
        for item in self.items:
            item.special_meter += 1

    def as_special(self) -> bool:
        return self.special_meter >= self.turn_for_ability

    def special(self, allies: List[stand], ennemies: List[stand]) -> tuple:
        """used for fight

        Args:
            allies (List[stand]): list of allies
            ennemies (List[stand]): list of ennemies

        Returns:
            tuple: payload,message
        """
        # reset the meter
        self.special_meter = 0
        return specials[f"{self.id}"](self, allies, ennemies)

    def to_dict(self) -> dict:
        """Update the data of the stand

        Returns:
            dict: the data of the stand
        """
        self.data["xp"] = self.xp
        self.data["ascension"] = self.ascension
        self.data["items"] = [s.to_dict() for s in self.items]
        return self.data

    def reset(self) -> None:
        """call at the end of a fight"""
        self.data["xp"] = self.xp
        self.data["ascension"] = self.ascension
        self.data["items"] = [s.to_dict() for s in self.items]
        self.__init__(self.data)


def stand_from_dict(data: dict) -> Stand:
    return Stand(data)


def get_stand_from_template(template: dict) -> Stand:
    data = {"id": template["id"], "xp": 0, "ascension": 0, "items": []}
    return Stand(data)
