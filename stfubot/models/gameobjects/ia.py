import disnake

from typing import List

from stfubot.models.gameobjects.stands import Stand, stand_from_dict


class Ia:
    def __init__(self, data: dict):
        self.avatar = data["avatar"]

        class d:
            def __init__(self, name: str):
                self.name: str = name

        self.discord = d(data["name"])
        self.stands: List[Stand] = [stand_from_dict(s) for s in data["stands"]]
        self.message: disnake.Message = None
        self.is_human = False

    def choice(self, ennemies: List[Stand]):
        # What the Ia must prioritize
        def prio(x: Stand):
            return x.current_hp * (x.current_damage)

        ennemies.sort(key=prio, reverse=True)
        return ennemies[0]
