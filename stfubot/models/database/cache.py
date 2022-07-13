import aioredis
import os
import pickle
import json

from typing import List

REDIS_URL = os.environ["REDIS_URL"]


class Cache:
    """Connection to the redis database"""

    def __init__(self):
        self.redis_pool = aioredis.ConnectionPool.from_url(url=REDIS_URL)
        self.ranked_key = "ranked_request"

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

    # ranked
    async def join_ranked_queu(self, request: dict) -> None:
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # serialize with json
        data = json.dumps(request)
        # add to the queu
        await redis_con.execute_command("RPUSH", self.ranked_key, data)

    async def leave_ranked_queu(self, request: dict) -> None:
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # serialize with json
        data = json.dumps(request)
        # remove user
        await redis_con.execute_command("LREM", self.ranked_key, -1, data)

    async def len_ranked_queu(self) -> int:
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # return the lenght
        return await redis_con.execute_command("LLEN", self.ranked_key) - 1

    async def match_found(self, request: dict) -> bool:
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # serialize with json
        data = json.dumps(request)
        return bool(await redis_con.execute_command("LPOS", self.ranked_key, data))

    async def get_matches(self) -> List[dict]:
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # serialize with json
        matches = await redis_con.execute_command("LRANGE", "matches_request", 1, -1)
        json_matches = list(map(json.loads, matches))
        return json_matches

    async def remove_matches(self, match) -> None:
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # serialize with json
        data = json.dumps(match)
        await redis_con.execute_command("LREM", "matches_request", -1, data)

    async def leave_match_macking(self, rq: dict) -> None:
        # get a connection
        redis_con = aioredis.Redis(connection_pool=self.redis_pool)
        # serialize with json
        data = json.dumps(rq)
        await redis_con.execute_command("LPUSH", "left_request", data)

    async def close(self):
        self.redis_pool.disconnect()
