import disnake
import random
import asyncio

from disnake.ext import commands, tasks

# stfu model
from stfubot.models.bot.stfubot import StfuBot

from typing import List


class Listeners(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot
        self.change_presence.start()

    @commands.Cog.listener()
    async def on_send_message_to_shard(
        self, embed: disnake.Embed, channel: disnake.TextChannel, id: str
    ):
        print("ranked shard:", shard_id, "\nrando guild id", rando_id)
        shard_id = channel.guild.shard_id
        rando_id = self.stfubot.guilds[0].id
        if shard_id == (rando_id >> 22) % self.stfubot.shard_count:
            channel = self.stfubot.get_partial_messageable(
                channel.id, type=disnake.ChannelType.text
            )
            msg = await channel.send(embed=embed)
            self.stfubot.dispatch("shard_send_message", msg, id)

    @commands.Cog.listener()
    async def on_delete_message_from_shard(self, message: disnake.Message):
        message = await self.stfubot.refresh_msg(message)
        shard_id = message.guild.shard_id
        rando_id = self.stfubot.guilds[0].id
        if shard_id == (rando_id >> 22) % self.stfubot.shard_count:
            message = await self.stfubot.refresh_msg(message)
            await message.delete()
            self.stfubot.dispatch("delete_message_from_shard_done", message.id)

    @commands.Cog.listener()
    async def on_edit_message_from_shard(
        self, embed: disnake.Embed, message: disnake.Message
    ):
        message = await self.stfubot.refresh_msg(message)
        shard_id = message.guild.shard_id
        rando_id = self.stfubot.guilds[0].id
        if shard_id == (rando_id >> 22) % self.stfubot.shard_count:
            message = await self.stfubot.refresh_msg(message)
            await message.edit(embed=embed)
            self.stfubot.dispatch("edit_message_from_shard_done", message.id)

    @commands.Cog.listener()
    async def on_edit_ui_from_shard(
        self, embed: disnake.Embed, view: disnake.ui.View, message: disnake.Message
    ):
        message = await self.stfubot.refresh_msg(message)
        shard_id = message.guild.shard_id
        rando_id = self.stfubot.guilds[0].id
        if shard_id == (rando_id >> 22) % self.stfubot.shard_count:
            message = await self.stfubot.refresh_msg(message)
            await message.edit(embed=embed, view=view)
            self.stfubot.dispatch("edit_ui_from_shard_done", message.id)

    @tasks.loop(seconds=15 * 60)
    async def change_presence(self):
        quotes = [
            "Stfurequiem but better",
            "The start of a new era",
            "what the fuck is oatmeal",
            "your adventure has just begun",
            "the jojo reference singularity will one day be reached",
            "STAN Kelian",
            "STAN Vince",
            "being keyshiwophobic >>>>",
        ]
        quote = random.choice(quotes)
        await self.stfubot.change_presence(activity=disnake.Game(quote))


def setup(stfubot: StfuBot):
    stfubot.add_cog(Listeners(stfubot))