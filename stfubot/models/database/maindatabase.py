import motor.motor_asyncio
import asyncio
import os

from typing import List, Union

from database.user import User, create_user
from database.cache import Cache

MONGO_URL = os.environ["MONGO_URL"]


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        """Main Database instance of the redis cache included

        Args:
            loop (asyncio.AbstractEventLoop): the current asyncio loop running
        """
        # Initialization of the cache
        self.cache = Cache()
        # Define the main database objects ( client , database , collections )
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL, io_loop=loop)
        self.db: motor.motor_asyncio.AsyncIOMotorDatabase = self.client["stfu"]
        self.users: motor.motor_asyncio.AsyncIOMotorCollection = self.db["users"]
        self.servers: motor.motor_asyncio.AsyncIOMotorCollection = self.db["servers"]
        self.logs: motor.motor_asyncio.AsyncIOMotorCollection = self.db["logs"]
        self.gangs: motor.motor_asyncio.AsyncIOMotorCollection = self.db["gangs"]
        self.ban: motor.motor_asyncio.AsyncIOMotorCollection = self.db["ban"]

    async def add_user(self, user_id: Union[str, int]):
        """Add a user to the database
        Args:
            user_id (int): _description_
        """
        # set integers as a string
        if isinstance(user_id, int):
            user_id = str(user_id)
        document = create_user(user_id)
        # await self.cache.this_data(document)
        await self.users.insert_one(document)

    async def get_user_info(self, user_id: Union[str, int]) -> User:
        """Retrieve the User information from the database

        Args:
            id (Union[str, int]): The ID of the user info

        Returns:
            User: the user class
        """
        # set integers as a string
        if isinstance(user_id, int):
            user_id = str(user_id)
        # cache management
        if await self.cache.is_cached(user_id):
            document = await self.cache.get_data(user_id)
            return User(document, self)
        document = await self.users.find_one({"_id": user_id})
        # cache the data
        # await self.cache.this_data(document)
        return User(document, self)

    async def update_user(self, document: dict) -> None:
        """Update the document in the database

        Args:
            document (dict): The New document
        """
        _id = document["_id"]
        await self.users.replace_one({"_id": _id}, document)
        # if await self.cache.is_cached(_id):
        #    await self.cache.this_data(document)

    async def user_in_database(self, user_id: Union[str, int]) -> bool:
        """Check if the user is registered

        Args:
            user_id (Union[str, int]): the unique discord id

        Returns:
            bool: the answer
        """
        # set integers as a string
        if isinstance(user_id, int):
            user_id = str(user_id)
        # if data is cached then it mean the user is registered
        if await self.cache.is_cached(user_id):
            return True
        # Else we check if we can get any data
        return not (await self.users.find_one({"_id": user_id}) == None)


if __name__ == "__main__":

    async def main():
        loop = asyncio.get_event_loop()
        db = Database(loop)
        User = await db.get_user_info("486465465")
        print(User.to_dict())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # loop.run_until_complete(db.add_user(str(random.randint(1, 1000000))))
