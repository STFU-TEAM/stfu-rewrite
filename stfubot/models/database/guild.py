import datetime
import disnake

from typing import List, Union, Optional

from typing import TYPE_CHECKING

# It's for typehint
if TYPE_CHECKING:
    from stfubot.models.database.maindatabase import Database


class Guild:
    def __init__(self, data: dict, database: "Database"):
        self.data = data
        self.database = database

        self.lang: str = data["lang"]
        self.donor_status: bool = data["donor_status"]

    async def update(self):
        await self.database.update_guild(self.to_dict())

    def to_dict(self) -> dict:
        self.data["lang"] = self.lang
        self.data["donor_status"] = self.donor_status
        return self.data


def create_guild(id: str):
    return {"_id": id, "lang": "en_US", "donor_status": False}