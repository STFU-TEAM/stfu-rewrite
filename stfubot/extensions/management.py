import disnake
import random
import asyncio

# utils
from utils.decorators import database_check
from utils.functions import play_files, sign

# stfu model
from models.bot.stfubot import StfuBot
from models.gameobjects.stands import Stand, stand_from_dict, get_stand_from_template
from globals.emojis import CustomEmoji

# specific class import
from disnake.ext import commands

# ui
from ui.StandSelect import StandSelectDropdown


class management(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(
        name="stand", description="show one of your main stand stats."
    )
    @database_check()
    async def stand(self, Interaction: disnake.ApplicationCommandInteraction):
        User = await self.stfubot.database.get_user_info(Interaction.author.id)
        if User.stands == []:
            embed = disnake.Embed(
                title="Error",
                description="You don't have any stand in your main stand.",
                color=disnake.Colour.blue(),
            )
            embed.set_thumbnail(
                url="https://storage.stfurequiem.com/randomAsset/avatar.png"
            )
            await Interaction.send(embed=embed)
        else:
            # make an embed
            embed = disnake.Embed(
                title="Which stand would you like to select ?",
                color=disnake.Colour.blue(),
            )
            embed.set_image(url="https://storage.stfurequiem.com/Image/arrow.gif")

            view = StandSelectDropdown(Interaction, User.stands)
            await Interaction.send(embed=embed, view=view)
            if await view.wait():
                raise asyncio.TimeoutError
            index = view.value
            # get the stand
            # get the stand
            stand: Stand = User.stands[index]
            # create a dict with everything we need
            emojis = [
                "🔪",
                str(CustomEmoji.ARROW),
                str(CustomEmoji.ITEM_REQUIEM),
                "🐞",
            ]
            items = [i for i in stand.items]
            stars = "⭐" * stand.stars + "🌟" * stand.ascension

            # shinies
            if stand.ascension + stand.stars > 7:
                stars = "🌟" * stand.stars + "🌠" * stand.ascension
                # per case embed and name
                if stand.id == 109:
                    stand.name = "ボームヴンレクイエム"
                    rand = 1
                elif stand.id == 84:
                    stand.name = "Alternate Universe Gold Experience Requiem"
                    rand = 5
                elif stand.id == 54:
                    stand.name = "Super Duper Cute and Angy Stray Cat"
                    rand = 2
                elif stand.id == 86:
                    stand.name = "受け継がれた魂 Stone Free"
                    rand = 1
                rand = random.randint(1, rand)
                url = f"https://storage.stfurequiem.com/Shiny/{stand.id}_{rand}.gif"
                play = f"data/sound/{stand.id}_1.mp3"
            # evolved 4 star
            elif stand.ascension > 1 and stand.stars == 4 and stand.id <= 85:
                url = f"https://storage.stfurequiem.com/Image/{stand.id}.gif"
                play = ""
            # 5+ star
            elif stand.stars >= 5:
                url = f"https://storage.stfurequiem.com/Image/{stand.id}.gif"
                play = f"data/sound/{stand.id}.mp3"
            else:
                url = f"https://storage.stfurequiem.com/Image/{stand.id}.png"
                play = ""
            embed = disnake.Embed(
                title=f"`{stand.name}`",
                description=f"`{stars}`",
                color=disnake.Colour.blue(),
            )
            bonus_hp = stand.current_hp - stand.base_hp
            bonus_damage = stand.current_damage - stand.base_damage
            bonus_speed = stand.current_speed - stand.base_speed
            bonus_critical = stand.current_critical - stand.base_critical
            embed.set_image(url=url)
            embed.add_field(
                name="▬▬▬`STATS`▬▬▬",
                value=f"HP:`{stand.base_hp}{sign(bonus_hp)}❤️`\n"
                + f"DAMAGE:`{stand.base_damage}{sign(bonus_damage)}⚔️`\n"
                + f"SPEED:`{stand.base_speed}{sign(bonus_speed)}💨`\n"
                + f"CRITICAL RATE:`{stand.base_critical}{sign(bonus_critical)}`\n    ▬▬▬▬▬▬▬▬▬",
            )
            if not (len(items)) == 0:
                item = ""
                for i in items:
                    item += f"{i.emoji}:{i.name}\n"
                item += "    ▬▬▬▬▬▬▬▬▬\n"
                embed.add_field(name="▬▬▬`ITEMS`▬▬▬", value=item)
            turn = (
                "\n"
                if stand.special_description == "None"
                else f"\nturn:`{stand.turn_for_ability}`"
            )
            embed.add_field(
                name="▬▬`SPECIAL`▬▬",
                value=stand.special_description + turn + "\n    ▬▬▬▬▬▬▬▬▬",
            )

            await Interaction.channel.send(embed=embed)
            if play:
                await play_files(Interaction, [play])


def setup(client: StfuBot):
    client.add_cog(management(client))