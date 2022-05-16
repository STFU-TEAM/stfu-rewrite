import disnake
import random
import json
import datetime

# stfu model
from models.bot.stfubot import StfuBot
from models.gameobjects.stands import Stand, stand_from_dict, get_stand_from_template

# specific class import
from disnake.ext import commands


class daily(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(name="begin", description="Start your daily journey")
    async def being(self, Interaction: disnake.ApplicationCommandInteraction):
        # Check if user is registered
        if not (await self.stfubot.database.user_in_database(Interaction.author.id)):
            await self.stfubot.database.add_user(Interaction.author.id)
            User = await self.stfubot.database.get_user_info(Interaction.author.id)
            # get a 4 star as a starting stand
            starting_stands = [s for s in self.stfubot.stand_file if s["stars"] == 4]
            stand = get_stand_from_template(random.choice(starting_stands))
            # add the stand and update
            embed = disnake.Embed(
                title="Welcome !",
                description="`Begin your journey ! here is your staring stand`",
                color=disnake.Colour.blue(),
            )
            embed.set_image(url=f"http://storage.stfurequiem.com/Image/{stand.id}.png")
            embed.add_field(
                name="▬▬▬`STAND`▬▬▬",
                value=f"name:`{stand.name}`\n" + "stars:`⭐⭐⭐⭐`\n" + "    ▬▬▬▬▬▬▬▬▬",
            )
            embed.add_field(
                name="▬▬▬`STATS`▬▬▬",
                value=f"HP:`{stand.current_hp}❤️`\n"
                + f"DAMAGE:`{stand.current_damage}⚔️`\n"
                + f"SPEED:`{stand.current_speed}💨`\n    ▬▬▬▬▬▬▬▬▬",
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
            embed.add_field(
                name="▬▬`Quick Start`▬▬",
                value="Welcome to the stfubot, it's a full / command bot use \n"
                + "/crusade or /job to start earning money \n"
                + "then check out /tower for opertunity to gain stands\n"
                + "good luck\n"
                + "    ▬▬▬▬▬▬▬▬▬",
            )
            User.stands.append(stand)
            User.last_adventure = datetime.datetime.now()
            await User.update()
            await Interaction.send(embed=embed)
        else:
            embed = disnake.Embed(title="Sorry but...")
            embed.add_field(
                name="▬▬▬START▬▬▬",
                value="It seems you alread started your journey\n" + "    ▬▬▬▬▬▬▬▬▬",
            )
            await Interaction.send(embed=embed)


def setup(client: StfuBot):
    client.add_cog(daily(client))