import datetime
import disnake

from typing import List

from typing import TYPE_CHECKING

# It's for typehint
if TYPE_CHECKING:
    from database.maindatabase import Database

from gameobjects.stands import Stand, stand_from_dict
from gameobjects.items import Item, item_from_dict


class User:
    """| Class used as an interface to data ,Any change made to the class is also made to the data"""

    def __init__(self, data: dict, database: "Database"):
        """Class constructor

        Args:
            data (dict): User dict (see maindatabase file)
            database (_type_): An Instance of Databse (for Updates)
        """
        # Initialization variables
        self.data: dict = data
        self.database: "Database" = database
        # Inerant variables
        self.id: str = data["_id"]
        self.stands: List[Stand] = [stand_from_dict(s) for s in data["stands"]]
        self.gang_id: int = data["gang_id"]
        self.stand_storage: List[Stand] = [
            stand_from_dict(s) for s in data["stand_storage"]
        ]
        self.pstand_storage: List[Stand] = [
            stand_from_dict(s) for s in data["pstand_storage"]
        ]
        self.items: List[Item] = [item_from_dict(s) for s in data["items"]]
        self.achievements: List[int] = data["achievements"]
        self.gang_invites: List[int] = data["gang_invites"]
        self.custom_stand: int = data["custom_stand"]
        self.coins: int = data["coins"]
        self.xp: int = data["xp"]
        self.job: dict = data["job"]
        self.prestige: int = data["prestige"]
        self.global_elo: int = data["global_elo"]
        self.crusade_level: int = data["crusade_level"]
        self.tower_level: int = data["tower_level"]
        self.profile_image: str = data["profile_image"]
        self.join_date: datetime.datetime = data["join_date"]
        self.last_crusade: datetime.datetime = data["last_crusade"]
        self.last_adventure: datetime.datetime = data["last_adventure"]
        self.last_job: datetime.datetime = data["last_job"]
        self.last_vote: datetime.datetime = data["last_vote"]
        self.donor_status: datetime.datetime = data["donor_status"]
        self.over_heaven_supporter: bool = data["over_heaven_supporter"]
        self.early_supporter: bool = data["early_supporter"]
        self.discord: disnake.Member = None

    async def update(self) -> None:
        """Update the user info in the database"""
        await self.database.update_user(self.to_dict())

    def is_donator(self):
        status = self.early_supporter | self.over_heaven_supporter
        # regular donor status
        status |= (
            self.donor_status >= datetime.datetime.now()
            and self.donor_status != datetime.datetime.max
        )
        # answer
        return status

    def to_dict(self) -> dict:
        """Convert Class to storable data

        Returns:
            dict: Stand
        """
        self.data["stands"] = [s.to_dict() for s in self.stands]
        self.data["gang_id"] = self.gang_id
        self.data["stand_storage"] = [s.to_dict() for s in self.stand_storage]
        self.data["pstand_storage"] = [s.to_dict() for s in self.pstand_storage]
        self.data["items"] = [s.to_dict() for s in self.items]
        self.data["achievements"] = self.achievements
        self.data["gang_invites"] = self.gang_invites
        self.data["custom_stand"] = self.custom_stand
        self.data["coins"] = self.coins
        self.data["xp"] = self.xp
        self.data["job"] = self.job
        self.data["prestige"] = self.prestige
        self.data["global_elo"] = self.global_elo
        self.data["crusade_level"] = self.crusade_level
        self.data["tower_level"] = self.tower_level
        self.data["profile_image"] = self.profile_image
        self.data["join_date"] = self.join_date
        self.data["last_crusade"] = self.last_crusade
        self.data["last_adventure"] = self.last_adventure
        self.data["last_vote"] = self.last_vote
        self.data["last_job"] = self.last_job
        self.data["donor_status"] = self.donor_status
        self.data["over_heaven_supporter"] = self.over_heaven_supporter
        self.data["early_supporter"] = self.early_supporter
        return self.data


def create_user(user_id: str):
    data = {
        "_id": user_id,
        "gang_id": None,
        "stands": [],
        "stand_storage": [],
        "pstand_storage": [],
        "items": [],
        "achievements": [],
        "gang_invites": [],
        "custom_stand": None,
        "coins": 0,
        "xp": 0,
        "job": None,
        "prestige": 0,
        "global_elo": 0,
        "crusade_level": 0,
        "tower_level": 0,
        "profile_image": "https://i.pinimg.com/originals/77/ba/e4/77bae4f9d1c02f732e9271976539ed48.gif",
        "join_date": datetime.datetime.now(),
        "last_crusade": datetime.datetime.min,
        "last_adventure": datetime.datetime.min,
        "last_vote": datetime.datetime.min,
        "last_job": datetime.datetime.min,
        "donor_status": datetime.datetime.min,
        "over_heaven_supporter": False,
        "early_supporter": False,
    }
    return data
