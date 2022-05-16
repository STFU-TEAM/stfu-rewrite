from email import message
import disnake
import random
import asyncio


from disnake.ext import commands

# ui
from stfubot.ui.fight.fight_ui import FightUi
from stfubot.ui.confirmation import Confirm
from stfubot.ui.place_holder import PlaceHolder

# utils
from utils.decorators import database_check
from utils.functions import (
    play_files,
    sign,
    game,
    get_fight_image,
    get_stand_status,
    get_turn_special,
)

# stfu model
from models.bot.stfubot import StfuBot
from models.gameobjects.stands import Stand, stand_from_dict, get_stand_from_template
from globals.emojis import CustomEmoji


class fight(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    @commands.slash_command(name="fight", description="fight someone in your server")
    async def fight(
        self, Interaction: disnake.ApplicationCommandInteraction, ennemy: disnake.Member
    ):
        await Interaction.response.defer()
        # Check if both user are already registered
        if not await self.stfubot.database.user_in_database(Interaction.author.id):
            embed = disnake.Embed(
                title=f"{Interaction.author.name} PLACE HOLDER",
                colour=disnake.Colour.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        if not await self.stfubot.database.user_in_database(ennemy.id):
            embed = disnake.Embed(
                title=f"{ennemy.name} PLACE HOLDER",
                colour=disnake.Colour.red(),
            )
            embed.set_image(url=self.stfubot.avatar_url)
            await Interaction.send(embed=embed)
            return
        # Get the users
        user_1 = await self.stfubot.database.get_user_info(ennemy.id)
        user_2 = await self.stfubot.database.get_user_info(Interaction.author.id)
        user_1.discord = Interaction.author
        user_2.discord = ennemy
        image = await get_fight_image(user_1.discord, user_2.discord, self.stfubot)
        embed = disnake.Embed(
            title=f"{ennemy.name} PLACE HOLDER", colour=disnake.Colour.blue()
        )
        view = Confirm(Interaction, user=ennemy)
        await Interaction.send(embed=embed, view=view)
        if await view.wait():
            raise asyncio.TimeoutError
        await Interaction.edit_original_message(embed=embed, view=PlaceHolder())
        if not view.value:
            embed = disnake.Embed(
                title=f"{ennemy.name} PLACE HOLDER", colour=disnake.Colour.blue()
            )
            await Interaction.channel.send(embed=embed)
            return
        # Everyone should have at least one stand in their main soooo.

        # Set up some fight Variable
        gold_experience_requiem = False
        gold_experience_requiem_done = True
        tusk_act_4 = False
        king_crimson = False
        combat_log = []
        turn = 0
        # Determine who start fist
        start_1 = sum([i.current_speed for i in user_1.stands])
        start_2 = sum([i.current_speed for i in user_2.stands])
        players = [user_1, user_2]
        if start_2 > start_1:
            players = [user_2, user_1]
        if start_2 == start_1:
            random.shuffle(players)
        # We give a little help if you start second
        for stand in players[1].stands:
            stand.special_meter += 1
        # Message used for status and attacks
        embed = disnake.Embed(
            title=f"{user_1.discord.name} vs {user_2.discord.name}",
            color=disnake.Color.blue(),
        )
        embed.set_image(file=image)
        message_1 = await Interaction.channel.send(embed=embed)
        # Message used to display specials
        embed = disnake.Embed(colour=disnake.Colour.blue())
        embed.set_image(url="https://c.tenor.com/B_J3xedKvA8AAAAC/jojo-anime.gif")
        message_2 = await Interaction.channel.send(embed=embed)
        # Game loop
        print(game(players[0].stands, players[1].stands))
        while game(players[0].stands, players[1].stands):
            # We get with player must play based of parity looks hard but it is not
            # Look in idle what n % 2 does if you need to
            player = players[turn % 2]
            watcher = players[(turn + 1) % 2]
            print(turn)

            for stand in player.stands:
                # We check again to make sure the game as not ended
                if not game(players[0].stands, players[1].stands):
                    break
                # First we check for attacks then we check for special
                # Basic Attacks
                if stand.is_alive() and not (stand.is_stunned()):
                    # embed stuff
                    embed = disnake.Embed(
                        title=f"Fight ⚔️:`{player.discord.name}` choose an ennemy stand to attack",
                        description=f"turn: `{turn + 1}`",
                        color=disnake.Color.blue(),
                    )
                    status = get_stand_status(stand)
                    turn_ = get_turn_special(stand)
                    embed.add_field(
                        name=f"Who `『{stand.name}』` should attack ?",
                        value=f"`HP`:`{stand.current_hp}/{stand.start_hp}❤️`\n`STATUS`:{status}\n`Ability`:{turn_}\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
                        inline=False,
                    )
                    for ennemy_stand in watcher.stands:
                        if ennemy_stand:
                            etoile = (
                                ennemy_stand.stars * "⭐" + "🌟" * ennemy_stand.ascension
                            )
                            status = get_stand_status(ennemy_stand)
                            spe = get_turn_special(ennemy_stand)
                            embed.add_field(
                                name=f"`『{ennemy_stand.name}』`\n`{etoile}`",
                                value=f"HP:`{int(ennemy_stand.current_hp)}/{int(ennemy_stand.start_hp)}❤️`\n`STATUS`:{status}\n`Ability`:{spe}\n    ▬▬▬▬▬▬▬▬▬",
                                inline=True,
                            )
                    view = FightUi(
                        message_1, player.discord, watcher.stands, player.stands
                    )
                    # still embed things
                    await message_1.edit(embed=embed, view=view)
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
                    data = stand.attack(targeted_stand)
                    info_message = ""
                    if data["Dodged"]:
                        info_message = f"{targeted_stand.name} "
                    elif data["critical"]:
                        info_message = f"{targeted_stand.name} "
                    else:
                        info_message = f"{targeted_stand.name} "
                    embed = disnake.Embed(
                        title=info_message, color=disnake.Color.blue()
                    )
                    embed.set_image(
                        url=f"https://storage.stfurequiem.com/Image/{stand.id}.png"
                    )
                    await message_2.edit(embed=embed)
                # Special
                if (
                    stand.is_alive()
                    and not (stand.is_stunned())
                    and stand.as_special()
                    and not gold_experience_requiem
                ):
                    await asyncio.sleep(1.5)
                    # actual special ability
                    payload, message = stand.special(player.stands, watcher.stands)
                    embed = disnake.Embed(title=message, color=disnake.Color.blue())
                    embed.set_image(
                        url=f"https://storage.stfurequiem.com/special/{stand.id}.gif"
                    )
                    # They payload now effect the fights
                    gold_experience_requiem |= payload["gold_experience_requiem"]
                    tusk_act_4 |= payload["tusk_act_4"]
                    king_crimson |= payload["king_crimson"]
                    # edit the second embed
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


def setup(client: StfuBot):
    client.add_cog(fight(client))