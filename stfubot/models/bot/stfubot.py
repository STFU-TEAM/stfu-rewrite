import json
import asyncio
import disnake

from disnake.ext import commands

from stfubot.models.database.maindatabase import Database
from stfubot.models.api.api_requests import StfuApi


class StfuBot(commands.AutoShardedInteractionBot):
    """AutoShardedBot with added methods and caviats"""

    def __init__(self, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()):
        super().__init__(
            max_messages=100000,
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

        self.database: Database = Database(loop)
        self.api: StfuApi = StfuApi()
        with open("stfubot/data/static/stand_template.json", "r") as item:
            self.stand_file: dict = json.load(item)["stand"]
        self.avatar_url = "https://storage.stfurequiem.com/randomAsset/avatar.png"
