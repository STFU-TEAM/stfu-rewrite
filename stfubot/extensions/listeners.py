import disnake

from disnake.ext import commands, tasks

# stfu model
from stfubot.models.bot.stfubot import StfuBot

from typing import List


class Listeners(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.Cog.listener()
    async def on_send_message_to_shard(
        self, embed: disnake.Embed, channel: disnake.TextChannel, id: str
    ):
        shard_id = channel.guild.shard_id
        this_shard_id = self.stfubot.shard_id
        print(f"received:{id} send_message from shard:{shard_id}|SHARD:{this_shard_id}")
        if shard_id == this_shard_id:
            channel = self.stfubot.get_partial_messageable(
                channel.id, type=disnake.ChannelType.text
            )
            msg = await channel.send(embed=embed)
            self.stfubot.dispatch("shard_send_message", msg, id)

    @commands.Cog.listener()
    async def on_delete_message_from_shard(self, message: disnake.Message):
        message = await self.stfubot.refresh_msg(message)
        shard_id = message.guild.shard_id
        this_shard_id = self.stfubot.shard_id
        if shard_id == this_shard_id:
            message = await self.stfubot.refresh_msg(message)
            await message.delete()
            self.stfubot.dispatch("delete_message_from_shard_done", message.id)

    @commands.Cog.listener()
    async def on_edit_message_from_shard(
        self, embed: disnake.Embed, message: disnake.Message
    ):
        message = await self.stfubot.refresh_msg(message)
        shard_id = message.guild.shard_id
        this_shard_id = self.stfubot.shard_id
        if shard_id == this_shard_id:
            message = await self.stfubot.refresh_msg(message)
            await message.edit(embed=embed)
            self.stfubot.dispatch("edit_message_from_shard_done", message.id)

    @commands.Cog.listener()
    async def on_edit_ui_from_shard(
        self, embed: disnake.Embed, view: disnake.ui.View, message: disnake.Message
    ):
        message = await self.stfubot.refresh_msg(message)
        shard_id = message.guild.shard_id
        this_shard_id = self.stfubot.shard_id
        if shard_id == this_shard_id:
            message = await self.stfubot.refresh_msg(message)
            await message.edit(embed=embed, view=view)
            self.stfubot.dispatch("edit_ui_from_shard_done", message.id)


def setup(stfubot: StfuBot):
    stfubot.add_cog(Listeners(stfubot))
