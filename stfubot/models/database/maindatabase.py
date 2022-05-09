import motor.motor_asyncio
import asyncio

from typing import List, Union

from user import User, create_user

URL = ""


class Database:

    def __init__(self, loop: asyncio.AbstractEventLoop):
        """Main Database instance of the redis cache included

        Args:
            loop (asyncio.AbstractEventLoop): the current asyncio loop running
        """

        # Define the main database objects ( client , database , collections )
        self.client = motor.motor_asyncio.AsyncIOMotorClient(URL, io_loop=loop)
        self.db: motor.motor_asyncio.AsyncIOMotorDatabase = self.client["stfu"]
        self.users: motor.motor_asyncio.AsyncIOMotorCollection = self.db[
            "users"]
        self.servers: motor.motor_asyncio.AsyncIOMotorCollection = self.db[
            "servers"]
        self.logs: motor.motor_asyncio.AsyncIOMotorCollection = self.db["logs"]
        self.gangs: motor.motor_asyncio.AsyncIOMotorCollection = self.db[
            "gangs"]
        self.ban: motor.motor_asyncio.AsyncIOMotorCollection = self.db["ban"]

    async def add_user(self, user_id: int):
        document = create_user(user_id)
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
        document = await self.users.find_one({"_id": user_id})
        return User(document, self)

    async def update_user(self, document: dict) -> None:
        """Update the document in the database

        Args:
            document (dict): The New document
        """
        _id = document["_id"]
        await self.users.replace_one({"_id": _id}, document)


async def main():
    loop = asyncio.get_event_loop()
    db = Database(loop)
    await db.add_user("242367586233352193")
    User = await db.get_user_info("242367586233352193")
    await User.update()
    print(User.id)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# loop.run_until_complete(db.add_user(str(random.randint(1, 1000000))))
