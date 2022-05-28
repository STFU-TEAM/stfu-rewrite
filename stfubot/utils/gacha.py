import disnake

from typing import List

from stfubot.globals.emojis import CustomEmoji
from stfubot.ui.gacha.stand_select import Stand_Select
from stfubot.ui.confirmation import Confirm
from stfubot.utils.functions import (
    get_drop_from_list,
    add_to_available_storage,
    stand_fields,
)

from models.database.user import User
from models.gameobjects.stands import Stand


async def gacha(
    Interaction: disnake.ApplicationCommandInteraction,
    translation: dict,
    user: User,
    stand_list: List[Stand],
):
    drop: Stand = get_drop_from_list(stand_list)

    stars = "⭐" * drop.stars
    add_to_available_storage(user, drop)
    msg = add_to_available_storage(drop)
    if msg:
        embed = disnake.Embed(title=translation["gacha"]["1"].format(msg))
        embed.set_thumbnail(
            url="https://vignette.wikia.nocookie.net/jjba/images/9/9f/Arrow_anime.png/revision/latest?cb=20190614222010"
        )
        embed = stand_fields(drop, embed)
        await Interaction.channel.send(embed=embed)
        return True
    return False
