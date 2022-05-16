import disnake
import asyncio
import io

from PIL import Image, ImageDraw
from typing import List, Union, TYPE_CHECKING
from discord.ext import commands

# It's for typehint
if TYPE_CHECKING:
    from gameobjects.stands import Stand

from gameobjects.effects import Effect, EffectType

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


# this returns a image used for fight
async def get_fight_image(
    user1: disnake.User, user2: disnake.User, client: disnake.Client
) -> disnake.File:
    image = Image.open("stfubot/data/image/template.png")
    # create object for drawing
    AVATAR_SIZE = 128
    # get both avatars
    avatar1 = user1.avatar.with_format("jpg").with_size(AVATAR_SIZE)
    avatar2 = user2.avatar.with_format("jpg").with_size(AVATAR_SIZE)
    buffer_avatar1 = io.BytesIO(await avatar1.read())
    buffer_avatar2 = io.BytesIO(await avatar2.read())
    avatar_image1 = Image.open(buffer_avatar1)
    avatar_image2 = Image.open(buffer_avatar2)
    # create a 128*128 round avatar
    avatar_image1 = avatar_image1.resize((AVATAR_SIZE, AVATAR_SIZE))
    avatar_image2 = avatar_image2.resize((AVATAR_SIZE, AVATAR_SIZE))
    # make the image a circle

    circle_image = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
    # paste the result
    image.paste(avatar_image1, (20, 35), circle_image)
    image.paste(avatar_image2, (250, 35), circle_image)
    # create buffer
    buffer_output = io.BytesIO()
    # save PNG in buffer
    image.save(buffer_output, format="PNG")
    # move to beginning of buffer so `send()` it will read from beginning
    buffer_output.seek(0)
    # give the file
    file = disnake.File(buffer_output, "image.png")
    return file


def get_stand_status(stand: "Stand") -> str:
    status = ""
    if not stand.effects:
        status = " `✔️` "
    else:
        status = ""
        unique: List[Effect] = []
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
