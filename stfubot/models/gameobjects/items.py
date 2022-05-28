import json

from enum import Enum
from typing import TYPE_CHECKING, List


# It's for typehint
if TYPE_CHECKING:
    from gameobjects.stands import Stand


from gameobjects.itemabilities import item_specials

with open("stfubot/data/static/item_templates.json", "r", encoding="utf-8") as item:
    item_file = json.load(item)["item"]


class Item:
    """This interface to jsoned data THIS CLASS IS NOT INTENDED TO BE CREATED MANUALLY
    Or to be modified.
    """

    def __init__(self, data: dict):

        self.data: dict = data
        self.id: int = data["id"]
        self.name: str = item_file[f"{self.id}"]["name"]
        self.bonus_hp: int = item_file[f"{self.id}"]["bonus_hp"]
        self.bonus_damage: int = item_file[f"{self.id}"]["bonus_damage"]
        self.bonus_speed: int = item_file[f"{self.id}"]["bonus_speed"]
        self.bonus_critical: int = item_file[f"{self.id}"]["bonus_critical"]
        self.price: int = item_file[f"{self.id}"]["price"]
        self.prurchasable: bool = item_file[f"{self.id}"]["prurchasable"]
        self.emoji = item_file[f"{self.id}"]["emoji"]
        self.is_equipable = item_file[f"{self.id}"]["is_equipable"]
        self.is_active = item_file[f"{self.id}"]["is_active"]
        self.turn_for_ability = item_file[f"{self.id}"]["turn_for_ability"]
        # Variable
        self.special_meter: int = 0

    def to_dict(self):
        return self.data

    def special(self, stand, allies, ennemies) -> str:
        self.special_meter = 0
        return item_specials[f"{self.id}"](stand, allies, ennemies)

    def as_special(self):
        return self.is_active and self.special_meter >= self.turn_for_ability


def item_from_dict(data: dict) -> Item:
    """take a dict and return an Item object

    Args:
        data (dict): normalized data

    Returns:
        Item: Item class
    """
    return Item(data)


def get_item_from_template(template: dict) -> dict:
    return {"id": template["id"]}
