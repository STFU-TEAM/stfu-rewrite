class Item:
    """This interface to jsoned data THIS CLASS IS NOT INTENDED TO BE CREATED MANUALLY
    Or to be modified.
    """

    def __init__(self, data: dict):
        self.data: dict = data
        self.id: int = data["id"]
        self.bonus_hp: int = data["bonus_hp"]
        self.bonus_damage: int = data["bonus_damage"]
        self.bonus_speed: int = data["bonus_speed"]
        self.bonus_critical: int = data["bonus_critical"]
        self.price: int = data["price"]
        self.prurchasable: bool = data["prurchasable"]
        # Variable
        self.special: int = 0

    def to_dict(self):
        return self.data

    def special(self):
        pass


def item_from_dict(data: dict) -> Item:
    """take a dict and return an Item object

    Args:
        data (dict): normalized data

    Returns:
        Item: Item class
    """
    return Item(data)