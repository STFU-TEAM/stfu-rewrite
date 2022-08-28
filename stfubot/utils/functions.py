import disnake
import asyncio
import random
import requests

from typing import List, Union, TYPE_CHECKING
from discord.ext import commands

# It's for typehint
if TYPE_CHECKING:
    from stfubot.models.gameobjects.stands import Stand

from stfubot.models.gameobjects.ia import Ia
from stfubot.models.gameobjects.effects import Effect, EffectType
from stfubot.models.database.user import User

# playing one or multiple file a better version of playfile bassicly
async def play_files(
    ctx: Union[commands.Context, disnake.ApplicationCommandInteraction],
    files: List[str],
):
    """
    takes a list of url and play them
    if no voice channel is find do nothing
    """
    voice_channel = ctx.author.voice
    # check if the author is connected
    if voice_channel is not None:
        try:
            # grab the channel
            voice = await ctx.author.voice.channel.connect()
        except disnake.errors.ClientException:
            # this error mean the client already connected
            # which can happen
            # get the voicestate
            voice = ctx.me.voice.channel.voice_states.get(ctx.me.id)
        # play every file in chains
        for url in files:
            source = disnake.FFmpegPCMAudio(url)
            voice.play(source)
            # wait untill the bot is finish playing
            while voice.is_playing():
                await asyncio.sleep(0.1)
        await voice.disconnect()
    # this render the fonction callable even if the person is not connected+


# Used in UI and embeds
def sign(x: int):
    if x > 0:
        return f"(+{int(x)})"
    elif x < 0:
        return f"(-{int(x)})"
    else:
        return ""


def game(stand1: List["Stand"], stand2: List["Stand"]) -> bool:
    result = False
    for stand in stand1:
        result |= stand.is_alive()
    result2 = False
    for stand in stand2:
        result2 |= stand.is_alive()
    return result and result2


def get_stand_status(stand: "Stand") -> str:
    status = ""
    if not stand.effects:
        status = " `✔️` "
    else:
        status = ""
        unique: List[Effect] = []
        actual_effect = stand.effects
        if stand.ressistance < 1:
            actual_effect.append(Effect(EffectType.WEAKEN, 1, 0))
        if stand.current_speed < stand.start_speed:
            actual_effect.append(Effect(EffectType.SLOW, 1, 0))
        for effect in stand.effects:
            if effect.type not in [e.type for e in unique]:
                unique.append(effect)
        for effect in unique:
            status += f" {effect.emoji}"
    return status


def get_turn_special(stand: "Stand") -> str:
    turn = stand.turn_for_ability - stand.special_meter
    if turn > 0:
        return f"in {turn} turn"
    return "ready ✔️"


def win(players: List[Union[User, Ia]]) -> User:
    """Determine who won between two players

    Args:
        players (List[User]): The User who fought

    Returns:
        User: The User who won
    """
    alive_status_1 = False
    for stand in players[0].stands:
        alive_status_1 |= stand.is_alive()
    alive_status_2 = False
    for stand in players[1].stands:
        alive_status_2 |= stand.is_alive()
    if alive_status_1 and not alive_status_2:
        return players[0]
    else:
        return players[1]


# used in cooldown functions
def secondsToText(secs):
    days = secs // 86400
    hours = int((secs - days * 86400) // 3600)
    minutes = int((secs - days * 86400 - hours * 3600) // 60)
    seconds = int(secs - days * 86400 - hours * 3600 - minutes * 60)
    result = (
        ("{0} day{1}, ".format(days, "s" if days != 1 else "") if days else "")
        + ("{0} hour{1}, ".format(hours, "s" if hours != 1 else "") if hours else "")
        + (
            "{0} minute{1}, ".format(minutes, "s" if minutes != 1 else "")
            if minutes
            else ""
        )
        + (
            "{0} second{1}, ".format(seconds, "s" if seconds != 1 else "")
            if seconds
            else ""
        )
    )
    return result


def format_combat_log(translation: dict, combat_log: List[str]) -> List[disnake.Embed]:
    embeds = []
    embed = disnake.Embed(title=translation["fight"]["9"], color=disnake.Color.blue())
    for i, line in enumerate(combat_log):
        if len(embed.fields) >= 8:
            embeds.append(embed)
            embed = disnake.Embed(
                title=translation["fight"]["9"], color=disnake.Color.blue()
            )
        embed.add_field(name=line, value=f"n°{i}")
    embeds.append(embed)
    return embeds


async def wait_for(view: disnake.ui.View):
    if await view.wait():
        raise asyncio.TimeoutError


# get a drop from a list
def get_drop_from_list(stand_list: List["Stand"], number_of_drop: int = 1) -> list:
    stand_list = [stand for stand in stand_list if stand.stars != 10]
    # count the stand per star category
    nums = [1, 1, 1, 1, 1, 1]
    for i in stand_list:
        nums[i.stars - 1] += 1
    # probability pondered by the number of stand in the star category
    stars = [1, 2, 3, 4, 5, 6]
    weights = [
        0.35,
        0.3,
        0.2,
        0.1,
        0.04,
        0.01,
    ]
    star = random.choices(stars, weights=weights, k=1)[0]

    stand_list = [stand for stand in stand_list if stand.stars == star]
    # return one of the stand
    drops = random.choices(stand_list, k=number_of_drop)
    return drops


def add_to_available_storage(user: User, stand: "Stand", skip_main:bool=False):
    if len(user.stands) < 3 and not skip_main:
        user.stands.append(stand)
        return "Main stand"
    if len(user.stand_storage) < 8:
        user.stand_storage.append(stand)
        return "Stand storage"
    if len(user.pstand_storage) < 8 and user.is_donator():
        user.pstand_storage.append(stand)
        return "Premium storage"
    return False


def stand_fields(stand: "Stand", embed: disnake.Embed):
    stars = "⭐" * stand.stars + "🌟" * stand.ascension
    embed.add_field(
        name="▬▬▬`STAND`▬▬▬",
        value=f"name:`{stand.name}`\n" + f"stars:`{stars}`\n" + "    ▬▬▬▬▬▬▬▬▬",
    )
    embed.add_field(
        name="▬▬▬`STATS`▬▬▬",
        value=f"HP:`{int(stand.current_hp)}❤️`\n"
        + f"DAMAGE:`{int(stand.current_damage)}⚔️`\n"
        + f"SPEED:`{int(stand.current_speed)}💨`\n    ▬▬▬▬▬▬▬▬▬",
    )
    turn = (
        "\n"
        if stand.special_description == "None"
        else f"\nturn:`{stand.turn_for_ability}\n`"
    )
    embed.add_field(
        name="▬▬`SPECIAL`▬▬",
        value=stand.special_description + turn + "    ▬▬▬▬▬▬▬▬▬",
    )
    embed.set_image(url=f"http://storage.stfurequiem.com/Image/{stand.id}.png")
    return embed


def is_url_image(image_url: str):
    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
    try:
        r = requests.head(image_url)
        if r.headers["content-type"] in image_formats:
            return True
        return False
    except:
        return False


async def view_timeout(interaction: disnake.ApplicationCommandInteraction):
    """add an expired button to views

    Args:
        interaction (disnake.ApplicationCommandInteraction): [description]
    """
    view = disnake.ui.View()
    view.add_item(
        disnake.ui.Button(
            label=f"Expired",
            emoji="⌚",
            style=disnake.ButtonStyle.grey,
            disabled=True,
        )
    )
    try:
        await interaction.edit_original_message(view=view)
    except:
        try:
            await interaction.response.edit_message(view=view)
        except:
            pass
        pass
