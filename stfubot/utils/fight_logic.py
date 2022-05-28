import disnake
import random
import asyncio
import json

from typing import List, Union, Tuple

# ui
from stfubot.ui.fight.fight_ui import FightUi
from stfubot.ui.place_holder import PlaceHolder

# utils
from stfubot.utils.functions import (
    game,
    get_stand_status,
    get_turn_special,
    win,
)

# stfu model
from stfubot.models.gameobjects.stands import Stand


from stfubot.models.gameobjects.ia import Ia
from stfubot.models.database.user import User


async def fight_instance(
    fighters: List[Union[User, Ia]],
    channels: List[disnake.TextChannel],
    translation: dict,
    ranked: bool = True,
) -> Tuple[Union[User, Ia], List[str]]:
    # Message used for status and attacks
    embed = disnake.Embed(
        title=f"{fighters[0].discord.name} vs {fighters[1].discord.name}",
        color=disnake.Color.blue(),
    )

    if ranked:
        with open(f"stfubot/lang/en.json", "r", encoding="utf8") as item:
            translation = json.load(item)
    messages_1 = await send_all(embed, channels)
    # Message used to display specials
    embed = disnake.Embed(colour=disnake.Colour.blue())
    embed.set_image(url="https://c.tenor.com/B_J3xedKvA8AAAAC/jojo-anime.gif")
    messages_2 = await send_all(embed, channels)
    # Set the message for the player
    fighters[0].message = messages_1[0]
    fighters[1].message = messages_1[1]
    # Set up some fight Variable
    tusk_act_4 = False
    king_crimson = False
    combat_log = []
    turn = 0
    # Determine who start fist
    start_1 = sum([i.current_speed for i in fighters[0].stands])
    start_2 = sum([i.current_speed for i in fighters[1].stands])
    players = [fighters[0], fighters[1]]
    if start_2 > start_1:
        players: List[Union[User, Ia]] = [fighters[1], fighters[0]]
    if start_2 == start_1:
        random.shuffle(players)
    # We give a little help if you start second
    for stand in players[1].stands:
        stand.special_meter += 1
    # Game loop
    while game(players[0].stands, players[1].stands):
        # We get with player must play based of parity looks hard but it is not
        # Look in idle what n % 2 does if you need to
        player = players[turn % 2]
        watcher = players[(turn + 1) % 2]
        for stand in player.stands:
            # We check again to make sure the game as not ended
            if not game(players[0].stands, players[1].stands):
                break
            # First we check for attacks then we check for special
            # Basic Attacks
            if stand.is_alive() and not (stand.is_stunned()):
                # embed stuff
                embed = disnake.Embed(
                    title=translation["fight"]["3"].format(player.discord.name),
                    description=translation["fight"]["4"].format(turn + 1),
                    color=disnake.Color.blue(),
                )
                status = get_stand_status(stand)
                turn_ = get_turn_special(stand)
                embed.add_field(
                    name=translation["fight"]["5"].format(stand.name),
                    value=f"`HP`:`{int(stand.current_hp)}/{int(stand.start_hp)}❤️`\n`STATUS`:{status}\n`Ability`:{turn_}\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
                    inline=False,
                )
                for ennemy_stand in watcher.stands:
                    if ennemy_stand.is_alive():
                        etoile = ennemy_stand.stars * "⭐" + "🌟" * ennemy_stand.ascension
                        status = get_stand_status(ennemy_stand)
                        spe = get_turn_special(ennemy_stand)
                        embed.add_field(
                            name=f"`『{ennemy_stand.name}』`\n`{etoile}`",
                            value=f"HP:`{int(ennemy_stand.current_hp)}/{int(ennemy_stand.start_hp)}❤️`\n`STATUS`:{status}\n`Ability`:{spe}\n    ▬▬▬▬▬▬▬▬▬",
                            inline=True,
                        )
                if player.is_human:
                    view = FightUi(
                        player.message, player.discord, watcher.stands, player.stands
                    )
                    # still embed things
                    if ranked:
                        await watcher.message.edit(embed=embed, view=PlaceHolder())
                        await player.message.edit(embed=embed, view=view)
                    else:
                        await player.message.edit(embed=embed, view=view)
                    if await view.wait():
                        raise asyncio.TimeoutError

                    await view.interaction.response.edit_message(
                        embed=embed, view=PlaceHolder()
                    )
                    if view.value == "ff":
                        for i in player.stands:
                            i.current_hp = 0
                        break
                    stand_index = view.value
                    targeted_stand: Stand = watcher.stands[stand_index]
                else:
                    await asyncio.sleep(1)
                    targeted_stand: Stand = player.choice(watcher.stands)
                data = stand.attack(targeted_stand)
                info_message = ""
                if data["Dodged"]:
                    info_message = translation["fight"]["6"].format(
                        targeted_stand.name, stand.name
                    )
                elif data["critical"]:
                    info_message = translation["fight"]["7"].format(
                        targeted_stand.name, data["damage"]
                    )
                else:
                    info_message = translation["fight"]["8"].format(
                        targeted_stand.name, data["damage"]
                    )
                combat_log.append(
                    translation["fight"]["4"].format(turn + 1) + ", " + info_message
                )
                embed = disnake.Embed(title=info_message, color=disnake.Color.blue())
                embed.set_image(
                    url=f"https://storage.stfurequiem.com/Image/{stand.id}.png"
                )
                await edit(messages_2, embed)
            try:
                # Special
                if stand.is_alive() and not (stand.is_stunned()) and stand.as_special():
                    await asyncio.sleep(1)
                    # actual special ability
                    payload, message = stand.special(player.stands, watcher.stands)
                    combat_log.append(
                        translation["fight"]["4"].format(turn + 1) + ", " + message
                    )
                    embed = disnake.Embed(title=message, color=disnake.Color.blue())
                    embed.set_image(
                        url=f"https://storage.stfurequiem.com/special/{stand.id}.gif"
                    )
                    # They payload now effect the fights
                    tusk_act_4 |= payload["tusk_act_4"]
                    king_crimson |= payload["king_crimson"]
                    # edit the second embed
                    await edit(messages_2, embed)
                    await asyncio.sleep(1.5)
            except:
                pass
            # item special
            if stand.is_alive():
                for item in stand.items:
                    if item.as_special():
                        await asyncio.sleep(0.5)
                        message = item.special(stand, player.stands, watcher.stands)

                        combat_log.append(
                            translation["fight"]["4"].format(turn + 1) + ", " + message
                        )
                        embed = disnake.Embed(title=message, color=disnake.Color.blue())
                        embed.set_image(
                            url=f"https://storage.stfurequiem.com/item_special/{item.id}.gif"
                        )
                        await edit(messages_2, embed)
                        await asyncio.sleep(0.5)

        # action done after the round
        for stand in player.stands + watcher.stands:
            stand.end_turn()
        turn_amount = 1
        if king_crimson:
            # We set this to 2 so we don't change parity
            # Effectivly skipping a turn
            turn_amount = 2
            # Disable the effect afterward
            king_crimson = False
        turn += turn_amount
    await delete_all(messages_1)
    await delete_all(messages_2)
    return win(players), combat_log


async def edit(messages: List[disnake.Message], embed: disnake.Embed) -> None:
    """edit all embed

    Args:
        messages (List[disnake.Message]): messages to edit
        embed (disnake.Embed): embed to edit
    """
    if messages[0] == messages[1]:
        await messages[0].edit(embed=embed)
        return
    for message in messages:
        await message.edit(embed=embed)


async def send_all(
    embed: disnake.Embed, channels: List[disnake.TextChannel]
) -> List[disnake.Message]:
    """send embed to all the channels

    Args:
        embed (disnake.Embed): the embed that need to be sent
        channels (List[disnake.TextChannel]): channels that embed need to be sent to

    Returns:
        List[disnake.Message]: The messages
    """
    if channels[0] == channels[1]:
        msg = await channels[0].send(embed=embed)
        return msg, msg
    return [await channel.send(embed=embed) for channel in channels]


async def delete_all(messages: List[disnake.Message]) -> None:
    """delete all messages

    Args:
        messages (List[disnake.Message]): messages to delete
    """
    if messages[0] == messages[1]:
        await messages[0].delete()
        return
    for message in messages:
        await message.delete()