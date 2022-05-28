import random

from typing import TYPE_CHECKING, List


# It's for typehint
if TYPE_CHECKING:
    from gameobjects.stands import Stand


"""

name your fonction to the stand

def item_special_boiler_plate(stand:"Stand",allied_stand:List["Stand"],ennemy_stand:List["Stand"])->tuple:
    #Whatever your code does to the lists above
    #Payload Contain behavior change to the game
    #message is what should be printed to the embed
    return message


"""


def dio_Knife(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    message = "None"
    return message


def stand_arrows(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    message = "None"
    return message


def requiem_arrow(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    message = "None"
    return message


def giornos_ladybug(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    message = "None"
    return message


def sheer_heart_attack(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    multiplier = 30
    valid_stand = [i for i in ennemy_stand if i.is_alive()]
    if len(valid_stand) != 0:
        target = random.choice(valid_stand)
        target.current_hp -= multiplier
        message = f"｢{stand.name}｣'s Sheer heart attack explode on {target.name} for {multiplier} damage"
    message = f"Sheer heart attack schearch for ennemies"
    return message


def red_stone_of_aja(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    stand.current_hp += 100
    stand.current_speed += 20
    stand.current_damage += 50
    stand.current_critical += 50

    message = f"｢{stand.name}｣ becomes transcend"

    return message


def stone_mask(
    stand: "Stand", allied_stand: List["Stand"], ennemy_stand: List["Stand"]
) -> tuple:
    stand.current_hp += 30
    stand.current_damage += 30

    message = f"｢{stand.name}｣ becomes a vempire"
    return message


item_specials = {
    "1": dio_Knife,
    "2": stand_arrows,
    "3": requiem_arrow,
    "4": giornos_ladybug,
    "5": sheer_heart_attack,
    "6": red_stone_of_aja,
    "7": stone_mask,
}