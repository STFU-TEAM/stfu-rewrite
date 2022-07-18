import disnake
import time
from datetime import datetime

from typing import List, TYPE_CHECKING, Optional
from math import inf

# It's for typehint
if TYPE_CHECKING:
    from stfubot.models.bot.stfubot import StfuBot


class Queue:
    def __init__(self, stfubot):
        self.stfubot: "StfuBot" = stfubot
        self.queue = []
        self.last_reset = -inf
        self.reason: List[str] = []
        self.request_done: List[dict] = []

    async def matchIsFound(self, Interaction: disnake.ApplicationCommandInteraction):
        request = await self.formatMatch(Interaction)
        return not await self.stfubot.database.cache.match_found(request)

    async def join(self, Interaction: disnake.ApplicationCommandInteraction):
        request = await self.formatMatch(Interaction)
        await self.stfubot.database.cache.join_ranked_queu(request)

    async def leave(
        self,
        Interaction: Optional[disnake.ApplicationCommandInteraction],
        reason: str,
        manual: list = [],
    ):
        if Interaction != None:
            rq = await self.formatMatch(Interaction)
        else:
            rq = manual
        if reason == "leave":
            await self.stfubot.database.cache.leave_match_macking(rq)
            await self.stfubot.database.cache.leave_ranked_queu(rq)
        self.request_done.append(rq)
        self.reason.append(reason)

    async def get_reason(self, Interaction: disnake.ApplicationCommandInteraction):
        rq = await self.formatMatch(Interaction)
        t = time.time()
        while not await self.formatMatch(Interaction) in self.request_done:
            # kick the player at 5 min
            if time.time() - t > 5 * 60:
                return "kick"
        index = self.request_done.index(rq)
        reason = self.reason.pop(index)
        self.request_done.remove(rq)
        return reason

    def reset_queu(self, time: float) -> None:
        """reset the time stamp"""
        self.last_reset = time
        return

    async def formatMatch(
        self, Interaction: disnake.ApplicationCommandInteraction
    ) -> dict:
        """get the request from an interaction
        Args:
            Interaction (disnake.ApplicationCommandInteraction): the slash command interaction

        Returns:
            dict: formated request
        """
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        request = {
            "user_id": str(Interaction.author.id),
            "channel_id": Interaction.channel.id,
            "elo": user.global_elo,
            "priority_level": 1 + user.is_donator(),
        }
        return request
