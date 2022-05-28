import io
import disnake

from PIL import Image, ImageDraw


async def get_part_3_tower_image(user: disnake.User, stage: int) -> disnake.File:
    image = Image.open("stfubot/data/image/towertemplate_part3.png")
    # create object for drawing
    AVATAR_SIZE = 128

    # get both avatars
    avatar1 = user.avatar.with_format("jpg").with_size(AVATAR_SIZE)
    buffer_avatar1 = io.BytesIO(await avatar1.read())
    avatar_image1 = Image.open(buffer_avatar1)
    # create a 200s*200 round avatar
    avatar_image1 = avatar_image1.resize((150, 150))
    # make the image a circle

    circle_image = Image.new("L", (150, 150))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, 150, 150), fill=255)
    # stage
    if stage == 1:
        pos = (177, 10)
    if stage == 2:
        pos = (151, 65)
    if stage == 3:
        pos = (86, 60)
    if stage == 4:
        pos = (57, 156)
    if stage == 5:
        pos = (124, 178)
    if stage == 6:
        pos = (215, 225)
    pos = list(pos)
    pos[0] = int(3.5 * pos[0])
    pos[1] = int(3.5 * pos[1])
    # paste the result
    image.paste(avatar_image1, pos, circle_image)
    # create buffer
    buffer_output = io.BytesIO()
    # save PNG in buffer
    image.save(buffer_output, format="PNG")
    # move to beginning of buffer so `send()` it will read from beginning
    buffer_output.seek(0)
    file = disnake.File(buffer_output, "myimage.png")
    return file


async def get_tower_victory_image(user: disnake.User) -> disnake.File:
    image = Image.open("stfubot/data/image/finalbattleview.png")
    # create object for drawing
    AVATAR_SIZE = 128
    # get both avatars
    avatar1 = user.avatar.with_format("jpg").with_size(AVATAR_SIZE)
    buffer_avatar1 = io.BytesIO(await avatar1.read())
    avatar_image1 = Image.open(buffer_avatar1)
    # create a 128*128 round avatar
    avatar_image1 = avatar_image1.resize((AVATAR_SIZE, AVATAR_SIZE))
    # make the image a circle

    circle_image = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
    # paste the result
    image.paste(avatar_image1, (125, 30), circle_image)
    # create buffer
    buffer_output = io.BytesIO()
    # save PNG in buffer
    image.save(buffer_output, format="PNG")
    # move to beginning of buffer so `send()` it will read from beginning
    buffer_output.seek(0)
    file = disnake.File(buffer_output, "myimage.png")
    return file


# easier to retrive programmatically
tower_images = {"1": get_part_3_tower_image}

# this returns a image used for fight
async def get_win_image(user1: disnake.User) -> disnake.File:
    image = Image.open("stfubot/data/image/winner.png")
    # create object for drawing
    AVATAR_SIZE = 128
    # get both avatars
    avatar1 = user1.avatar.with_format("jpg").with_size(AVATAR_SIZE)
    buffer_avatar1 = io.BytesIO(await avatar1.read())
    avatar_image1 = Image.open(buffer_avatar1)
    # create a 128*128 round avatar
    avatar_image1 = avatar_image1.resize((AVATAR_SIZE, AVATAR_SIZE))
    # make the image a circle

    circle_image = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
    # paste the result
    image.paste(avatar_image1, (135, 45), circle_image)
    # create buffer
    buffer_output = io.BytesIO()
    # save PNG in buffer
    image.save(buffer_output, format="PNG")
    # move to beginning of buffer so `send()` it will read from beginning
    buffer_output.seek(0)
    file = disnake.File(buffer_output, "image.png")
    return file


# this returns a image used for fight
async def get_fight_image(user1: disnake.User, user2: disnake.User) -> disnake.File:
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
