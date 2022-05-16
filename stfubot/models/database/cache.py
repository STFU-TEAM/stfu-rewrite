import aioredis
import os
import pickle

REDIS_URL = os.environ["REDIS_URL"]


class Cache:
    """Connection to the redis database"""

    def __init__(self):
        self.redis_pool = aioredis.ConnectionPool.from_url(url=REDIS_URL)

    async def this_data(self, data: dict, time: int = 10, key: str = None) -> None:
        """cache the dict pickle first for good measure,
            default key is the _id key in the data
        Args:
            data (dict): any data
            time (int): time store the data for (in min)
        """
        # get a connection to redis
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        if key is None:
            key = data["_id"]
        # store the data
        await redis_con.execute_command("set", key, pickle.dumps(data))
        # set a time limit before the data is dumped
        await redis_con.expire(key, 60 * time)
        await redis_con.close()

    async def get_data(self, key: str) -> dict:
        """Retrive an existing cached data

        Args:
            key (str): default is data["_id"]

        Returns:
            dict: the data you asked for
        """
        # get a connection to redis
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # get the data from the cache
        data = await redis_con.execute_command("get", key)
        # unpickle the data
        data = pickle.loads(data)
        # return the data
        await redis_con.close()
        return data

    async def is_cached(self, key: str) -> bool:
        """[ return if the key exist
        Args:
            key (str): default is data["_id"]

        Returns:
            bool: [Descriptive]
        """
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # return the bool
        test = bool(await redis_con.exists(key))
        await redis_con.close()
        return test

    async def delete(self, key: str) -> None:
        """delete a key

        Args:
            key (str): default is data["_id"]
        """
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # delete the value
        await redis_con.delete(key)
        await redis_con.close()
