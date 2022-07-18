import json
import asyncio
import disnake
import traceback

from logging import warning
from disnake.ext import commands
from typing import List

from datetime import datetime

from stfubot.models.database.maindatabase import Database
from stfubot.models.api.api_requests import StfuApi
from stfubot.models.database.queue import Queue

from stfubot.utils.fight_logic import fight_instance


class StfuBot(commands.AutoShardedInteractionBot):
    """AutoShardedBot with added methods and caviats"""

    def __init__(self, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()):
        super().__init__(
            max_messages=1000000,
            loop=loop,
            sync_commands=True,
            sync_commands_debug=True,
        )
        self.developers = [
            242367586233352193,  # EIRBLAST
            112866272106012672,  # Arkkos
            289413979644755970,  # Kelian
        ]
        self.testers = self.developers + [
            248492672979959809,  # EIRBOT
            435082104381112340,  # Allways
        ]
        self.give_stand = self.developers + [
            704961055662538833,  # Keyshiwo
            348342650853785602,  # Greg
            476057912532533273,  # Pickle
            435082104381112340,  # Allways
        ]
        with open(f"stfubot/lang/en_US.json", "r", encoding="utf8") as item:
            self.en_translation = json.load(item)
        # the database model
        self.database: Database = Database(loop)
        # the api model
        self.api: StfuApi = StfuApi()
        # ranked queue
        self.ranked_queue = Queue(self)
        with open("stfubot/data/static/stand_template.json", "r") as item:
            self.stand_file: dict = json.load(item)["stand"]
        self.avatar_url: str = "https://storage.stfurequiem.com/randomAsset/avatar.png"
        # The Matchmaking status
        self.MatchMaking_Is_Running: bool = False
        # ranked tasks so we can cancel them manually
        self.RankedTask: List[asyncio.Task] = []

    def startMatchmaking(self):
        """start the matchmaking listener"""
        if self.MatchMaking_Is_Running:
            print("matchmaking already started")
            return
        self.MatchMaking = self.loop.create_task(self.matchMacking())
        print("Started the matchmaking")

    async def refresh_msg(self, msg: disnake.Message) -> disnake.Message:
        """this fonction just refresh a message

        Args:
            msg (discord.Message): the message to re-cached
        Returns:
            discord.Message: the same message but cached
        """
        old_msg = msg
        # wrap in try so it does not return None
        try:
            channel_1 = await self.fetch_channel(msg.channel.id)
        except disnake.errors.NotFound:
            channel_1 = self.get_channel(msg.channel.id)
            if channel_1 == None:
                msg = old_msg
        try:
            msg = await channel_1.fetch_message(msg.id)
        except disnake.errors.NotFound:
            msg: disnake.PartialMessage = channel_1.get_partial_message(msg.id)
            msg = await msg.fetch()
            if msg == None:
                msg = old_msg
        else:
            # If we get None we return the old message
            msg = msg if msg != None else old_msg
        return msg

    async def matchMacking(self):
        """this listen for new match and create them"""
        # wait until the bot started
        await self.wait_until_ready()
        # We do not lunch the matchmaking if it is alr running
        self.MatchMaking_Is_Running = True
        # loop the matchmaking
        while True:  # loop forever hopefully
            try:
                await asyncio.sleep(1)
                matches = await self.database.cache.get_matches()
                for match in matches:
                    users = []
                    channels = []

                    # try to retrieve the classes
                    try:
                        # get the relevant things
                        users.append(
                            (
                                await self.getch_user(
                                    int(match["user_ids"][0]), strict=True
                                )
                            )
                        )
                        users.append(
                            (
                                await self.getch_user(
                                    int(match["user_ids"][1]), strict=True
                                )
                            )
                        )
                        channels.append(
                            (await self.fetch_channel(match["channel_ids"][0]))
                        )
                        channels.append(
                            (await self.fetch_channel(match["channel_ids"][1]))
                        )
                    except:
                        # kick the player if an error occurs
                        user_1 = await self.database.get_user_info(match["user_ids"][0])
                        user_2 = await self.database.get_user_info(match["user_ids"][1])
                        # create the request
                        request1 = {
                            "user_id": match["user_ids"][0],
                            "channel_id": match["channel_ids"][0],
                            "elo": user_1.global_elo,
                            "priority_level": 1 + user_1.is_donator(),
                        }
                        request2 = {
                            "user_id": match["user_ids"][1],
                            "channel_id": match["channel_ids"][1],
                            "elo": user_2.global_elo,
                            "priority_level": 1 + user_2.is_donator(),
                        }
                        # kick the players
                        await self.ranked_queue.leave(None, "kick", request1)
                        await self.ranked_queue.leave(None, "kick", request2)
                        # remove the match
                        await self.database.cache.remove_matches(match)
                    # kick the player if an error arrive
                    user_1 = await self.database.get_user_info(match["user_ids"][0])
                    user_1.discord = users[0]
                    user_2 = await self.database.get_user_info(match["user_ids"][1])
                    user_2.discord = users[1]
                    # create the request
                    request1 = {
                        "user_id": match["user_ids"][0],
                        "channel_id": match["channel_ids"][0],
                        "elo": user_1.global_elo,
                        "priority_level": 1 + user_1.is_donator(),
                    }
                    request2 = {
                        "user_id": match["user_ids"][1],
                        "channel_id": match["channel_ids"][1],
                        "elo": user_2.global_elo,
                        "priority_level": 1 + user_2.is_donator(),
                    }
                    # create Ranked task
                    users = [user_1, user_2]
                    print(users)
                    print(channels)
                    self.RankedTask.append(
                        self.loop.create_task(
                            fight_instance(
                                users,
                                channels,
                                self.en_translation,
                                fight_id=match["match_id"],
                                client=self,
                            )
                        )
                    )
                    # kick the players
                    await self.ranked_queue.leave(None, "match", request1)
                    await self.ranked_queue.leave(None, "match", request2)
                    await self.database.cache.remove_matches(match)
            except Exception as error:
                error_traceback = "".join(
                    traceback.format_exception(
                        etype=type(error), value=error, tb=error.__traceback__
                    )
                )
                # log error
                await self.database.add_log(
                    datetime.now(),
                    "matchmaking",
                    str(type(error)),
                    str(error_traceback),
                )
                warning("error in matchmaking")
            # sleep to so the loop keep going
            await asyncio.sleep(0.1)
        # cancel the task
        return
