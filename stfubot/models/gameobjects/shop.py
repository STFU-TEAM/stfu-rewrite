import disnake
import uuid

from typing import List, TYPE_CHECKING

# It's for typehint
if TYPE_CHECKING:
    from stfubot.models.database.maindatabase import Database
    from stfubot.models.database.user import User


from stfubot.models.gameobjects.items import Item, item_from_dict


class Shop:
    def __init__(self, data: dict, database: "Database"):
        self.database: "Database" = database
        self.data = data
        self.id: str = data["_id"]
        self.owner: str = data["owner"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.image_url: str = data["image_url"]
        self.items: List[Item] = [item_from_dict(s) for s in data["items"]]
        self.prices: List[int] = data["prices"]

    def sell(self, item: Item, price: int):
        self.items.append(item)
        self.prices.append(price)

    async def buy(self, index: int, buyer: "User"):
        item = self.items.pop(index)
        price = self.prices.pop(index)
        buyer.coins -= price
        buyer.items.append(item)
        owner = await self.database.get_user_info(self.owner)
        owner.coins += price
        await buyer.update()
        await owner.update()
        await self.update()

    async def update(self) -> None:
        """Updata the shop in the database"""
        await self.database.update_shop(self.to_dict())

    def to_dict(self) -> dict:
        self.data["name"] = self.name
        self.data["description"] = self.description
        self.data["image_url"] = self.image_url
        self.data["items"] = [s.to_dict() for s in self.items]
        self.data["prices"] = self.prices
        return self.data


def create_shop(name: str, description: str, user_id: str) -> dict:
    """Create the shop data

    Args:
        name (str): name of the shop
        description (str): description of the shop

    Returns:
        dict: data of the shop
    """
    return {
        "_id": str(uuid.uuid4()),
        "owner": user_id,
        "name": name,
        "description": description,
        "image_url": "https://storage.stfurequiem.com/randomAsset/shop.gif",
        "items": [],
        "prices": [],
    }
